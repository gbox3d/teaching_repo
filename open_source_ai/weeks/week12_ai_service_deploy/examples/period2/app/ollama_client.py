"""Ollama 모델 서버와 이야기하는 얇은 클라이언트.

- 앱 서버(FastAPI)는 이 클래스만 통해 Ollama 에 접근한다.
- 실패를 세 가지 예외로 구분한다: 연결 실패(OllamaUnavailable), 시간 초과(OllamaTimeout),
  모델 없음(OllamaModelMissing). main.py 가 이를 502·504·503 으로 바꾼다.
- 13주차에서 이 클래스를 가짜(Fake) 클라이언트로 바꿔 끼워 테스트한다.

단독 점검: uv run python -m app.ollama_client --prompt "uv 가 무엇인지 한 문장으로"
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
from collections.abc import AsyncIterator
from datetime import datetime
from pathlib import Path
from typing import Any

import httpx
from dotenv import load_dotenv


class OllamaError(Exception):
    """Ollama 관련 오류의 공통 조상."""


class OllamaUnavailable(OllamaError):
    """연결 거부·주소 오류 — 모델 서버가 꺼져 있거나 OLLAMA_HOST 가 틀렸다."""


class OllamaTimeout(OllamaError):
    """연결은 됐지만 제한 시간 안에 응답이 오지 않았다."""


class OllamaModelMissing(OllamaError):
    """요청한 모델이 서버에 없다(pull 하지 않았거나 이름이 틀렸다)."""


class OllamaClient:
    def __init__(self, host: str, model: str, timeout: float = 60.0) -> None:
        self.host = host.rstrip("/")
        self.model = model
        self.timeout = timeout
        # 연결 자체는 5초 안에 끝나야 하고, 생성 응답은 timeout 초까지 기다린다.
        self._http = httpx.AsyncClient(base_url=self.host, timeout=httpx.Timeout(timeout, connect=5.0))

    @classmethod
    def from_env(cls) -> OllamaClient:
        """설정 계층: 기본값 < .env < 셸 환경변수. load_dotenv 는 이미 있는 환경변수를 덮어쓰지 않는다."""
        load_dotenv()
        return cls(
            host=os.environ.get("OLLAMA_HOST", "http://localhost:11434"),
            model=os.environ.get("OLLAMA_MODEL", "qwen3:8b"),
            timeout=float(os.environ.get("OLLAMA_TIMEOUT", "60")),
        )

    async def aclose(self) -> None:
        await self._http.aclose()

    def _payload(self, messages: list[dict[str, str]], model: str | None, temperature: float, max_tokens: int, stream: bool) -> dict[str, Any]:
        return {
            "model": model or self.model,
            "messages": messages,
            "stream": stream,
            # Qwen3 계열은 thinking 출력이 답과 섞여 나온다. 서비스 응답에는 답만 필요하므로 끈다.
            "think": False,
            "options": {"temperature": temperature, "num_predict": max_tokens},
        }

    def _check_status(self, status_code: int, body_text: str, model: str) -> None:
        if status_code == 404:
            raise OllamaModelMissing(f"모델 '{model}' 이(가) {self.host} 에 없다. `ollama list` 로 이름을 확인하고 필요하면 pull 한다.")
        if status_code >= 400:
            raise OllamaError(f"Ollama 오류 {status_code}: {body_text[:200]}")

    async def _request(self, method: str, path: str, **kwargs: Any) -> httpx.Response:
        try:
            resp = await self._http.request(method, path, **kwargs)
        except httpx.ConnectTimeout as exc:
            raise OllamaUnavailable(f"{self.host} 에 5초 안에 연결되지 않았다. 주소와 방화벽을 확인한다.") from exc
        except httpx.TimeoutException as exc:
            raise OllamaTimeout(f"{self.host} 가 {self.timeout:g}초 안에 응답하지 않았다 ({method} {path}).") from exc
        except httpx.TransportError as exc:
            raise OllamaUnavailable(f"{self.host} 에 연결할 수 없다. Ollama 가 실행 중인지, OLLAMA_HOST 가 맞는지 확인한다. ({type(exc).__name__})") from exc
        model = kwargs.get("json", {}).get("model", self.model) if isinstance(kwargs.get("json"), dict) else self.model
        self._check_status(resp.status_code, resp.text, model)
        return resp

    async def list_models(self) -> list[str]:
        """GET /api/tags — 서버에 내려받아 둔 모델 이름 목록."""
        resp = await self._request("GET", "/api/tags")
        return [item.get("name", "") for item in resp.json().get("models", [])]

    async def chat(self, messages: list[dict[str, str]], *, model: str | None = None, temperature: float = 0.2, max_tokens: int = 256) -> dict[str, Any]:
        """POST /api/chat 비스트리밍. 응답 전체(JSON)를 그대로 돌려준다."""
        payload = self._payload(messages, model, temperature, max_tokens, stream=False)
        resp = await self._request("POST", "/api/chat", json=payload)
        return resp.json()

    async def chat_stream(self, messages: list[dict[str, str]], *, model: str | None = None, temperature: float = 0.2, max_tokens: int = 256) -> AsyncIterator[dict[str, Any]]:
        """POST /api/chat 스트리밍. NDJSON 한 줄을 dict 하나로 바꿔 차례로 내보낸다."""
        payload = self._payload(messages, model, temperature, max_tokens, stream=True)
        try:
            async with self._http.stream("POST", "/api/chat", json=payload) as resp:
                if resp.status_code >= 400:
                    await resp.aread()
                    self._check_status(resp.status_code, resp.text, payload["model"])
                async for line in resp.aiter_lines():
                    if line.strip():
                        yield json.loads(line)
        except httpx.ConnectTimeout as exc:
            raise OllamaUnavailable(f"{self.host} 에 5초 안에 연결되지 않았다.") from exc
        except httpx.TimeoutException as exc:
            raise OllamaTimeout(f"{self.host} 가 {self.timeout:g}초 안에 다음 청크를 보내지 않았다.") from exc
        except httpx.TransportError as exc:
            raise OllamaUnavailable(f"{self.host} 에 연결할 수 없다. ({type(exc).__name__})") from exc


async def _check(prompt: str, out_dir: Path) -> int:
    """단독 점검: 모델 목록 → 비스트리밍 대화 1회 → outputs/ 기록."""
    client = OllamaClient.from_env()
    report: dict[str, Any] = {"host": client.host, "model": client.model, "checked_at": datetime.now().isoformat(timespec="seconds")}
    try:
        report["models"] = await client.list_models()
        data = await client.chat([{"role": "user", "content": prompt}], max_tokens=128)
        report["reply"] = data.get("message", {}).get("content", "")
        report["eval_count"] = data.get("eval_count")
        print(f"[ok] {client.model} → {report['reply'][:120]!r}")
        code = 0
    except OllamaError as exc:
        report["error"] = {"type": type(exc).__name__, "detail": str(exc)}
        print(f"[fail] {type(exc).__name__}: {exc}")
        code = 1
    finally:
        await client.aclose()
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"ollama-check-{datetime.now():%Y%m%d-%H%M%S}.json"
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"기록: {path}")
    return code


def main() -> None:
    parser = argparse.ArgumentParser(description="앱 서버 없이 Ollama 클라이언트만 점검한다.")
    parser.add_argument("--prompt", default="uv 가 무엇인지 한 문장으로 설명해 줘.")
    parser.add_argument("--out-dir", default=os.environ.get("LOG_DIR", "outputs"))
    args = parser.parse_args()
    raise SystemExit(asyncio.run(_check(args.prompt, Path(args.out_dir))))


if __name__ == "__main__":
    main()
