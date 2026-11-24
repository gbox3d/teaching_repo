"""4교시 추론 점검. 질문 하나를 봇에 보내는 동안 Ollama 요청과 응답을 가로채 보여 주고, 의심되는 원인을 적는다.
봇 코드는 바꾸지 않는다. 봇이 urllib로 보낸 요청만 잡고, 그중 /api/chat과 /api/embed를 자세히 본다.
판정과 출력 함수는 Ollama 없이 시험할 수 있다."""

import http.client
import importlib
import io
import json
import time
import urllib.request
from urllib.error import HTTPError
from urllib.parse import urlsplit
from urllib.request import ProxyHandler, Request, build_opener
from urllib.response import addinfourl

from shared import MAX_QUESTION_LENGTH, configure_utf8, validate_response

BOT = "student_bot"  # ex04에서 잰 봇과 같게 둔다. 특강의 임베딩 RAG 봇은 "rag_bot"
QUESTION_TIMEOUT = 30  # 14주 채점기의 문항당 제한(초)과 비교한다.
SHOW_PROMPT = True  # 보낸 messages 전문을 출력한다. False면 역할과 글자 수만 보인다.
PREVIEW = 300  # 응답 본문처럼 긴 글은 이 글자 수까지만 보인다.
SLOW_LOAD = 1.0  # load_duration이 이 초보다 길면 모델을 새로 올린 것으로 본다.
NEAR_CONTEXT = 0.9  # prompt_eval_count가 실행 컨텍스트의 이 비율 이상이면 한도에 가깝다고 본다.


# ---------- 가로채기와 조회 ----------

def read_body(raw: bytes) -> tuple[dict, str]:
    """본문의 글과, JSON 객체면 읽은 사전(아니면 빈 사전). 스트리밍 응답(여러 줄 JSON)은 글로만 남는다."""
    text = raw.decode("utf-8", errors="replace")
    try:
        value = json.loads(text)
    except json.JSONDecodeError:
        value = None
    return (value if type(value) is dict else {}), text


def ask(bot, question: str) -> tuple[list[dict], object, float]:
    """bot.answer(question)을 부르는 동안 urllib 요청과 응답을 기록한다. 예외가 나도 원래 open으로 되돌린다.
    돌려주는 값은 (호출 기록, 봇의 반환값 또는 봇이 낸 예외, 걸린 초)다."""
    calls = []
    original = urllib.request.OpenerDirector.open

    def recording_open(self, fullurl, data=None, *args, **kwargs):
        url = fullurl if isinstance(fullurl, str) else fullurl.full_url
        body = data if data is not None or isinstance(fullurl, str) else fullurl.data
        call = {"url": url, "path": urlsplit(url).path.rstrip("/"),
                "request": read_body(body)[0] if isinstance(body, bytes) else {},
                "status": None, "response": {}, "text": "", "error": None, "seconds": None}
        calls.append(call)
        started = time.perf_counter()
        try:
            response = original(self, fullurl, data, *args, **kwargs)
            raw = response.read()
            response.close()
        except HTTPError as exc:
            try:
                raw = exc.read()
            except Exception:
                raw = b""
            call["response"], call["text"] = read_body(raw)
            call.update(status=exc.code, seconds=time.perf_counter() - started)
            # 봇도 오류 본문을 읽을 수 있게 읽은 바이트로 같은 오류를 다시 만들어 올린다.
            raise HTTPError(exc.filename, exc.code, exc.msg, exc.hdrs, io.BytesIO(raw)) from None
        except Exception as exc:
            call.update(error=f"{type(exc).__name__}: {exc}", seconds=time.perf_counter() - started)
            raise
        call["response"], call["text"] = read_body(raw)
        call.update(status=response.status, seconds=time.perf_counter() - started)
        # 읽은 바이트로 본문·상태·헤더가 같은 응답을 만들어 돌려준다. HTTPResponse의 reason·getheader()는 없다.
        return addinfourl(io.BytesIO(raw), response.headers, getattr(response, "url", url), response.status)

    urllib.request.OpenerDirector.open = recording_open
    started = time.perf_counter()
    try:
        result = bot.answer(question)
    except Exception as exc:
        result = exc
    finally:
        urllib.request.OpenerDirector.open = original
    return calls, result, time.perf_counter() - started


def fetch(url: str, body: dict | None = None) -> object:
    """진단용 조회(/api/show, /api/ps). 모델을 올리지 않는다. 연결 실패, HTTP 오류, HTTP가 아닌 응답이면 None이다."""
    data = None if body is None else json.dumps(body).encode("utf-8")
    request = Request(url, data=data, headers={"Content-Type": "application/json"})
    try:
        with build_opener(ProxyHandler({})).open(request, timeout=5) as response:
            return json.load(response)
    except (OSError, ValueError, http.client.HTTPException):
        return None


def look_up(calls: list[dict], shown: dict) -> object:
    """봇이 부른 서버에 생성 모델의 /api/show를 모델마다 한 번 조회해 shown에 넣고, /api/ps 결과를 돌려준다."""
    for call in calls:
        parts, model = urlsplit(call["url"]), model_of(call)
        if is_chat(call) and model != "?" and shown.get(model) is None:
            shown[model] = fetch(f"{parts.scheme}://{parts.netloc}/api/show", {"model": model})
    parts = urlsplit(calls[0]["url"]) if calls else None
    return fetch(f"{parts.scheme}://{parts.netloc}/api/ps") if parts else None


# ---------- 호출 기록 읽기 ----------

def cut(text: object) -> str:
    """긴 글은 PREVIEW 글자까지만 남기고 줄바꿈은 \\n으로 보인다."""
    text = str(text).replace("\n", "\\n")
    return text if len(text) <= PREVIEW else f"{text[:PREVIEW]}…(+{len(text) - PREVIEW}자)"


def model_of(call: dict) -> str:
    return str(call["request"].get("model") or "?")


def options_of(call: dict) -> dict:
    options = call["request"].get("options")
    return options if type(options) is dict else {}


def is_chat(call: dict) -> bool:
    return call["path"].endswith("/api/chat")


def is_embed(call: dict) -> bool:
    return call["path"].endswith("/api/embed")


def full_name(model: str) -> str:
    """태그를 생략한 모델 이름은 :latest로 본다."""
    return model if ":" in model.rsplit("/", 1)[-1] else model + ":latest"


def seconds(nanoseconds: object) -> float | None:
    """Ollama의 *_duration 값은 나노초다."""
    return nanoseconds / 1e9 if type(nanoseconds) in (int, float) else None


def load_seconds(calls: list[dict]) -> float:
    """이번 질문의 호출들이 모델을 올리는 데 쓴 시간(load_duration의 합)."""
    return sum(seconds(call["response"].get("load_duration")) or 0 for call in calls)


def error_text(call: dict) -> str:
    return str(call["response"].get("error") or call["text"].strip() or call["error"] or "")


def reply_of(call: dict) -> tuple[str | None, str]:
    """/api/chat 응답의 본문과 생각 글. message가 없으면 본문은 None이다."""
    message = call["response"].get("message")
    if type(message) is not dict:
        return None, ""
    return str(message.get("content") or ""), str(message.get("thinking") or "")


def check_content(content: str) -> tuple[object, str | None, bool]:
    """본문을 json.loads로 읽는다. 돌려주는 값은 (읽은 값, 오류, 중괄호 안쪽만 떼면 JSON으로 읽히는지)다."""
    text = content.strip()
    try:
        return json.loads(text), None, False
    except json.JSONDecodeError as exc:
        error = f"{exc.msg} (위치 {exc.pos})"
    try:
        json.loads(text[text.index("{"):text.rindex("}") + 1])
        return None, error, True
    except ValueError:  # 중괄호가 없거나 안쪽도 JSON이 아니다.
        return None, error, False


def modelfile_parameters(info: object) -> dict[str, str]:
    """/api/show의 parameters(한 줄에 '이름 값')를 사전으로 바꾼다. stop처럼 여러 줄인 값은 이어 붙인다."""
    values = {}
    text = info.get("parameters") if type(info) is dict else None
    for line in str(text or "").splitlines():
        name, _, value = line.strip().partition(" ")
        if name:
            values[name] = f"{values[name]}, {value.strip()}" if name in values else value.strip()
    return values


def ps_rows(ps: object) -> list[tuple[str, float | None, dict]]:
    """/api/ps의 모델마다 (이름, GPU 비율, 항목). GPU 비율은 size_vram/size이고 100보다 작으면 일부가 CPU에서 돈다."""
    models = ps.get("models") if type(ps) is dict else None
    rows = []
    for entry in models if type(models) is list else []:
        if type(entry) is dict:
            size, vram = entry.get("size"), entry.get("size_vram")
            percent = 100 * vram / size if type(size) is int and type(vram) is int and size > 0 else None
            rows.append((str(entry.get("name") or entry.get("model") or "?"), percent, entry))
    return rows


def run_context(call: dict, info: object, ps: object) -> tuple[int | None, str]:
    """이번 실행의 컨텍스트 길이와 출처. /api/ps, 요청의 num_ctx, Modelfile num_ctx 순서로 찾는다.
    /api/ps는 모델이 실제로 올라간 길이다. 요청값은 /api/ps에서 이 모델의 길이를 찾지 못했을 때만 쓴다."""
    for name, _, entry in ps_rows(ps):
        if full_name(name) == full_name(model_of(call)) and type(entry.get("context_length")) is int:
            return entry["context_length"], "/api/ps"
    if type(options_of(call).get("num_ctx")) is int:
        return options_of(call)["num_ctx"], "요청 num_ctx"
    value = modelfile_parameters(info).get("num_ctx", "")
    return (int(value), "Modelfile num_ctx") if value.isdigit() else (None, "확인 못 함")


def vector_dims(call: dict) -> list[int]:
    """/api/embed 응답의 벡터 차원 목록."""
    vectors = call["response"].get("embeddings")
    return sorted({len(vector) for vector in vectors if type(vector) is list}) if type(vectors) is list else []


def embedding_models(calls: list[dict]) -> dict[str, list[int]]:
    """임베딩 호출에 쓴 모델 이름과 그 모델이 준 벡터 차원."""
    models = {}
    for call in filter(is_embed, calls):
        dims = models.setdefault(full_name(model_of(call)), [])
        dims += [dim for dim in vector_dims(call) if dim not in dims]
    return models


def check_result(result: object) -> tuple[str, str | None]:
    """14주 채점기가 붙일 status(시간 제외)와 사유. 워커처럼 JSON으로 한 번 바꿨다 읽은 값을 검사하므로
    튜플은 리스트가 되고, JSON으로 바꿀 수 없는 값은 워커 오류(error)가 된다."""
    if isinstance(result, BaseException):
        return "error", f"{type(result).__name__}: {cut(result)}"
    try:
        sent = json.loads(json.dumps(result, allow_nan=False))
    except (TypeError, ValueError) as exc:
        return "error", f"JSON으로 바꿀 수 없음: {exc}"
    try:
        validate_response(sent)
    except (TypeError, ValueError) as exc:
        return "invalid_response", str(exc)
    return "ok", None


# ---------- 출력 구역 ----------

def describe_calls(calls: list[dict]) -> list[str]:
    lines = ["[1] 호출 목록"]
    if not calls:
        return lines + ["  잡힌 호출이 없습니다. 봇이 모델을 부르지 않았거나 urllib.request가 아닌 방법(requests, "
                        "ollama 패키지, LangChain 등)으로 요청했습니다. 그런 요청은 이 도구로 볼 수 없습니다."]
    for number, call in enumerate(calls, 1):
        outcome = f"HTTP {call['status']}" if call["status"] is not None else call["error"] or "응답 없음"
        took = f", {call['seconds']:.2f}초" if call["seconds"] is not None else ""
        lines.append(f"  {number}. {call['path']} model={model_of(call)} → {outcome}{took}")
        if call["status"] is not None and call["status"] >= 400:
            lines.append(f"     오류 본문: {cut(error_text(call))}")
    return lines


def describe_prompt(request: dict) -> list[str]:
    """보낸 messages의 역할과 글자 수. SHOW_PROMPT면 전문도 보인다."""
    messages = request.get("messages") if type(request.get("messages")) is list else []
    items = [(str(item.get("role")), str(item.get("content") or "")) for item in messages if type(item) is dict]
    lines = ["  messages: " + (", ".join(f"{role} {len(text)}자" for role, text in items) or "없음")]
    for role, text in items if SHOW_PROMPT else []:
        lines += [f"    [{role}]"] + [f"      {line}" for line in text.splitlines() or [""]]
    return lines


def thinking_default(info: dict) -> str:
    thinking = info.get("thinking")
    return f", 생각 기본값 {json.dumps(thinking['default'])}" if type(thinking) is dict and "default" in thinking else ""


def describe_model(model: str, info: object, options: dict) -> list[str]:
    """/api/show로 본 모델 정보. 요청이 덮어쓴 Modelfile 값에는 표시를 붙인다."""
    if type(info) is not dict:
        return [f"  모델 정보({model}): 확인 못 함(/api/show 조회 실패)"]
    values = ", ".join(f"{name}={value}" + ("(요청이 덮어씀)" if name in options else "")
                       for name, value in modelfile_parameters(info).items())
    details = info.get("details") if type(info.get("details")) is dict else {}
    return [f"  모델 정보({model}): capabilities {', '.join(info.get('capabilities') or []) or '없음'}"
            + thinking_default(info),
            f"    Modelfile 기본값: {values or '없음'}",
            f"    Modelfile SYSTEM: {cut(info['system']) if info.get('system') else '없음'}",
            f"    양자화 {details.get('quantization_level') or '확인 못 함'}, "
            f"템플릿 출처 {info.get('template_source') or '확인 못 함'}"]


def describe_time(body: dict) -> str:
    """*_duration을 초로 바꾸고 생성 속도(tokens/s)를 계산한다."""
    parts = []
    for label, key in (("전체", "total_duration"), ("적재", "load_duration"),
                       ("입력 처리", "prompt_eval_duration"), ("생성", "eval_duration")):
        value = seconds(body.get(key))
        parts.append(f"{label} {value:.2f}초" if value is not None else f"{label} 없음")
    count, duration = body.get("eval_count"), seconds(body.get("eval_duration"))
    if type(count) is int and duration:
        parts.append(f"생성 속도 {count / duration:.1f} tokens/s")
    return ", ".join(parts)


def describe_reply(call: dict) -> list[str]:
    """응답의 끝난 이유와 토큰 수, 본문과 생각 글, JSON 읽기 결과, 시간."""
    body, (content, thinking) = call["response"], reply_of(call)
    if content is None:
        return [f"  응답: {cut(error_text(call)) or '없음'}"]
    counts = "  ".join(f"{key}={body.get(key, '없음')}" for key in ("done_reason", "prompt_eval_count", "eval_count"))
    lines = [f"  응답: {counts}  thinking {len(thinking)}자",
             f"    content {len(content)}자: {cut(content) if content else '(비었음)'}"]
    if thinking:
        lines.append(f"    thinking: {cut(thinking)}")
    if content.strip():
        value, error, outside = check_content(content)
        if error:
            parsed = f"실패 {error}" + (", 중괄호 밖에 글자 있음" if outside else "")
        else:
            parsed = "성공 " + cut(json.dumps(value, ensure_ascii=False))
        lines.append(f"    코드 펜스 {'있음' if '```' in content else '없음'}, json.loads {parsed}")
    return lines + ["  시간: " + describe_time(body)]


def describe_generation(number: int, total: int, call: dict, info: object, ps: object) -> list[str]:
    request = call["request"]
    sent = "  ".join(f"{key}={cut(json.dumps(request[key], ensure_ascii=False)) if key in request else '없음'}"
                     for key in ("model", "think", "stream", "format", "options"))
    lines = [f"[2] 생성 호출 {number}/{total}: {call['path']}", f"  보낸 설정: {sent}"]
    lines += describe_prompt(request) + describe_model(model_of(call), info, options_of(call))
    context, source = run_context(call, info, ps)
    model_info = info.get("model_info") if type(info) is dict and type(info.get("model_info")) is dict else {}
    maximum = next((value for key, value in model_info.items() if key.endswith(".context_length")), "확인 못 함")
    lines.append(f"  컨텍스트: 실행 {f'{context}({source})' if context else '확인 못 함'}, 모델 최대 {maximum}")
    return lines + describe_reply(call)


def describe_embeddings(calls: list[dict]) -> list[str]:
    lines = ["[3] 임베딩 호출"]
    for number, call in enumerate(filter(is_embed, calls), 1):
        given, vectors = call["request"].get("input"), call["response"].get("embeddings")
        count = len(given) if type(given) is list else "?" if given is None else 1
        if type(vectors) is list and vectors:
            shape = f"벡터 {len(vectors)}개, {'/'.join(map(str, vector_dims(call))) or '?'}차원"
        else:
            shape = cut(error_text(call) or "벡터 없음")
        took = f", {call['seconds']:.2f}초" if call["seconds"] is not None else ""
        lines.append(f"  {number}. model={model_of(call)} 입력 {count}개 → {shape}{took}")
    models = embedding_models(calls)
    if not models:
        return lines + ["  없음"]
    return lines + [f"  사용한 임베딩 모델: {', '.join(models)}" + (" (둘 이상)" if len(models) > 1 else "")]


def describe_ps(ps: object, calls: list[dict]) -> list[str]:
    lines = ["[4] 실행 위치(/api/ps)"]
    if not calls:
        return lines + ["  잡힌 호출이 없어 조회하지 않았습니다."]
    if type(ps) is not dict:
        return lines + ["  확인 못 함(/api/ps 조회 실패)"]
    used = {full_name(model_of(call)) for call in calls}
    for name, percent, entry in ps_rows(ps):
        place = "GPU 비율 확인 못 함"
        if percent is not None:  # 비율이 있으면 size와 size_vram은 정수다.
            vram, size = entry["size_vram"] / 2**30, entry["size"] / 2**30
            place = f"GPU {percent:.1f}%(size_vram {vram:.2f} GiB / size {size:.2f} GiB)"
        context = entry.get("context_length")
        context = f"컨텍스트 {context}" if type(context) is int else "컨텍스트 필드 없음"
        mark = ", 이번 질문에 사용" if full_name(name) in used else ""
        lines.append(f"  {name}: {place}, {context}{mark}")
    return lines if len(lines) > 1 else lines + ["  올라간 모델 없음"]


def describe_result(result: object, elapsed: float, load: float) -> list[str]:
    """반환값 검사와 시간. 채점기는 준비 질문으로 모델 적재 시간을 빼므로 status는 적재를 뺀 시간으로 정한다."""
    status, reason = check_result(result)
    if isinstance(result, BaseException):
        shown, contract = f"예외 {reason}", "검사 못 함(예외)"
    else:
        shown = cut(json.dumps(result, ensure_ascii=False, default=repr))
        contract = "통과" if status == "ok" else f"실패, {reason}"
    took = max(elapsed - load, 0.0)
    status = "timeout" if took > QUESTION_TIMEOUT else status
    note = "점수는 ex04에서 정답과 비교해 매깁니다." if status == "ok" else "채점기에서는 0점입니다."
    return ["[5] 최종 판정", f"  반환값: {shown}", f"  응답 계약(validate_response): {contract}",
            f"  소요 시간: {elapsed:.2f}초(모델 적재 {load:.2f}초 포함)",
            f"  적재를 뺀 시간: {took:.2f}초, 제한 {QUESTION_TIMEOUT}초 {'초과' if took > QUESTION_TIMEOUT else '이내'}."
            " 채점기는 준비 질문으로 적재 시간을 뺍니다.",
            f"  채점기 status: {status}. {note}"]


# ---------- 판정 규칙 ----------

def issue(symptom: str, evidence: str, fix: str) -> str:
    return f"  - {symptom} | 근거: {evidence} | 고칠 곳: {fix}"


def request_fix(text: str) -> tuple[str, str]:
    """HTTP 400·500번대 오류 본문으로 증상과 고칠 곳을 고른다. 두 문구는 Ollama 0.40.17에서 본 것이다."""
    lowered = text.lower()
    if "context size" in lowered or "context length" in lowered:
        return "컨텍스트 부족", "options의 num_ctx를 늘리거나 TOP_K와 문서 길이를 줄이세요."
    if "does not support thinking" in lowered:
        return "생각 모드가 없는 모델에 생각 요청", "요청의 think를 False로 두세요."
    return "요청 오류", "오류 문구가 가리키는 요청 값(think, format, options 등)을 확인하세요."


def generation_problems(call: dict, info: object, ps: object) -> list[str]:
    """/api/chat 호출 하나의 설정과 응답에서 보이는 문제."""
    request, body, options = call["request"], call["response"], options_of(call)
    info = info if type(info) is dict else {}
    parameters = modelfile_parameters(info)
    content, thinking = reply_of(call)
    found = []
    if request.get("think") is None and "thinking" in (info.get("capabilities") or []):
        sent = "null" if "think" in request else "없음"
        found.append(issue("생각 모드를 모델 기본값에 맡김", f"요청 think {sent}, capabilities에 thinking{thinking_default(info)}",
                           "요청 본문에 \"think\": False를 넣으세요."))
    if thinking and request.get("think") is False:
        found.append(issue("think False인데 생각 글이 옴", f"thinking {len(thinking)}자",
                           "ollama show로 모델의 생각 모드 설정을 확인하고 다른 태그나 모델을 쓰세요."))
    elif thinking:
        found.append(issue("응답에 생각 글이 있음", f"thinking {len(thinking)}자, eval_count {body.get('eval_count', '없음')}",
                           "요청의 think를 False로 두세요. 생각 글을 만드는 데도 생성 시간이 듭니다."))
    if content is not None and not content.strip():
        reason = body.get("done_reason", "없음")
        found.append(issue("본문이 비었음", f"content 0자, thinking {len(thinking)}자, done_reason {reason}",
                           "think를 False로 두고, done_reason이 length면 num_predict를 늘리세요."))
    if body.get("done_reason") == "length":
        limit = (f"{options['num_predict']}(요청)" if "num_predict" in options else
                 f"{parameters['num_predict']}(Modelfile)" if "num_predict" in parameters else "없음(Ollama 기본값)")
        found.append(issue("출력이 길이 한도에서 끊김", f"done_reason length, eval_count {body.get('eval_count', '없음')}, "
                           f"num_predict {limit}", "options의 num_predict를 늘리거나 답을 짧게 쓰도록 SYSTEM_PROMPT를 고치세요."))
    context, source = run_context(call, info, ps)
    used = body.get("prompt_eval_count")
    if context and type(used) is int and used >= NEAR_CONTEXT * context:
        found.append(issue("입력이 컨텍스트 한도에 가까움", f"prompt_eval_count {used}, 실행 컨텍스트 {context}({source})",
                           "입력이 조금 더 길어지면 요청이 오류로 끝날 수 있습니다. options의 num_ctx를 늘리거나 "
                           "TOP_K와 문서 길이를 줄이세요."))
    error, outside = None, False
    if content and content.strip():
        _, error, outside = check_content(content)
    if error and "```" in content:
        found.append(issue("코드 펜스", "content에 ``` 있음",
                           "SYSTEM_PROMPT의 'JSON만' 지시를 확인하거나 봇에서 펜스를 벗기는 후처리를 넣으세요."))
    elif error and outside:
        found.append(issue("JSON 밖 글자", "중괄호 안쪽만 떼면 JSON으로 읽힘",
                           "SYSTEM_PROMPT의 'JSON만' 지시를 확인하거나 봇에서 앞뒤 글자를 떼는 후처리를 넣으세요."))
    if error:
        found.append(issue("JSON 파싱 실패", f"json.loads {error}", "SYSTEM_PROMPT의 JSON 형식 지시와 num_predict를 확인하세요."))
    if "temperature" not in options:
        source = (f"Modelfile temperature {parameters['temperature']}" if "temperature" in parameters else
                  "Modelfile에도 없음(Ollama 기본값)" if info else "모델 정보 확인 못 함")
        found.append(issue("온도를 모델 기본값에 맡김", f"요청 options에 temperature 없음, {source}",
                           "options에 \"temperature\": 0을 넣으세요."))
    messages = request.get("messages") if type(request.get("messages")) is list else []
    if info.get("system") and not any(type(item) is dict and item.get("role") == "system" for item in messages):
        found.append(issue("모델에 박힌 시스템 지시 적용", f"요청에 system 메시지 없음, Modelfile SYSTEM '{cut(info['system'])}'",
                           "요청 messages 맨 앞에 system 메시지를 넣거나 SYSTEM 없는 Modelfile로 다시 등록하세요."))
    if request.get("stream") is not False:
        sent = json.dumps(request["stream"]) if "stream" in request else "없음"
        found.append(issue("스트리밍 요청", f"요청 stream {sent}",
                           "요청 본문에 \"stream\": False를 넣으세요. 스트리밍 응답은 JSON 여러 줄로 나뉘어 옵니다."))
    return found


def call_problems(call: dict, info: object, ps: object) -> list[str]:
    """호출 하나에서 보이는 문제. HTTP 오류, 연결 오류, 적재 시간, 생성 설정과 응답을 본다."""
    path, model, status, text = call["path"], model_of(call), call["status"], error_text(call)
    if status == 404 and "model" in text.lower():
        return [issue("모델 없음", f"{path} HTTP 404, model={model}, 오류 '{cut(text)}'",
                      f"봇의 {'EMBED_MODEL' if is_embed(call) else 'MODEL'}을 ollama list에 나오는 이름으로 고치세요.")]
    if status == 404:
        return [issue("주소 없음", f"HTTP 404, 주소 {call['url']}, 오류 '{cut(text)}'",
                      "봇의 Ollama 주소 상수(OLLAMA_URL, CHAT_URL, EMBED_URL)의 경로를 확인하세요.")]
    if status is not None and status >= 400:
        symptom, fix = request_fix(text)
        return [issue(symptom, f"{path} HTTP {status}, 오류 '{cut(text)}'", fix)]
    if status is None and not call["error"]:
        return []  # Ctrl+C 등으로 응답 전에 멈췄다.
    if status is None and "timed out" in call["error"].lower():
        return [issue("요청 시간 초과", f"{path} {call['error']}",
                      "봇의 REQUEST_TIMEOUT과 [4]의 GPU 비율, 생각 모드를 확인하세요.")]
    if status is None:
        return [issue("연결 실패", f"{path} {call['error']}", "Ollama가 실행 중인지, 봇의 주소 상수가 맞는지 확인하세요.")]
    found = []
    load = seconds(call["response"].get("load_duration"))
    if load is not None and load > SLOW_LOAD:
        found.append(issue("모델 새로 적재", f"{path} model={model} load_duration {load:.2f}초",
                           "첫 질문이면 정상입니다(채점기는 준비 질문으로 이 시간을 뺍니다). 둘째 질문부터도 길면 모델이 "
                           "내려갔다 다시 올라간 것이고 채점기도 이 시간을 셉니다. [4]와 ollama ps로 확인하세요."))
    return found + (generation_problems(call, info, ps) if is_chat(call) else [])


def place_problems(calls: list[dict], ps: object) -> list[str]:
    """이번 질문에 쓴 모델이 GPU에 다 올라갔는지, 임베딩 모델이 하나인지 본다."""
    found = []
    used = {full_name(model_of(call)) for call in calls}
    for name, percent, _ in ps_rows(ps):
        if full_name(name) in used and percent is not None and percent < 100:
            found.append(issue("모델 일부가 CPU에서 실행됨", f"{name} GPU {percent:.1f}%(size_vram/size)",
                               "다른 모델을 내리거나 num_ctx를 줄이거나 더 작은 모델을 쓰세요. CPU로 내려간 만큼 느려집니다."))
    models = embedding_models(calls)
    if len(models) > 1:
        shown = ", ".join(f"{name} {'/'.join(map(str, dims)) or '?'}차원" for name, dims in models.items())
        found.append(issue("임베딩 모델이 둘 이상", shown, "색인과 질문을 EMBED_MODEL 하나로 임베딩하고 색인을 다시 만드세요."))
    return found


def result_problems(calls: list[dict], result: object, elapsed: float) -> list[str]:
    """봇의 반환값과 적재를 뺀 시간을 14주 채점기 기준으로 본다."""
    found = []
    took = max(elapsed - load_seconds(calls), 0.0)
    if took > QUESTION_TIMEOUT:
        found.append(issue("시간 초과", f"적재를 뺀 시간 {took:.2f}초 > 제한 {QUESTION_TIMEOUT}초",
                           "생각 모드, num_predict, [4]의 GPU 비율을 확인하세요. 채점기에서는 timeout 0점입니다."))
    status, reason = check_result(result)
    if isinstance(result, BaseException):
        found.append(issue("봇이 예외로 끝남", reason,
                           "위 호출 오류와 봇의 응답 처리 코드를 확인하세요. 채점기에서는 error 0점입니다."))
    elif status == "error":
        found.append(issue("JSON으로 보낼 수 없는 반환값", reason,
                           "사전·리스트·문자열·참거짓만 담아 반환하게 봇을 고치세요. 채점기에서는 error 0점입니다."))
    elif status == "invalid_response":
        found.append(issue("응답 계약 실패", reason, "answers, sources, abstain 세 키만 있는 사전을 반환하게 "
                           "봇을 고치세요. 채점기에서는 invalid_response 0점입니다."))
    return found


def diagnose(calls: list[dict], show_info: dict, ps_info: object, result: object, elapsed: float) -> list[str]:
    """의심되는 문제를 '증상 | 근거 | 고칠 곳' 한 줄씩 돌려준다. Ollama 없이 시험할 수 있는 순수 함수다."""
    found = []
    for call in calls:
        found += call_problems(call, show_info.get(model_of(call)), ps_info)
    return found + place_problems(calls, ps_info) + result_problems(calls, result, elapsed)


def notes(calls: list[dict], show_info: dict) -> list[str]:
    """문제로 판정하지 않는 참고 줄. 요청 options가 덮어쓰지 않아 Modelfile 값이 그대로 쓰이는 PARAMETER다.
    temperature는 '온도를 모델 기본값에 맡김' 규칙이 따로 본다."""
    lines = []
    for call in filter(is_chat, calls):
        rest = [f"{name}={value}" for name, value in modelfile_parameters(show_info.get(model_of(call))).items()
                if name not in options_of(call) and name != "temperature"]
        line = (f"  참고: 요청이 덮어쓰지 않은 Modelfile 값 | {model_of(call)} {', '.join(rest)} | "
                "영향이 의심되면 options에 같은 이름으로 값을 넣어 ex04로 비교하세요.")
        if rest and line not in lines:
            lines.append(line)
    return lines


def report(calls: list[dict], show_info: dict, ps_info: object, result: object, elapsed: float) -> list[str]:
    """질문 하나의 여섯 구역 출력 줄. [6]은 문제 줄 다음에 참고 줄을 붙인다."""
    lines = describe_calls(calls)
    chats = list(filter(is_chat, calls))
    for number, call in enumerate(chats, 1):
        lines += describe_generation(number, len(chats), call, show_info.get(model_of(call)), ps_info)
    if not chats:
        lines.append("[2] 생성 호출(/api/chat): 없음")
    lines += describe_embeddings(calls) + describe_ps(ps_info, calls) + describe_result(result, elapsed, load_seconds(calls))
    problems = diagnose(calls, show_info, ps_info, result, elapsed)
    lines += ["[6] 의심되는 문제와 고칠 곳"] + (problems or [
        "  찾은 문제가 없습니다. 답의 내용이 틀렸다면 검색된 문서(ex05)와 SYSTEM_PROMPT를 확인하세요."])
    return lines + notes(calls, show_info)


def main() -> None:
    configure_utf8()
    try:
        bot = importlib.import_module(BOT)
    except Exception as exc:
        print(f"봇 모듈을 불러오지 못했습니다(BOT={BOT}): {type(exc).__name__}: {exc}")
        return
    shown = {}  # 모델 이름 → /api/show 결과. 모델마다 한 번만 조회한다.
    print(f"추론 점검: 봇의 answer(question)이 보내는 요청과 받은 응답을 보여 줍니다(BOT={BOT}).")
    print("질문을 입력하세요. 빈 입력은 건너뛰고 /bye 또는 Ctrl+C로 종료합니다.")
    print("봇 파일을 고쳤다면 /bye로 종료한 뒤 다시 실행하세요. 실행 중에는 고친 내용을 다시 읽지 않습니다.")
    while True:
        try:
            question = input("\n질문> ").strip()
            if question == "/bye":
                break
            if not question:
                continue
            if len(question) > MAX_QUESTION_LENGTH:
                print(f"질문은 {MAX_QUESTION_LENGTH}자 이내로 입력하세요.")
                continue
            calls, result, elapsed = ask(bot, question)
            ps = look_up(calls, shown)
            print("\n".join(report(calls, shown, ps, result, elapsed)), flush=True)
        except (EOFError, KeyboardInterrupt):
            print("\n점검 종료")
            break
