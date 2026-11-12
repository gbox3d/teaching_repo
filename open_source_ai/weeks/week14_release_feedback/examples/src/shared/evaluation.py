"""정답을 가진 부모 프로세스의 채점기. 학생 모듈을 여기서 import하지 않는다."""

import json
import math
import os
import queue
import signal
import subprocess
import sys
import threading
import time

from shared import (
    MAX_ANSWER_LENGTH, MAX_ITEMS, MAX_QUESTION_LENGTH, MAX_SOURCE_LENGTH,
    normalize, validate_response, validate_strings,
)

QUESTION_TIMEOUT = 30.0
WARMUP_TIMEOUT = 120.0
WARMUP_QUESTION = "원광대학교의 소재 도시 이름은 무엇인가요?"
MAX_PROTOCOL_LENGTH = 65536
CATEGORIES = ("fact", "composite", "unknown")


def validate_gold(gold: object) -> dict:
    if type(gold) is not dict or set(gold) != {"id", "expected", "sources", "abstain"}:
        raise ValueError("정답에는 id, expected, sources, abstain만 있어야 합니다.")
    validate_id(gold["id"])
    if type(gold["abstain"]) is not bool:
        raise ValueError("정답 abstain은 bool이어야 합니다.")
    expected = gold["expected"]
    if type(expected) is not list or len(expected) > MAX_ITEMS:
        raise ValueError("expected는 길이 제한 내 별칭 그룹 배열이어야 합니다.")
    for group in expected:
        validate_strings(group, "expected 별칭 그룹", MAX_ANSWER_LENGTH)
        if not group:
            raise ValueError("expected의 별칭 그룹은 비어 있으면 안 됩니다.")
    validate_strings(gold["sources"], "정답 sources", MAX_SOURCE_LENGTH)
    if gold["abstain"]:
        if expected or gold["sources"]:
            raise ValueError("unknown 정답에는 사실과 출처가 없어야 합니다.")
    elif not expected or not gold["sources"]:
        raise ValueError("known 정답에는 사실과 출처가 있어야 합니다.")
    return gold


def validate_id(value: object) -> None:
    if type(value) is not str or not value.strip() or len(value) > 128 or value != value.strip():
        raise ValueError("id는 양끝 공백 없는 1~128자 문자열이어야 합니다.")


def validate_dataset(questions: object, answers: object) -> dict[str, dict]:
    if type(questions) is not list or not questions or type(answers) is not list:
        raise ValueError("질문과 정답은 배열이어야 하며 질문은 하나 이상 필요합니다.")
    question_ids = set()
    for question in questions:
        if type(question) is not dict or set(question) != {"id", "category", "question"}:
            raise ValueError("문항에는 id, category, question만 있어야 합니다.")
        validate_id(question["id"])
        if question["id"] in question_ids:
            raise ValueError(f"문항 id 중복: {question['id']}")
        question_ids.add(question["id"])
        if question["category"] not in CATEGORIES:
            raise ValueError("category는 fact, composite, unknown 중 하나여야 합니다.")
        text = question["question"]
        if type(text) is not str or not text.strip() or len(text) > MAX_QUESTION_LENGTH:
            raise ValueError("질문은 비어 있지 않은 길이 제한 내 문자열이어야 합니다.")
    gold_by_id = {}
    for gold in answers:
        validate_gold(gold)
        if gold["id"] in gold_by_id:
            raise ValueError(f"정답 id 중복: {gold['id']}")
        gold_by_id[gold["id"]] = gold
    if question_ids != set(gold_by_id):
        raise ValueError("질문과 정답의 id 집합이 다릅니다. 누락·추가·오기를 확인하세요.")
    for question in questions:
        if (question["category"] == "unknown") != gold_by_id[question["id"]]["abstain"]:
            raise ValueError(f"범주와 정답 abstain 불일치: {question['id']}")
    return gold_by_id


def match_facts(predictions: set[str], groups: list[set[str]]) -> int:
    """증가 경로로 최대 이분 매칭을 구한다. 응답 하나는 사실 하나에만 배정한다."""
    owners: dict[int, str] = {}

    def assign(prediction: str, visited: set[int]) -> bool:
        for index, aliases in enumerate(groups):
            if prediction not in aliases or index in visited:
                continue
            visited.add(index)
            if index not in owners or assign(owners[index], visited):
                owners[index] = prediction
                return True
        return False

    return sum(assign(prediction, set()) for prediction in sorted(predictions))


def f1(matches: int, predicted: int, expected: int) -> float:
    return 2 * matches / (predicted + expected) if predicted + expected else 0.0


def zero_result(error: str | None = None, status: str = "ok") -> dict:
    return {
        "score": 0.0, "status": status, "error": error,
        "subscores": {"answer_f1": 0.0, "source_f1": 0.0, "matched_facts": 0,
                      "answer_points": 0.0, "source_points": 0.0, "abstain_points": 0.0},
    }


def score_response(response: object, gold: dict) -> dict:
    """Ollama 없이 사용 가능한 순수 채점 함수. 형식 오류 응답은 0점이다."""
    validate_gold(gold)
    result = zero_result()
    try:
        validate_response(response)
    except ValueError as exc:
        return zero_result(str(exc), "invalid_response")
    if gold["abstain"]:
        if response["abstain"] and response["answers"] == [] and response["sources"] == []:
            result["score"] = 100.0
            result["subscores"]["abstain_points"] = 100.0
        return result
    if response["abstain"]:
        return result
    predictions = {normalize(item) for item in response["answers"]}
    groups = [{normalize(alias) for alias in group} for group in gold["expected"]]
    matches = match_facts(predictions, groups)
    answer_f1 = f1(matches, len(predictions), len(groups))
    sources = {normalize(item) for item in response["sources"]}
    expected_sources = {normalize(item) for item in gold["sources"]}
    source_f1 = f1(len(sources & expected_sources), len(sources), len(expected_sources))
    source_points = 20 * source_f1 if answer_f1 > 0 else 0.0
    result["subscores"].update(
        answer_f1=answer_f1, source_f1=source_f1, matched_facts=matches,
        answer_points=80 * answer_f1, source_points=source_points,
    )
    result["score"] = 80 * answer_f1 + source_points
    return result


class Worker:
    """문항 사이에는 프로세스를 유지하고 실패 시 종료한다. 보안 격리는 아니다."""

    def __init__(self, command: list[str] | None = None):
        self.command = command or [sys.executable, "-u", "-m", "shared.worker"]
        self.process = None
        self.thread = None
        self.windows_job = None

    def attach_windows_job(self) -> None:
        """부모가 먼저 끝나도 자식을 종료할 수 있도록 전용 Windows Job에 묶는다."""
        import ctypes
        from ctypes import wintypes

        api = ctypes.WinDLL("kernel32", use_last_error=True)
        for name, arguments, result in (
            ("CreateJobObjectW", [ctypes.c_void_p, wintypes.LPCWSTR], wintypes.HANDLE),
            ("AssignProcessToJobObject", [wintypes.HANDLE, wintypes.HANDLE], wintypes.BOOL),
            ("TerminateJobObject", [wintypes.HANDLE, wintypes.UINT], wintypes.BOOL),
            ("CloseHandle", [wintypes.HANDLE], wintypes.BOOL),
        ):
            function = getattr(api, name)
            function.argtypes = arguments
            function.restype = result
        job = api.CreateJobObjectW(None, None)
        if not job:
            raise ctypes.WinError(ctypes.get_last_error())
        self.windows_job = (api, job)
        if not api.AssignProcessToJobObject(job, int(self.process._handle)):
            raise ctypes.WinError(ctypes.get_last_error())

    def request(self, question: str, timeout: float) -> object:
        try:
            if self.process is None:
                env = os.environ.copy()
                env.update(PYTHONIOENCODING="utf-8", PYTHONUTF8="1")
                self.process = subprocess.Popen(
                    self.command, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                    stderr=None, text=True, encoding="utf-8", bufsize=1, env=env,
                    start_new_session=os.name != "nt",
                    creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if os.name == "nt" else 0,
                )
                if os.name == "nt":
                    self.attach_windows_job()
            process = self.process
            replies = queue.Queue(maxsize=1)

            def exchange():
                try:
                    process.stdin.write(json.dumps(question, ensure_ascii=False) + "\n")
                    process.stdin.flush()
                    line = process.stdout.readline(MAX_PROTOCOL_LENGTH + 1)
                    if not line or not line.endswith("\n") or len(line) > MAX_PROTOCOL_LENGTH:
                        raise ValueError("워커 응답이 비어 있거나 길이 제한을 초과했습니다.")
                    replies.put((True, json.loads(line)))
                except Exception as exc:
                    replies.put((False, exc))

            self.thread = threading.Thread(target=exchange, name="evaluation-worker-io", daemon=True)
            self.thread.start()
            try:
                success, reply = replies.get(timeout=timeout)
            except queue.Empty:
                raise TimeoutError(f"문항 제한 시간 {timeout:g}초를 초과했습니다.") from None
            self.thread.join()
            self.thread = None
            if not success:
                raise reply
            if type(reply) is not dict or type(reply.get("ok")) is not bool:
                raise ValueError("워커 응답 봉투 형식이 올바르지 않습니다.")
            if not reply["ok"]:
                raise RuntimeError(str(reply.get("error", "워커 실행 오류")))
            if set(reply) != {"ok", "response"}:
                raise ValueError("워커 응답 봉투에 누락 또는 추가 키가 있습니다.")
            return reply["response"]
        except BaseException:
            self.close()
            raise

    def close(self) -> None:
        process = self.process
        if process is None:
            return
        try:
            if os.name == "nt":
                if self.windows_job is not None:
                    api, job = self.windows_job
                    if not api.TerminateJobObject(job, 1):
                        import ctypes
                        raise ctypes.WinError(ctypes.get_last_error())
                if process.poll() is None:
                    process.kill()
            else:
                # 부모가 먼저 끝났어도 같은 세션의 자식이 파이프를 유지할 수 있다.
                process.poll()  # 종료한 세션 리더를 먼저 회수한다(macOS zombie 그룹 처리).
                for attempt in range(2):
                    try:
                        os.killpg(process.pid, signal.SIGKILL)
                        break
                    except ProcessLookupError:
                        break
                    except PermissionError:
                        # poll 직후 리더가 종료한 경쟁 조건이면 회수 후 한 번 더 확인한다.
                        if attempt or process.poll() is None:
                            raise
            process.wait()
        finally:
            if self.windows_job is not None:
                api, job = self.windows_job
                api.CloseHandle(job)
                self.windows_job = None
            if self.thread is not None:
                self.thread.join(timeout=2)
                self.thread = None
            process.stdin.close()
            process.stdout.close()
            self.process = None

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()


def evaluate(
    questions: list[dict], answers: list[dict], *,
    timeout: float = QUESTION_TIMEOUT, warmup_timeout: float = WARMUP_TIMEOUT,
    worker_command: list[str] | None = None, on_result=None,
) -> dict:
    """공개·비공개 runner가 같은 문항/정답 배열 계약으로 호출하는 부모 API."""
    gold_by_id = validate_dataset(questions, answers)
    if any(type(value) not in (int, float) or not math.isfinite(value) or value <= 0
           for value in (timeout, warmup_timeout)):
        raise ValueError("제한 시간은 양의 유한한 수여야 합니다.")
    started = time.perf_counter()
    results = []
    warmups = []
    with Worker(worker_command) as worker:
        for question in questions:
            preparation_error = None
            if worker.process is None:
                warmup_started = time.perf_counter()
                warmup = {"before_id": question["id"], "status": "ok", "error": None,
                          "response": None}
                try:
                    warmup["response"] = worker.request(WARMUP_QUESTION, warmup_timeout)
                except Exception as exc:
                    preparation_error = exc
                    warmup.update(status="timeout" if isinstance(exc, TimeoutError) else "error",
                                  error=f"{type(exc).__name__}: {exc}")
                else:
                    try:
                        validate_response(warmup["response"])
                    except ValueError as exc:
                        # 응답 형식만 틀리면 모델은 이미 준비됐다. 프로세스를 유지한다.
                        warmup.update(status="invalid_response", error=str(exc))
                warmup["latency"] = time.perf_counter() - warmup_started
                warmups.append(warmup)
            question_started = time.perf_counter()
            response = None
            gold = gold_by_id[question["id"]]
            try:
                if preparation_error is not None:
                    # 준비가 실패한 새 프로세스에 제한 30초만 주어 본 문항을 보내지 않는다.
                    raise preparation_error
                response = worker.request(question["question"], timeout)
                scored = score_response(response, gold)
            except Exception as exc:
                worker.close()
                prefix = "모델 준비 실패로 문항을 실행하지 못했습니다. " if preparation_error else ""
                scored = zero_result(f"{prefix}{type(exc).__name__}: {exc}",
                                     "timeout" if isinstance(exc, TimeoutError) else "error")
            row = dict(question, response=response, gold=gold, **scored,
                       latency=time.perf_counter() - question_started)
            results.append(row)
            if on_result is not None:
                on_result(row)
    categories = {}
    for category in CATEGORIES:
        scores = [row["score"] for row in results if row["category"] == category]
        categories[category] = {
            "count": len(scores), "mean_score": sum(scores) / len(scores) if scores else None,
        }
    return {"results": results, "categories": categories, "total": len(results),
            "mean_score": sum(row["score"] for row in results) / len(questions),
            "warmup": warmups[0], "warmups": warmups,
            "elapsed_seconds": time.perf_counter() - started}
