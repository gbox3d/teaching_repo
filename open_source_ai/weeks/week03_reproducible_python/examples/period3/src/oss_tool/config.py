"""설정 로더 — 기본값 < .env 파일 < 셸 환경변수 < 명령 인자.

좁은 범위일수록 우선한다. 값마다 어디서 왔는지(source)를 함께 돌려주므로
`oss-tool config` 가 "지금 어떤 값이 왜 쓰이는지"를 보여 줄 수 있다.

python-dotenv 의 `dotenv_values()` 는 .env 를 dict 로만 읽고 os.environ 을 건드리지 않는다.
`load_dotenv()` 는 .env 를 os.environ 에 넣는 방식이라 편하지만 출처 구분이 사라진다.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import dotenv_values

# 교재 검증용 기본값. 실제 모델 ID·양자화는 학기별 환경 기준표에서 확정하고 .env 로 바꾼다.
DEFAULTS: dict[str, str] = {
    "OLLAMA_HOST": "http://localhost:11434",
    "OLLAMA_MODEL": "qwen3:8b",  # RTX 4070 기준. CPU 만 있는 PC 는 .env 에서 qwen3:0.6b 로 바꾼다.
}
# 기본값이 없어도 읽어 두는 선택 키. 5주차 Hugging Face 실습부터 쓴다.
OPTIONAL_KEYS: tuple[str, ...] = ("HF_TOKEN",)
# 키 이름에 이 단어가 들어가면 값을 화면·파일에 그대로 쓰지 않는다.
SECRET_MARKERS: tuple[str, ...] = ("TOKEN", "KEY", "SECRET", "PASSWORD")


@dataclass(frozen=True)
class Setting:
    key: str
    value: str | None
    source: str  # "default" | ".env" | "env" | "arg"

    @property
    def is_secret(self) -> bool:
        return any(marker in self.key.upper() for marker in SECRET_MARKERS)

    def display(self) -> str:
        """화면·저장용 표현. 비밀은 설정 여부만 보여 준다."""
        if not self.value:
            return "(비어 있음)"
        if self.is_secret:
            return "(설정됨, 가려짐)"
        return self.value


def load_settings(
    overrides: dict[str, str | None] | None = None,
    env_file: str | Path = ".env",
) -> dict[str, Setting]:
    """모든 키에 대해 (값, 출처) 를 계산한다. overrides 는 명령 인자에서 온 값."""
    overrides = overrides or {}
    env_path = Path(env_file)
    file_values: dict[str, str | None] = dotenv_values(env_path) if env_path.is_file() else {}

    settings: dict[str, Setting] = {}
    for key in (*DEFAULTS, *OPTIONAL_KEYS):
        value: str | None = DEFAULTS.get(key)
        source = "default"
        if file_values.get(key):
            value, source = file_values[key], ".env"
        if os.environ.get(key):
            value, source = os.environ[key], "env"
        if overrides.get(key):
            value, source = overrides[key], "arg"
        settings[key] = Setting(key=key, value=value, source=source)
    return settings


def settings_to_dict(settings: dict[str, Setting]) -> dict[str, object]:
    """JSON 저장용. 비밀로 보이는 값은 가린 채로만 내보낸다(outputs/ 도 유출 경로다)."""
    return {
        key: {"value": setting.display(), "source": setting.source, "secret": setting.is_secret}
        for key, setting in settings.items()
    }
