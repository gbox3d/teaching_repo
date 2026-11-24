"""ex07 추론 점검 시험. Ollama 없이 돈다.
127.0.0.1 임의 포트에 가짜 Ollama 서버를 띄우고, 임시 폴더의 가짜 봇이 그 서버로 urllib 요청을 보낸다."""

import contextlib
import importlib
import io
import json
import socket
import sys
import tempfile
import threading
import unittest
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from unittest import mock
from urllib.error import HTTPError

import ex07_inspect as ex07

QUESTION = "원광대학교를 상징하는 새는 무엇인가요?"
GOOD_CONTENT = '{"answers": ["봉황"], "sources": ["wku-symbols"], "abstain": false}'
GOOD_RESULT = {"answers": ["봉황"], "sources": ["wku-symbols"], "abstain": False}
BOT_NAME = "fake_ex07_bot"

# /api/show·/api/ps 응답의 모양은 Ollama 0.40.17에서 조회한 필드를 따른다.
THINKING_SHOW = {
    "capabilities": ["completion", "tools", "thinking"],
    "thinking": {"values": [False, True], "default": True},
    "parameters": "presence_penalty               1.5\ntemperature                    1\ntop_k                          20",
    "details": {"quantization_level": "Q8_0"},
    "model_info": {"fake.context_length": 262144},
    "template_source": "renderer_parser",
}
CLEAN_SHOW = {
    "capabilities": ["completion"],
    "parameters": "num_predict                    512\ntemperature                    0",
    "details": {"quantization_level": "F16"},
    "model_info": {"fake.context_length": 32768},
    "template_source": "gguf_chat_template",
}
CLEAN_PS = {"models": [{"name": "fake-chat:latest", "model": "fake-chat:latest", "size": 1000, "size_vram": 1000,
                        "context_length": 4096}]}

BOT_SOURCE = '''"""시험용 가짜 봇. 가짜 서버에 urllib로 요청한다."""
import json
from urllib.error import HTTPError
from urllib.request import ProxyHandler, Request, build_opener

BASE = "__BASE__"
MODEL = "fake-chat"
EMBED_MODELS = []  # 질문마다 이 모델들로 임베딩을 먼저 부른다.
CHANGES = {}  # 생성 요청 본문에 덮어쓸 값
DROP = ()  # 생성 요청 본문에서 뺄 키
FAIL_AFTER_CHAT = False
received = []  # 봇이 받은 응답 본문(바이트). 오류 본문도 담는다.


def post(path, body):
    request = Request(BASE + path, data=json.dumps(body, ensure_ascii=False).encode("utf-8"),
                      headers={"Content-Type": "application/json"}, method="POST")
    try:
        with build_opener(ProxyHandler({})).open(request, timeout=10) as response:
            raw = response.read()
    except HTTPError as exc:
        received.append(exc.read())
        raise
    received.append(raw)
    return json.loads(raw)


def answer(question):
    for model in EMBED_MODELS:
        post("/api/embed", {"model": model, "input": [question]})
    request = {
        "model": MODEL, "stream": False, "think": False,
        "messages": [{"role": "system", "content": "JSON으로만 답한다."}, {"role": "user", "content": question}],
        "options": {"temperature": 0, "num_predict": 512},
    }
    request.update(CHANGES)
    for key in DROP:
        del request[key]
    body = post("/api/chat", request)
    if FAIL_AFTER_CHAT:
        raise RuntimeError("시험용 오류")
    return json.loads(body["message"]["content"])
'''


def chat_reply(content: str = GOOD_CONTENT, thinking: str | None = None, **changes) -> dict:
    message = {"role": "assistant", "content": content}
    if thinking is not None:
        message["thinking"] = thinking
    body = {"model": "fake-chat", "message": message, "done": True, "done_reason": "stop",
            "total_duration": 2_000_000_000, "load_duration": 50_000_000, "prompt_eval_count": 800,
            "prompt_eval_duration": 300_000_000, "eval_count": 40, "eval_duration": 1_000_000_000}
    body.update(changes)
    return body


def chat_request(drop: tuple = (), **changes) -> dict:
    request = {"model": "fake-chat", "stream": False, "think": False,
               "messages": [{"role": "system", "content": "JSON으로만 답한다."}, {"role": "user", "content": QUESTION}],
               "options": {"temperature": 0, "num_predict": 512}}
    request.update(changes)
    for key in drop:
        del request[key]
    return request


def record(path: str = "/api/chat", request: dict | None = None, response: object = None, status: int | None = 200,
           error: str | None = None) -> dict:
    """ask()가 남기는 호출 기록과 같은 모양. response가 글이면 JSON 객체가 아닌 본문이다."""
    if response is None and status == 200:
        response = chat_reply()
    text = response if type(response) is str else json.dumps(response, ensure_ascii=False) if response else ""
    return {"url": "http://127.0.0.1:11434" + path, "path": path,
            "request": chat_request() if request is None else request,
            "status": status, "response": response if type(response) is dict else {}, "text": text,
            "error": error, "seconds": 0.5}


def embed_record(model: str, dims: int) -> dict:
    return record("/api/embed", {"model": model, "input": [QUESTION]},
                  {"model": model, "embeddings": [[0.1] * dims], "load_duration": 1_000_000})


class FakeOllama(BaseHTTPRequestHandler):
    """가짜 Ollama. 받은 요청은 server.seen에, 보낸 본문은 server.sent에 남긴다."""

    def log_message(self, *args):
        pass

    def send(self, status: int, payload: object) -> None:
        raw = payload if type(payload) is bytes else json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.server.sent.append(raw)
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def broken(self) -> bool:
        """server.broken이면 진단 조회에 HTTP가 아닌 한 줄을 보낸다."""
        if self.server.broken and self.path in ("/api/show", "/api/ps"):
            self.wfile.write(b"NOT-HTTP\r\n")
            return True
        return False

    def do_GET(self):
        self.server.seen.append((self.path, None))
        if self.broken():
            return
        if self.path == "/api/ps":
            self.send(200, self.server.ps)
        else:
            self.send(404, b"404 page not found")

    def do_POST(self):
        body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        self.server.seen.append((self.path, body))
        model = body.get("model")
        if self.broken():
            return
        if self.path == "/api/chat" and model in self.server.chat and body.get("stream", True) is not False:
            # Ollama처럼 stream을 false로 보내지 않으면 한 줄에 JSON 하나씩 나눠 보낸다.
            reply = self.server.chat[model]
            first = {"model": model, "message": {"role": "assistant", "content": reply["message"]["content"][:5]}}
            last = dict(reply, message={"role": "assistant", "content": reply["message"]["content"][5:]})
            self.send(200, (json.dumps(first) + "\n" + json.dumps(last) + "\n").encode("utf-8"))
        elif self.path == "/api/chat" and model in self.server.chat:
            self.send(200, self.server.chat[model])
        elif self.path == "/api/embed" and model in self.server.dims:
            vectors = [[0.5] * self.server.dims[model] for _ in body["input"]]
            self.send(200, {"model": model, "embeddings": vectors, "load_duration": 1_000_000})
        elif self.path == "/api/show" and model in self.server.shows:
            self.send(200, self.server.shows[model])
        elif self.path in ("/api/chat", "/api/embed", "/api/show"):
            self.send(404, {"error": f"model '{model}' not found"})
        else:
            self.send(404, b"404 page not found")


class FakeServerTest(unittest.TestCase):
    """가짜 서버와 가짜 봇으로 가로채기·조회·대화 반복을 확인한다."""

    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), FakeOllama)
        cls.server.daemon_threads = True
        cls.base = f"http://127.0.0.1:{cls.server.server_address[1]}"
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.folder = tempfile.TemporaryDirectory()
        Path(cls.folder.name, BOT_NAME + ".py").write_text(BOT_SOURCE.replace("__BASE__", cls.base), encoding="utf-8")
        sys.path.insert(0, cls.folder.name)

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        sys.path.remove(cls.folder.name)
        sys.modules.pop(BOT_NAME, None)
        cls.folder.cleanup()

    def setUp(self):
        self.server.seen, self.server.sent, self.server.broken = [], [], False
        self.server.chat = {"fake-chat": chat_reply()}
        self.server.dims = {"bge-m3": 4, "other-embed": 3}
        self.server.shows = {"fake-chat": THINKING_SHOW}
        self.server.ps = CLEAN_PS
        sys.modules.pop(BOT_NAME, None)  # 시험마다 봇의 전역 값을 새로 시작한다.
        self.bot = importlib.import_module(BOT_NAME)
        self.original = urllib.request.OpenerDirector.open

    def assertRestored(self):
        self.assertIs(urllib.request.OpenerDirector.open, self.original)

    def inspect(self) -> str:
        """main()이 질문 하나에 하는 일(ask, look_up, report)을 하고 출력 글을 돌려준다."""
        calls, result, elapsed = ex07.ask(self.bot, QUESTION)
        shown = {}
        return "\n".join(ex07.report(calls, shown, ex07.look_up(calls, shown), result, elapsed))

    def test_capture_records_request_and_response(self):
        calls, result, elapsed = ex07.ask(self.bot, QUESTION)
        self.assertRestored()
        self.assertEqual(result, GOOD_RESULT)
        self.assertEqual(len(calls), 1)
        call = calls[0]
        self.assertEqual((call["url"], call["path"]), (self.base + "/api/chat", "/api/chat"))
        self.assertEqual(call["request"], self.server.seen[0][1])
        self.assertEqual(call["status"], 200)
        self.assertEqual(call["response"], json.loads(self.server.sent[0]))
        self.assertEqual(call["text"], self.server.sent[0].decode("utf-8"))
        self.assertIsNone(call["error"])
        self.assertGreaterEqual(elapsed, call["seconds"])

    def test_bot_receives_same_bytes(self):
        self.bot.EMBED_MODELS = ["bge-m3"]
        calls, result, _ = ex07.ask(self.bot, QUESTION)
        self.assertEqual(result, GOOD_RESULT)
        self.assertEqual(self.bot.received, self.server.sent)
        self.assertEqual([call["path"] for call in calls], ["/api/embed", "/api/chat"])

    def test_http_error_is_recorded_and_raised_again(self):
        self.bot.MODEL = "missing-model"
        calls, result, _ = ex07.ask(self.bot, QUESTION)
        self.assertRestored()
        self.assertIsInstance(result, HTTPError)
        self.assertEqual(result.code, 404)
        self.assertEqual(calls[0]["status"], 404)
        self.assertEqual(calls[0]["response"], {"error": "model 'missing-model' not found"})
        self.assertEqual(self.bot.received, self.server.sent)  # 봇도 같은 오류 본문을 읽었다.
        text = "\n".join(ex07.diagnose(calls, {}, None, result, 0.1))
        self.assertIn("모델 없음", text)
        self.assertIn("봇의 MODEL을 ollama list", text)
        self.assertIn("봇이 예외로 끝남", text)

    def test_open_restored_after_bot_exception(self):
        self.bot.FAIL_AFTER_CHAT = True
        calls, result, _ = ex07.ask(self.bot, QUESTION)
        self.assertRestored()
        self.assertIsInstance(result, RuntimeError)
        self.assertEqual(calls[0]["status"], 200)

    def test_open_restored_after_ctrl_c(self):
        with mock.patch.object(self.bot, "answer", side_effect=KeyboardInterrupt):
            with self.assertRaises(KeyboardInterrupt):
                ex07.ask(self.bot, QUESTION)
        self.assertRestored()

    def test_connection_failure(self):
        probe = socket.socket()
        probe.bind(("127.0.0.1", 0))
        port = probe.getsockname()[1]
        probe.close()  # 아무도 듣지 않는 포트
        self.bot.BASE = f"http://127.0.0.1:{port}"
        calls, result, _ = ex07.ask(self.bot, QUESTION)
        self.assertRestored()
        self.assertIsNone(calls[0]["status"])
        self.assertTrue(calls[0]["error"])
        self.assertIn("연결 실패", "\n".join(ex07.diagnose(calls, {}, None, result, 0.1)))
        self.assertIsNone(ex07.look_up(calls, {}))  # 진단 조회도 실패하면 None이다.

    def test_look_up_asks_show_once_per_model(self):
        shown = {}
        for _ in range(2):
            calls, _, _ = ex07.ask(self.bot, QUESTION)
            ps = ex07.look_up(calls, shown)
        self.assertRestored()
        self.assertEqual([path for path, _ in self.server.seen].count("/api/show"), 1)
        self.assertEqual([path for path, _ in self.server.seen].count("/api/ps"), 2)
        self.assertEqual(shown["fake-chat"]["template_source"], "renderer_parser")
        self.assertEqual(ps, CLEAN_PS)
        self.assertEqual(len(calls), 1)  # 진단 조회는 호출 기록에 들어가지 않는다.

    def test_look_up_survives_non_http_reply(self):
        self.server.broken = True  # /api/show·/api/ps가 HTTP가 아닌 줄을 보내면 http.client가 BadStatusLine을 낸다.
        text = self.inspect()
        self.assertIn("모델 정보(fake-chat): 확인 못 함(/api/show 조회 실패)", text)
        self.assertIn("확인 못 함(/api/ps 조회 실패)", text)
        self.assertIn("채점기 status: ok", text)

    def test_streaming_request(self):
        self.bot.DROP = ("stream",)
        calls, result, elapsed = ex07.ask(self.bot, QUESTION)
        self.assertIsInstance(result, json.JSONDecodeError)  # 봇이 여러 줄 응답을 JSON 하나로 읽다가 실패했다.
        self.assertEqual(calls[0]["response"], {})
        self.assertEqual(calls[0]["text"].count("\n"), 2)
        text = "\n".join(ex07.report(calls, {"fake-chat": CLEAN_SHOW}, CLEAN_PS, result, elapsed))
        self.assertIn("스트리밍 요청 | 근거: 요청 stream 없음", text)
        self.assertIn("봇이 예외로 끝남 | 근거: JSONDecodeError", text)
        self.assertIn("채점기 status: error", text)

    def test_report_has_six_sections(self):
        self.bot.EMBED_MODELS = ["bge-m3", "other-embed"]
        text = self.inspect()
        for header in ("[1] 호출 목록", "[2] 생성 호출 1/1: /api/chat", "[3] 임베딩 호출", "[4] 실행 위치",
                       "[5] 최종 판정", "[6] 의심되는 문제와 고칠 곳"):
            self.assertIn(header, text)
        self.assertIn("[system]", text)  # SHOW_PROMPT가 True면 messages 전문을 보인다.
        self.assertIn("presence_penalty=1.5", text)
        self.assertIn("temperature=1(요청이 덮어씀)", text)
        self.assertIn("컨텍스트: 실행 4096(/api/ps), 모델 최대 262144", text)
        self.assertIn("1. model=bge-m3 입력 1개 → 벡터 1개, 4차원", text)
        self.assertIn("fake-chat:latest: GPU 100.0%", text)
        self.assertIn("임베딩 모델이 둘 이상", text)
        self.assertIn("채점기 status: ok", text)

    def test_notes_follow_no_problem_line(self):
        lines = self.inspect().splitlines()
        section = lines[lines.index("[6] 의심되는 문제와 고칠 곳") + 1:]
        self.assertTrue(section[0].startswith("  찾은 문제가 없습니다."))
        self.assertEqual(section[1:], ["  참고: 요청이 덮어쓰지 않은 Modelfile 값 | fake-chat presence_penalty=1.5, "
                                       "top_k=20 | 영향이 의심되면 options에 같은 이름으로 값을 넣어 ex04로 비교하세요."])

    def test_main_skips_empty_input_and_ends_with_bye(self):
        typed = iter(["", QUESTION, "/bye"])
        output = io.StringIO()
        with mock.patch.object(ex07, "BOT", BOT_NAME), \
                mock.patch("builtins.input", side_effect=lambda prompt="": next(typed)) as asked, \
                contextlib.redirect_stdout(output):
            ex07.main()
        self.assertRestored()
        self.assertEqual(asked.call_count, 3)
        self.assertEqual([path for path, _ in self.server.seen].count("/api/chat"), 1)
        self.assertIn("[6] 의심되는 문제와 고칠 곳", output.getvalue())

    def test_main_ends_on_ctrl_c(self):
        output = io.StringIO()
        with mock.patch.object(ex07, "BOT", BOT_NAME), mock.patch("builtins.input", side_effect=KeyboardInterrupt), \
                contextlib.redirect_stdout(output):
            ex07.main()
        self.assertIn("점검 종료", output.getvalue())


class RuleTest(unittest.TestCase):
    """판정 규칙은 호출 기록만으로 시험한다."""

    def problems(self, calls, show=CLEAN_SHOW, ps=CLEAN_PS, result=None, elapsed=1.0) -> str:
        result = GOOD_RESULT if result is None else result
        return "\n".join(ex07.diagnose(calls, {"fake-chat": show}, ps, result, elapsed))

    def report(self, calls, show=CLEAN_SHOW, ps=CLEAN_PS, result=None, elapsed=1.0) -> str:
        result = GOOD_RESULT if result is None else result
        return "\n".join(ex07.report(calls, {"fake-chat": show}, ps, result, elapsed))

    def test_clean_call_has_no_problem(self):
        self.assertEqual(ex07.diagnose([record()], {"fake-chat": CLEAN_SHOW}, CLEAN_PS, GOOD_RESULT, 1.0), [])
        self.assertIn("찾은 문제가 없습니다.", self.report([record()]))
        self.assertNotIn("참고:", self.report([record()]))

    def test_missing_model_404(self):
        call = record(request={"model": "qwen3.5-2b"}, response={"error": "model 'qwen3.5-2b' not found"}, status=404)
        text = self.problems([call], result=HTTPError("http://127.0.0.1", 404, "Not Found", {}, None))
        self.assertIn("모델 없음", text)
        self.assertIn("model=qwen3.5-2b", text)
        self.assertIn("ollama list", text)

    def test_missing_embedding_model_points_to_embed_model(self):
        call = record("/api/embed", {"model": "nomic"}, {"error": "model 'nomic' not found"}, status=404)
        self.assertIn("봇의 EMBED_MODEL을", self.problems([call]))

    def test_wrong_path_404(self):
        call = record("/api/chats", response="404 page not found", status=404)
        self.assertIn("주소 없음", self.problems([call]))

    def test_context_overflow_400(self):
        error = {"error": "request (870 tokens) exceeds the available context size (512 tokens)"}
        text = self.problems([record(response=error, status=400)])
        self.assertIn("컨텍스트 부족 | 근거: /api/chat HTTP 400", text)
        self.assertIn("num_ctx를 늘리거나 TOP_K와 문서 길이를 줄이세요", text)

    def test_think_on_model_without_thinking_400(self):
        text = self.problems([record(response={"error": '"wku-lora" does not support thinking'}, status=400)])
        self.assertIn("생각 모드가 없는 모델에 생각 요청", text)
        self.assertIn("think를 False로", text)

    def test_other_request_error(self):
        self.assertIn("요청 오류 | 근거: /api/chat HTTP 500", self.problems([record(response={"error": "boom"}, status=500)]))

    def test_thinking_model_without_think(self):
        text = self.problems([record(request=chat_request(drop=("think",)))], show=THINKING_SHOW)
        self.assertIn("생각 모드를 모델 기본값에 맡김 | 근거: 요청 think 없음", text)
        self.assertIn("생각 기본값 true", text)

    def test_thinking_model_with_null_think(self):
        text = self.problems([record(request=chat_request(think=None))], show=THINKING_SHOW)
        self.assertIn("생각 모드를 모델 기본값에 맡김 | 근거: 요청 think null", text)

    def test_thinking_in_reply(self):
        text = self.problems([record(request=chat_request(think=True), response=chat_reply(thinking="문서를 본다"))])
        self.assertIn("응답에 생각 글이 있음", text)
        self.assertIn("thinking 6자", text)

    def test_empty_content_with_thinking(self):
        call = record(response=chat_reply(content="", thinking="먼저 문서를 읽는다", done_reason="length"))
        text = self.problems([call], result="")
        self.assertIn("본문이 비었음", text)
        self.assertIn("think False인데 생각 글이 옴", text)
        self.assertIn("출력이 길이 한도에서 끊김", text)

    def test_done_reason_length(self):
        call = record(response=chat_reply(content='{"answers": ["봉', done_reason="length", eval_count=512))
        text = self.problems([call], result='{"answers": ["봉')
        self.assertIn("출력이 길이 한도에서 끊김", text)
        self.assertIn("num_predict 512(요청)", text)
        self.assertIn("JSON 파싱 실패", text)

    def test_code_fence(self):
        content = "```json\n" + GOOD_CONTENT + "\n```"
        text = self.problems([record(response=chat_reply(content=content))], result=content)
        self.assertIn("코드 펜스", text)
        self.assertIn("JSON 파싱 실패", text)
        self.assertIn("응답 계약 실패", text)

    def test_text_outside_json(self):
        content = "다음과 같습니다. " + GOOD_CONTENT
        text = self.problems([record(response=chat_reply(content=content))], result=content)
        self.assertIn("JSON 밖 글자", text)
        self.assertNotIn("코드 펜스", text)

    def test_missing_temperature_uses_modelfile_value(self):
        request = chat_request(options={"num_predict": 512})
        text = self.problems([record(request=request)], show=THINKING_SHOW)
        self.assertIn("온도를 모델 기본값에 맡김", text)
        self.assertIn("Modelfile temperature 1", text)

    def test_modelfile_system_is_inherited(self):
        request = chat_request(messages=[{"role": "user", "content": QUESTION}])
        show = dict(CLEAN_SHOW, system="당신은 그리스·로마 신화를 소개하는 안내자입니다.")
        text = self.problems([record(request=request)], show=show)
        self.assertIn("모델에 박힌 시스템 지시 적용", text)
        self.assertIn("그리스·로마", text)

    def test_modelfile_values_are_notes_not_problems(self):
        self.assertEqual(ex07.diagnose([record()], {"fake-chat": THINKING_SHOW}, CLEAN_PS, GOOD_RESULT, 1.0), [])
        notes = ex07.notes([record(), record()], {"fake-chat": THINKING_SHOW})
        self.assertEqual(len(notes), 1)  # 같은 모델의 호출이 여러 번이어도 한 줄만 보인다.
        self.assertIn("| fake-chat presence_penalty=1.5, top_k=20 |", notes[0])
        self.assertNotIn("temperature", notes[0])  # 요청이 덮어썼다.

    def test_mixed_embedding_models(self):
        text = self.problems([embed_record("bge-m3", 1024), embed_record("other-embed", 768), record()])
        self.assertIn("임베딩 모델이 둘 이상", text)
        self.assertIn("bge-m3:latest 1024차원, other-embed:latest 768차원", text)

    def test_same_embedding_model_with_and_without_tag(self):
        self.assertNotIn("임베딩 모델이 둘 이상", self.problems([embed_record("bge-m3", 4), embed_record("bge-m3:latest", 4)]))

    def test_timeout_counts_time_without_load(self):
        text = self.problems([record()], elapsed=31.0)  # 적재 0.05초
        self.assertIn("시간 초과 | 근거: 적재를 뺀 시간 30.95초 > 제한 30초", text)
        self.assertIn("채점기 status: timeout", self.report([record()], elapsed=31.0))

    def test_first_question_load_is_left_out(self):
        call = record(response=chat_reply(load_duration=30_000_000_000))
        self.assertNotIn("시간 초과", self.problems([call], elapsed=35.0))
        text = self.report([call], elapsed=35.0)
        self.assertIn("소요 시간: 35.00초(모델 적재 30.00초 포함)", text)
        self.assertIn("적재를 뺀 시간: 5.00초, 제한 30초 이내. 채점기는 준비 질문으로 적재 시간을 뺍니다.", text)
        self.assertIn("채점기 status: ok", text)
        self.assertIn("모델 새로 적재", text)
        clamped = self.report([record(response=chat_reply(load_duration=2_000_000_000))], elapsed=1.0)
        self.assertIn("적재를 뺀 시간: 0.00초", clamped)  # 보고된 적재가 잰 시간보다 길어도 음수로 보이지 않는다.

    def test_near_context_from_ps(self):
        text = self.problems([record(response=chat_reply(prompt_eval_count=4000))])
        self.assertIn("입력이 컨텍스트 한도에 가까움 | 근거: prompt_eval_count 4000, 실행 컨텍스트 4096(/api/ps)", text)

    def test_near_context_from_request_num_ctx(self):
        # /api/ps에 이 모델의 컨텍스트 길이가 없을 때만 요청의 num_ctx를 쓴다.
        ps = {"models": [{key: value for key, value in CLEAN_PS["models"][0].items() if key != "context_length"}]}
        request = chat_request(options={"temperature": 0, "num_predict": 512, "num_ctx": 512})
        text = self.problems([record(request=request, response=chat_reply(prompt_eval_count=500))], ps=ps)
        self.assertIn("실행 컨텍스트 512(요청 num_ctx)", text)

    def test_ps_context_before_request_num_ctx(self):
        # /api/ps의 길이가 있으면 요청의 num_ctx보다 먼저 쓴다.
        request = chat_request(options={"temperature": 0, "num_predict": 512, "num_ctx": 270})
        calls = [record(request=request, response=chat_reply(prompt_eval_count=260))]
        self.assertNotIn("입력이 컨텍스트 한도에 가까움", self.problems(calls))
        self.assertIn("컨텍스트: 실행 4096(/api/ps)", self.report(calls))

    def test_partial_gpu(self):
        ps = {"models": [dict(CLEAN_PS["models"][0], size_vram=600)]}
        self.assertIn("모델 일부가 CPU에서 실행됨 | 근거: fake-chat:latest GPU 60.0%", self.problems([record()], ps=ps))

    def test_slow_load(self):
        self.assertIn("모델 새로 적재", self.problems([record(response=chat_reply(load_duration=6_000_000_000))]))

    def test_stream_request(self):
        self.assertIn("스트리밍 요청 | 근거: 요청 stream true", self.problems([record(request=chat_request(stream=True))]))

    def test_contract_checks_value_after_json(self):
        as_tuple = {"answers": ("봉황",), "sources": ["wku-symbols"], "abstain": False}
        self.assertEqual(ex07.check_result(as_tuple), ("ok", None))  # 워커를 거치면 튜플은 리스트가 된다.
        self.assertNotIn("응답 계약 실패", self.problems([record()], result=as_tuple))
        status, reason = ex07.check_result({"answers": {"봉황"}, "sources": [], "abstain": False})
        self.assertEqual(status, "error")
        self.assertIn("JSON으로 바꿀 수 없음", reason)
        self.assertIn("JSON으로 보낼 수 없는 반환값", self.problems([record()], result={"answers": {"봉황"}}))

    def test_contract_failure_and_status(self):
        wrong = {"answers": ["봉황"], "sources": ["wku-symbols"], "abstain": "false"}
        self.assertIn("응답 계약 실패", self.problems([record()], result=wrong))
        self.assertEqual(ex07.check_result(wrong)[0], "invalid_response")
        self.assertEqual(ex07.check_result(RuntimeError("x"))[0], "error")
        self.assertEqual(ex07.check_result(GOOD_RESULT)[0], "ok")
        self.assertIn("채점기 status: invalid_response. 채점기에서는 0점입니다.", self.report([record()], result=wrong))

    def test_no_calls_notice(self):
        text = "\n".join(ex07.describe_calls([]))
        self.assertIn("잡힌 호출이 없습니다", text)
        self.assertIn("requests, ollama 패키지, LangChain", text)
        self.assertIn("잡힌 호출이 없어 조회하지 않았습니다", "\n".join(ex07.describe_ps(None, [])))

    def test_generate_call_is_only_listed(self):
        call = record("/api/generate", {"model": "fake-chat", "prompt": QUESTION}, {"response": GOOD_CONTENT})
        text = self.report([call])
        self.assertIn("1. /api/generate model=fake-chat → HTTP 200", text)
        self.assertIn("[2] 생성 호출(/api/chat): 없음", text)

    def test_show_prompt_off(self):
        with mock.patch.object(ex07, "SHOW_PROMPT", False):
            self.assertEqual(ex07.describe_prompt(chat_request()), ["  messages: system 12자, user 21자"])

    def test_preview_cuts_long_text(self):
        self.assertEqual(ex07.cut("가\n나"), "가\\n나")  # 줄바꿈은 한 줄 안에 \n으로 보인다.
        with mock.patch.object(ex07, "PREVIEW", 5):
            self.assertEqual(ex07.cut("가나다라마바사"), "가나다라마…(+2자)")


if __name__ == "__main__":
    unittest.main()
