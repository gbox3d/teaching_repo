# 추론 버그 잡기

학습과 등록은 끝났는데 챗봇의 답이 이상할 때 원인을 좁히는 안내서다. 모델을 다시 학습하기 전에 봇이 Ollama에 실제로 보낸 요청과 받은 응답부터 본다. 도구는 이 프로젝트의 `ex07` 추론 점검이고, 명령은 모두 `examples/`에서 실행한다. 특강 4교시 실습의 순서와 시간은 [4교시 안내](period4/README.md)를 따른다. 이 문서에는 그때와 과제 기간에 찾아볼 증상 표, 버그 심기 전체, 학습한 모델을 점검하는 순서를 둔다. 학습이 오류 없이 느려지는 문제는 끝의 [학습 중 느려짐과 메모리](#학습-중-느려짐과-메모리)에 따로 적는다.

이 문서의 실측은 기준 PC(Windows 11, RTX 5060 8GB)에서 2026-11-23과 2026-11-24에 Ollama 0.40.17로 확인한 값이다. Ollama가 업데이트되면 오류 문구와 기본값이 달라질 수 있으므로, 결과를 기록할 때 모델 이름과 ID(`ollama list`의 ID)를 함께 적는다.

## ex07 추론 점검

처음 실행하거나 `pyproject.toml`의 명령이 바뀌었으면 먼저 `uv sync`를 실행한다.

```powershell
uv run ex07
```

`질문>`에 질문을 입력하면 [ex07](src/ex07_inspect/__init__.py)이 `BOT`이 가리키는 봇의 `answer(question)`을 한 번 부르고, 그동안 봇이 Ollama에 보낸 요청과 받은 응답을 여섯 구역으로 출력한다. 빈 입력은 건너뛰고 `/bye`나 Ctrl+C로 끝난다. 봇 파일을 고쳤으면 ex07을 끝내고 다시 실행한다. 실행 중에는 처음 불러온 봇 모듈을 계속 쓴다.

바꿔 볼 값은 파일 맨 위의 상수다.

| 상수 | 기본값 | 뜻 |
|---|---|---|
| `BOT` | `"student_bot"` | 점검할 봇 모듈. ex04에서 잰 봇과 같게 둔다. 특강의 임베딩 RAG 봇은 `"rag_bot"` |
| `QUESTION_TIMEOUT` | `30` | 비교할 문항당 제한(초). 14주차 채점기와 같은 값 |
| `SHOW_PROMPT` | `True` | 보낸 messages 전문을 출력한다. `False`면 역할과 글자 수만 출력한다 |
| `PREVIEW` | `300` | 응답 본문처럼 긴 글을 이 글자 수까지만 출력한다 |
| `SLOW_LOAD` | `1.0` | `load_duration`이 이 초보다 길면 '모델 새로 적재'로 판정한다 |
| `NEAR_CONTEXT` | `0.9` | `prompt_eval_count`가 실행 컨텍스트의 이 비율 이상이면 '입력이 컨텍스트 한도에 가까움'으로 판정한다 |

`SLOW_LOAD`와 `NEAR_CONTEXT`는 판정에 쓰려고 정한 기준이며 측정한 값이 아니다.

| 구역 | 내용 |
|---|---|
| [1] 호출 목록 | 봇이 보낸 요청마다 경로, 모델, HTTP 상태, 소요 시간. 오류면 오류 본문 |
| [2] 생성 호출 | `/api/chat`마다 보낸 설정(model, think, stream, format, options), messages, 모델 정보, 컨텍스트, 응답(done_reason, prompt_eval_count, eval_count, thinking, content, JSON 읽기 결과), 시간 |
| [3] 임베딩 호출 | `/api/embed`마다 모델, 입력 수, 벡터 수와 차원. 이번 질문에 사용한 임베딩 모델 목록 |
| [4] 실행 위치 | `/api/ps`의 모델별 GPU 적재 비율(size_vram/size), 크기, context_length |
| [5] 최종 판정 | 반환값, 응답 계약(`validate_response`) 결과, 소요 시간과 그중 모델 적재 시간, 적재를 뺀 시간과 제한, 14주차 채점기가 붙일 status |
| [6] 의심되는 문제와 고칠 곳 | 한 줄에 증상, 근거 값, 고칠 곳. 문제가 없으면 '찾은 문제가 없습니다'. 맨 아래 '참고' 줄은 문제로 판정하지 않은 정보 |

[5]는 14주차 채점기의 판정을 따른다. 채점 워커는 봇의 반환값을 JSON으로 바꿔 채점기에 보내므로, ex07도 반환값을 JSON으로 한 번 바꿨다가 다시 읽은 값으로 응답 계약을 검사한다. 튜플은 리스트로 바뀌어 통과하고, 집합처럼 JSON으로 바꿀 수 없는 값은 워커 오류라 status가 `error`다.

[5]의 status는 모델 적재를 뺀 시간으로 정한다. 채점기는 워커를 시작할 때마다 준비 질문을 한 번 보내 모델을 올리고, 그 시간을 점수와 문항별 시간에서 뺀다([평가 명세](../../../weeks/week14_chatbot_project/evaluation_spec.md#실행과-시간)). ex07에는 준비 질문이 없어 첫 질문의 소요 시간에 모델 적재가 들어가므로 두 시간을 함께 보인다. rag_bot은 첫 질문 때 문서 색인도 만든다. 질문 사이에 오래 쉬지 않았는데도 둘째 질문부터 적재가 길면 모델이 내려갔다 다시 올라간 것이고, 채점기도 그 시간을 센다. 이때는 [6]의 '모델 새로 적재'와 [4]를 본다.

[6]의 '참고' 줄은 요청 options가 덮어쓰지 않아 모델의 Modelfile 값이 그대로 쓰이는 PARAMETER를 모델마다 한 줄로 보인다. 문제로 판정하지 않으므로 문제 줄이 없으면 '찾은 문제가 없습니다' 다음에 나온다. temperature는 '온도를 모델 기본값에 맡김' 규칙이 따로 보므로 참고 줄에서 뺀다.

모델 정보는 `/api/show`로, 실행 위치는 `/api/ps`로 조회한다. 두 조회는 모델을 GPU에 올리지 않는다. 조회 주소는 봇이 실제로 부른 주소의 `scheme://host:port`를 따른다. 조회가 연결 실패, HTTP 오류, HTTP가 아닌 응답으로 끝나면 그 자리에 '확인 못 함'이 나오고 점검은 이어진다. 모델 정보는 모델마다 한 번만 조회하므로, ex07을 켠 채로 같은 이름의 모델을 다시 등록했으면 ex07을 다시 실행한다.

### 버그를 넣지 않았을 때의 출력

자기 PC에서 버그를 넣지 않았을 때의 값은 [버그 심기 실습](#버그-심기-실습)의 준비에서 기준값으로 적는다. 다음은 봇 코드와 ex07의 규칙으로 정해지는 것이다.

- student_bot과 rag_bot은 요청마다 `"think": False`, `"stream": False`와 options의 temperature 0, num_predict 512를 보낸다. [2]의 '보낸 설정'에 이 값이 나온다.
- rag_bot은 ex07을 켠 뒤 첫 질문 때 문서 색인을 만드는 `/api/embed`를 한 번 더 보낸다. 둘째 질문부터 [3]에는 질문을 임베딩하는 호출 하나만 나온다.
- 첫 질문의 [5] 소요 시간에는 모델 적재가 들어간다. 적재가 `SLOW_LOAD`보다 길면 버그가 없어도 [6]에 '모델 새로 적재'가 나온다.
- [6] 끝의 참고 줄은 요청이 덮어쓰지 않은 Modelfile 값이 temperature 말고도 있는 모델에만 나온다.

### ex07이 보지 못하는 것

- ex07은 봇이 `urllib.request`로 보낸 요청만 잡는다. 14주차 [student_bot](../../../weeks/week14_chatbot_project/examples/src/student_bot/__init__.py)과 특강 [rag_bot](src/rag_bot/__init__.py)이 이 방식이다. requests나 ollama 패키지, 5주차의 LangChain `ChatOllama`로 요청하는 봇이면 [1]에 잡힌 호출이 없다는 안내가 나온다.
- 자세히 보는 경로는 `/api/chat`과 `/api/embed`다. `/api/generate`와 옛 `/api/embeddings` 호출은 [1]에 경로, 모델, 상태, 시간이 나오고, [6]은 그 호출의 HTTP 오류, 연결 실패, 요청 시간 초과, 모델 적재, GPU 비율만 판정한다. 생성 설정과 응답 내용은 판정하지 않는다.
- 봇에 돌려주는 응답은 읽은 바이트로 다시 만든 객체다. 본문, 상태, `headers`는 같지만 `http.client.HTTPResponse`에만 있는 `reason`, `getheader()`가 없다. 이런 속성을 쓰는 봇은 ex07 아래에서만 `AttributeError`로 끝난다.
- 봇의 `answer`를 실제로 부르므로 Ollama가 켜져 있어야 한다. [5]의 소요 시간은 ex07이 `answer()` 한 번을 잰 값이고, 채점기의 latency에는 워커와 주고받는 시간이 더해진다.

### 과제 폴더에서 ex07 쓰기

과제 챗봇은 14주차 예제를 복사한 개인 과제 폴더에서 고친다. ex07은 14주차 `shared`만 쓰므로 그 폴더로 옮겨 자기 `student_bot`을 점검할 수 있다.

1. 이 특강의 `src/ex07_inspect` 폴더를 과제 폴더의 `src/` 아래에 복사한다.
2. 과제 폴더의 `pyproject.toml`에 이미 있는 두 표를 고친다. `[project.scripts]`의 기존 줄 아래에 `ex07` 줄을 더하고, `[tool.uv.build-backend]`의 `module-name` 목록 끝에 `"ex07_inspect"`를 더한다. 14주차 예제를 그대로 복사한 폴더라면 고친 뒤 두 표는 아래 모양이다(사이의 `[build-system]`은 그대로 둔다). 이 블록을 파일 끝에 통째로 붙이면 같은 표가 두 번 생겨 TOML 오류가 난다. `ex04`를 이미 옮겼으면 `ex04` 줄과 목록의 `"lab_shared"`, `"ex04_my_eval"`을 지우지 않고 그 뒤에 더한다.

   ```toml
   [project.scripts]
   ex01 = "ex01_chat:main"
   ex02 = "ex02_evaluate:main"
   ex03 = "ex03_improve:main"
   evaluate = "ex02_evaluate:main"
   ex07 = "ex07_inspect:main"  # 더한 줄

   [tool.uv.build-backend]
   # 목록 끝의 "ex07_inspect"를 더했다
   module-name = ["shared", "student_bot", "ex01_chat", "ex02_evaluate", "ex03_improve", "ex07_inspect"]
   ```

3. `uv sync`를 다시 실행한 뒤 `uv run ex07`을 실행한다. `BOT = "student_bot"`은 그대로 둔다. `rag_bot`은 이 특강 폴더에만 있다.

scripts와 `module-name`을 고친 뒤 `uv sync`를 다시 해야 하는 까닭은 [1교시 안내](period1/README.md#과제-폴더로-옮기기)에 있다.

## 증상에서 원인으로 좁히는 순서

1. 같은 봇, 같은 질문으로 재현한다. ex07의 `BOT`을 ex04에서 잰 봇과 같게 두고, `rag_bot`이면 `MODEL`도 잴 때와 같게 둔다. ex04 출력에서 실패한 문항 아래의 `질문` 줄을 그대로 ex07의 `질문>`에 입력한다. 앞의 `질문` 낱말은 빼고 문장만 넣는다. ex04는 160자(`RESPONSE_WIDTH`)보다 긴 질문을 `...`로 잘라 보이므로, 잘렸으면 문항 파일에서 원문을 복사한다. 채점기는 문항마다 질문 하나만 보내므로, ex07에서도 앞 질문에 기대지 않고 그 질문 하나로 재현한다. 요청에 `"temperature": 0`이 없으면 같은 질문의 답이 바뀔 수 있으므로 두세 번 입력해 비교한다.
2. ex07로 요청과 응답을 본다. [6]의 문제 줄을 위에서부터 읽고, 각 줄의 근거를 [2]~[5]의 값과 대조한다. 문제 줄이 없는데 답이 틀렸다면 검색된 문서(ex05)와 `SYSTEM_PROMPT`를 보고, '참고' 줄의 값도 원인 후보로 둔다.
3. 모델에 박힌 설정을 본다. 요청에 넣지 않은 값은 모델을 등록할 때의 Modelfile이 정한다. 아래 플래그는 Ollama 0.40.17에서 확인했다. 다른 버전은 `ollama show --help`로 확인한다.

   ```powershell
   ollama show qwen3.5:2b               # capabilities, 생각 모드 기본값, 최대 컨텍스트, 양자화, 템플릿 출처
   ollama show qwen3.5:2b --parameters  # Modelfile의 PARAMETER 값
   ollama show qwen3.5:2b --system      # Modelfile의 SYSTEM
   ollama show qwen3.5:2b --template    # 프롬프트 템플릿
   ollama show qwen3.5:2b --modelfile   # Modelfile 전체. FROM 줄에는 이 PC의 모델 파일 경로가 나온다
   ollama ps                            # 올라간 모델, PROCESSOR(GPU·CPU 비율), CONTEXT
   ```

4. 형식을 본다. [5]에서 반환값이 answers·sources·abstain 세 키만 있는 사전인지 본다. 실패했으면 [2]의 json.loads 결과로 원인을 나눈다. 본문을 JSON으로 읽지 못한 경우(코드 펜스, JSON 밖 글자, 중간에 끊긴 출력)와 읽었지만 계약을 어긴 경우(키 이름, 문자열 `"false"`, 빈 문자열)는 고칠 곳이 다르다.
5. 시간을 본다. [5]의 적재를 뺀 시간을 30초 제한과 비교하고, [2]의 시간(적재·입력 처리·생성)과 [4]의 GPU 비율로 시간이 어디에 드는지 본다.

## 증상별 확인할 값과 고칠 곳

14주차 채점기는 문항마다 status를 붙인다. `invalid_response`는 응답 계약 위반, `timeout`은 문항당 30초 초과, `error`는 봇의 예외나 워커 실행 오류이고, 셋 다 그 문항이 0점이다. ex04의 실패 종류 표에서는 각각 형식 오류, 시간 초과, 실행 오류로 나온다. 형식이 맞으면 status는 `ok`이고 점수는 정답과 비교해 정해진다.

| [6]의 증상 | 확인할 값 | 고칠 곳 | 채점기 status |
|---|---|---|---|
| 모델 없음 | [1]의 HTTP 404와 오류 본문의 모델 이름 | 봇의 `MODEL`·`EMBED_MODEL`을 `ollama list`의 이름으로 | `error` |
| 주소 없음 | HTTP 404, 주소의 경로 | `OLLAMA_URL`·`CHAT_URL`·`EMBED_URL` | `error` |
| 연결 실패 | [1]의 연결 오류 | Ollama 실행 여부, 주소 상수 | `error` |
| 컨텍스트 부족 | [1]의 HTTP 400, 오류 본문의 입력 토큰 수와 컨텍스트 크기 | options의 `num_ctx`, `TOP_K`, 문서 길이 | `error` |
| 생각 모드가 없는 모델에 생각 요청 | [1]의 HTTP 400, [2]의 think, 모델 정보의 capabilities | 요청의 `"think": False` | `error` |
| 요청 오류 | HTTP 400·500번대와 오류 문구 | 오류 문구가 가리키는 요청 값(think, format, options 등) | `error` |
| 요청 시간 초과 | [1]의 timed out | 봇의 `REQUEST_TIMEOUT`, 생각 모드, GPU 비율 | 30초가 먼저 지나면 `timeout`, 아니면 `error` |
| 생각 모드를 모델 기본값에 맡김 | [2]의 think(없음 또는 null), 모델 정보의 capabilities와 생각 기본값 | 요청에 `"think": False` | 아래 생각 글 줄과 같다 |
| 응답에 생각 글이 있음, think False인데 생각 글이 옴 | [2]의 thinking 글자 수, eval_count, 시간 | `"think": False`, `ollama show`로 모델의 생각 설정 확인 | 느려지면 `timeout`, 본문이 비면 `invalid_response` |
| 본문이 비었음 | content 0자, thinking 글자 수, done_reason | think, `num_predict` | `invalid_response` |
| 출력이 길이 한도에서 끊김 | done_reason=length, eval_count, num_predict와 그 출처 | options의 `num_predict`, 짧게 답하라는 지시 | JSON이 끊기면 `invalid_response` |
| 입력이 컨텍스트 한도에 가까움 | prompt_eval_count와 [2]의 실행 컨텍스트 | options의 `num_ctx`, `TOP_K`, 문서 길이 | 이번 질문은 형식에 따른다. 입력이 더 길어지면 '컨텍스트 부족'으로 `error` |
| 코드 펜스, JSON 밖 글자 | content 앞부분, 코드 펜스 여부 | `SYSTEM_PROMPT`의 'JSON만' 지시, 펜스와 앞뒤 글자를 떼는 후처리 | 봇이 원문을 그대로 돌려주면 `invalid_response` |
| JSON 파싱 실패 | json.loads 오류와 위치 | `SYSTEM_PROMPT`의 형식 지시, `num_predict` | `invalid_response` |
| 응답 계약 실패 | [5]의 사유 | 봇의 반환 처리 | `invalid_response` |
| JSON으로 보낼 수 없는 반환값 | [5]의 사유 | 봇이 사전·리스트·문자열·참거짓만 담아 반환하게 | `error` |
| 온도를 모델 기본값에 맡김 | options의 temperature 유무, Modelfile temperature | options에 `"temperature": 0` | 형식이 맞으면 `ok`. 같은 질문의 답이 실행마다 달라질 수 있다 |
| 모델에 박힌 시스템 지시 적용 | 요청 messages의 system 유무, Modelfile SYSTEM | messages 맨 앞에 system 메시지, 또는 SYSTEM 없는 Modelfile로 다시 등록 | 답에 따라 `ok` 또는 `invalid_response` |
| 스트리밍 요청 | [2]의 stream(없음 또는 true), JSON 여러 줄로 온 응답 글 | 요청에 `"stream": False` | 봇이 응답 전체를 JSON 하나로 읽으면 `error` |
| 모델 새로 적재 | load_duration, 몇 번째 질문인지 | 첫 질문이면 정상. 매번 길면 [4]와 `ollama ps`로 모델이 내려갔다 다시 올라가는지 확인 | 준비 질문 뒤에도 길면 `timeout`이 될 수 있다 |
| 모델 일부가 CPU에서 실행됨 | [4]의 GPU 비율 | 다른 모델 내리기, `num_ctx` 줄이기, 더 작은 모델 | 느려지면 `timeout` |
| 임베딩 모델이 둘 이상 | [3]의 모델 이름과 차원 | 색인과 질문을 같은 `EMBED_MODEL`로 임베딩하고 색인 다시 만들기 | 형식이 맞으면 `ok`. 검색 결과는 ex05로 확인 |
| 시간 초과 | [5]의 적재를 뺀 시간 | 생각 모드, `num_predict`, GPU 비율 | `timeout` |
| 봇이 예외로 끝남 | [5]의 예외 이름과 [1]의 오류 | 봇의 요청·응답 처리 코드 | `error` |

[6]의 '참고: 요청이 덮어쓰지 않은 Modelfile 값' 줄은 표에 없다. 문제로 판정하지 않은 정보이고, 영향이 의심되면 봇 요청의 options에 같은 이름으로 값을 넣어 ex04로 비교한다. 읽는 법은 아래 [Modelfile 기본값](#modelfile-기본값)에 있다.

## 모델이 물려주는 설정

요청에 넣지 않은 값은 모델을 등록할 때의 설정이 정한다. 같은 봇 코드라도 `MODEL`만 바꾸면 동작이 달라지는 까닭이다. 아래 값은 기준 PC(Windows 11, RTX 5060 8GB)에서 Ollama 0.40.17로 `ollama show`, `/api/show`, `/api/ps`를 조회해 확인했다. 확인할 때 생성 요청은 보내지 않았다.

| 항목 | `qwen3.5:2b`(ID 0689d44085e0) | `wku-base`, `wku-lora`(이 특강에서 등록) | `week07-lora`(7주차에 등록) |
|---|---|---|---|
| capabilities | completion, vision, tools, thinking | tools, completion | tools, completion |
| 생각 모드 | 있음. 값은 false·true, 기본값 true | 없음 | 없음 |
| Modelfile PARAMETER | temperature 1, top_k 20, top_p 0.95, presence_penalty 1.5 | temperature 0 | num_predict 120, temperature 0 |
| Modelfile SYSTEM | 없음 | 없음 | 당신은 그리스·로마 신화를 소개하는 안내자입니다. 한국어로 짧게 답하세요. |
| 템플릿 출처(template source) | renderer_parser. `--template`은 `{{ .Prompt }}`만 보인다 | gguf_chat_template | gguf_chat_template |
| 양자화 | Q8_0, 비전 projector 포함 | F16 | F16 |
| 최대 컨텍스트(model_info) | 262144 | 32768 | 32768 |

최대 컨텍스트는 모델이 다룰 수 있는 길이이고, 실제로 쓰는 길이는 `/api/ps`의 context_length나 `ollama ps`의 CONTEXT로 본다. num_ctx를 보내지 않는 student_bot과 rag_bot으로 평가한 직후 `/api/ps`의 context_length는 `qwen3.5:2b`, `bge-m3`, `wku-lora` 모두 4096이었다. [Ollama 문서의 Modelfile 표](https://docs.ollama.com/modelfile)는 num_ctx 기본값을 2048로 적고 있어 이 관찰과 다르다. 기본값은 문서보다 실행 중인 값으로 확인한다.

### 생각 모드

`qwen3.5:2b`는 생각 모드를 지원하고 기본값이 true다. [Ollama 채팅 API 문서](https://docs.ollama.com/api/chat)는 요청의 think가 true면 생각을 요청하고, false면 생각 출력을 요청하지 않으며, null이면 모델 기본값을 쓴다고 적는다. think를 아예 빼는 경우는 문서에 따로 없다. 모델의 capabilities에 thinking이 있으면 ex07은 think를 빼거나 null로 보낸 요청을 '생각 모드를 모델 기본값에 맡김'으로 판정한다. student_bot과 rag_bot은 요청마다 `"think": False`를 보내므로 모델 기본값을 쓰지 않는다.

생각 글도 모델이 생성하는 토큰이다. 생각 모드를 바꿨으면 [2]의 thinking 글자 수, eval_count, done_reason, 시간을 바꾸기 전과 비교한다. 생각을 요청한 호출이 HTTP 오류로 끝나고 오류 본문에 `does not support thinking`이 있으면 ex07은 '생각 모드가 없는 모델에 생각 요청'으로 보인다. 어떤 모델에서 어떤 결과가 나오는지는 [버그 심기 실습](#버그-심기-실습)의 1번에서 직접 관찰한다.

태그가 같아도 가리키는 빌드가 바뀌면 생각 동작이 바뀔 수 있다. 이 과목에서는 2026-09-03에 `qwen3:4b`가 생각 전용 빌드를 가리켜 `"think": false`가 무시된 일이 있었다. ex07의 'think False인데 생각 글이 옴'이 이런 경우다. 점수를 기록할 때 모델 ID(`ollama list`의 ID)와 `ollama show`의 생각 설정을 함께 적는다.

### Modelfile 기본값

모델에 박힌 기본값은 요청이 덮어쓰지 않으면 그대로 적용된다. 요청 options에 같은 이름의 값을 넣으면 그 요청에는 넣은 값이 쓰이고, 넣지 않은 값은 모델을 등록할 때의 Modelfile PARAMETER가 쓰인다.

student_bot과 rag_bot은 options에 temperature 0과 num_predict 512를 보낸다. 그래서 `qwen3.5:2b`의 temperature 1은 쓰이지 않고, 위 표의 나머지 PARAMETER는 모델 값이 그대로 쓰인다. ex07은 이런 값을 [2]의 'Modelfile 기본값'에서 '(요청이 덮어씀)' 표시가 없는 값으로 보이고, [6]에서는 '참고' 줄로 모은다. 어느 값이 답에 영향을 주는지는 ex07이 판정하지 않는다. 의심되는 값이 있으면 봇 요청의 options에 같은 이름으로 값을 넣고 ex04로 넣기 전과 비교한다. 한 번에 한 값만 바꾸고 `public`과 `mine`을 모두 잰다.

`week07-lora`의 num_predict 120은 요청이 num_predict를 보내지 않을 때 쓰인다. rag_bot처럼 512를 보내면 512가 쓰인다.

### 시스템 지시

`week07-lora`에는 Modelfile SYSTEM(신화 안내자)이 들어 있다. 요청 messages에 system 메시지가 없으면 이 문장이 프롬프트에 들어가는 것으로 본다. Ollama 문서는 SYSTEM을 템플릿에 쓰는 시스템 메시지라고만 적고, 요청에 system 메시지가 있을 때의 처리는 적지 않는다. 기준 PC에서도 응답으로 확인하지 않았다. 그래서 봇은 요청마다 system 메시지를 직접 넣고, ex07은 요청에 system이 없는데 Modelfile SYSTEM이 있으면 [6]에 '모델에 박힌 시스템 지시 적용'을 낸다.

### 컨텍스트와 출력 길이

입력이 실행 컨텍스트에 비해 길거나 출력이 num_predict에 닿으면 응답이 정상과 달라진다. 확인할 값은 [2]의 '컨텍스트'(실행 길이와 그 출처), prompt_eval_count, eval_count, done_reason이다.

- 요청이 HTTP 오류로 끝나고 오류 본문에 `context size`나 `context length`가 있으면 ex07은 '컨텍스트 부족'으로 보인다.
- done_reason이 length면 출력이 num_predict에서 멈춘 것이다. ex07은 '출력이 길이 한도에서 끊김'을 보이고, 그 num_predict가 요청과 Modelfile 가운데 어디서 왔는지 근거에 적는다.
- '입력이 컨텍스트 한도에 가까움'은 prompt_eval_count가 실행 컨텍스트의 `NEAR_CONTEXT` 비율 이상일 때 내는 경고다. 이번 요청은 처리됐지만 질문이나 검색 문서가 조금 더 길어지면 요청이 오류로 끝날 수 있다.

값에 따라 어떤 결과가 나오는지는 [버그 심기 실습](#버그-심기-실습)의 2번과 6번에서 직접 관찰한다.

### 템플릿 출처

`ollama show <모델>`의 template source(ex07 [2]의 '템플릿 출처')는 모델마다 다르다. 이 특강의 모델에서 기준 PC의 Ollama 0.40.17로 확인한 값이다.

| 모델 | 받거나 등록한 방법 | template source |
|---|---|---|
| `qwen3.5:2b` | Ollama 라이브러리에서 `ollama pull` | renderer_parser |
| `bge-m3`(임베딩 모델) | Ollama 라이브러리에서 `ollama pull` | none |
| `wku-base`, `wku-lora`, `week07-lora` | GGUF 파일을 Modelfile로 등록(`ollama create`) | gguf_chat_template |

같은 라이브러리에서 받은 모델끼리도 값이 다르다. 다른 모델이나 다른 방법(예: Hugging Face Hub의 GGUF를 `hf.co/...` 이름으로 받음)으로 받은 모델은 확인하지 않았으므로 `ollama show`로 본다.

renderer_parser 모델은 `--template`이 `{{ .Prompt }}`만 보여 이 명령으로는 실제 프롬프트 글을 볼 수 없다. 파일로 등록한 학습 모델은 `--template` 글을 학습 때의 템플릿과 바로 비교할 수 있다. 비교하는 방법은 아래 [템플릿](#템플릿)에 있다.

### 확인 필요

- num_ctx를 보내지 않을 때 Ollama가 실행 컨텍스트 길이를 정하는 규칙. 기준 PC에서는 4096을 관찰했다.
- 입력은 실행 컨텍스트 안에 들지만 입력과 num_predict를 더하면 넘을 때의 동작.
- 요청에 system 메시지가 있을 때 Modelfile SYSTEM이 빠지는지.
- GGUF 메타데이터의 샘플링 값(`general.sampling.*`)을 Ollama가 기본값으로 쓰는지. 아래 '같은 messages로 두 실행 비교'의 샘플링 값 단계에서 다룬다.

## 버그 심기 실습

버그를 일부러 하나 넣고, 실행하기 전에 결과를 예상해 적고, ex07과 ex04로 관찰한 뒤 넣기 전 상태로 되돌린다. 증상과 원인을 짝짓는 연습이다. 예상 결과는 이 문서에 두지 않는다.

버그 1~3은 [4교시 실습](period4/README.md#3-버그-심기)에서 하고, 4교시에는 시간에 맞춰 질문 A 하나만 넣는다. 4~9는 과제 기간에 골라서 하는 선택 항목이다. 7은 다른 임베딩 모델이 설치된 PC에서만 할 수 있다.

준비는 다음 순서로 한다.

1. 넣기 전 상태를 기록한다. `git diff -- src/rag_bot/__init__.py`를 실행해 출력을 버그 심기 기록표 첫 칸에 적는다. 2·3교시에 바꾼 상수(`TOP_K`, `MIN_SCORE`, `MODEL` 등)가 있으면 그 줄이 나오고, 바꾼 것이 없으면 아무것도 나오지 않는다. 버그를 되돌리면 이 상태로 돌아와야 한다.
2. [ex07](src/ex07_inspect/__init__.py)의 `BOT`을 `"rag_bot"`으로 바꾼다. 버그는 특강의 [rag_bot](src/rag_bot/__init__.py)에 넣는다. 14주차 `student_bot`은 저장소의 기준 봇이므로 고치지 않는다. `rag_bot`의 `MODEL`은 지금 값을 그대로 둔다. 4교시에는 3교시에 등록한 자기 모델이다.
3. 버그 없이 `uv run ex07`을 실행하고 다음 두 질문을 차례로 입력한다. 질문마다 [2]의 모델 정보(capabilities), prompt_eval_count, eval_count와 [5]의 적재를 뺀 시간, status, [6]에 나온 줄을 버그 심기 기록표의 기준값 칸에 적는다.
   - 질문 A: 원광대학교를 상징하는 새는 무엇인가요?
   - 질문 B: 오늘 학생식당 저녁 메뉴는 무엇인가요?
4. 버그는 한 번에 하나만 넣는다. 넣을 때마다 ex07을 `/bye`로 끝내고 다시 실행해 같은 질문을 입력한다. ex07은 실행 중에 고친 봇 파일을 다시 읽지 않는다.
5. 실행 전에 버그 심기 기록표의 예상 칸을 채운다. 예상은 준비 3에서 적은 지금 모델의 정보와 위 [증상 표](#증상별-확인할-값과-고칠-곳)를 보고 정한다. 같은 버그라도 `MODEL`이 가리키는 모델에 따라 결과가 다를 수 있다. 실행 뒤에는 [6]에 새로 나온 증상과 [5]의 status를 관찰 칸에 적고, [ex04](src/ex04_my_eval/__init__.py)를 `BOT = "rag_bot"`, `QUESTION_SET = "mine"`으로 한 번 실행해 전체 평균과 실패 종류 표에서 잃은 점수가 가장 큰 줄을 적는다.
6. 되돌릴 때는 바꾼 곳을 넣기 전 값으로 돌린다. 되돌린 뒤 `git diff -- src/rag_bot/__init__.py`의 출력이 준비 1의 기록과 같은지 확인한다.

기준값에서도 [6]에 줄이 나올 수 있다. 버그를 넣은 뒤에는 기준값에 없던 줄을 찾는다. ex07을 다시 켠 첫 질문에서 모델을 다시 올리면 버그와 상관없이 '모델 새로 적재'가 나올 수 있다.

| 번호 | 시기 | 버그 | 넣는 곳(`src/rag_bot/__init__.py`) | 바꾸는 값 |
|---|---|---|---|---|
| 1 | 4교시 | 생각 모드 켜기 | `answer()` 요청의 `"think": False` | `"think": True` |
| 2 | 4교시 | 출력 한도 줄이기 | `answer()` 요청 options의 `"num_predict": 512` | 준비 3에서 적은 질문 A의 eval_count를 2로 나눈 정수 |
| 3 | 4교시 | 없는 모델 이름 | `MODEL` | 지금 이름에서 한 글자를 틀리게 바꾼 값(예: `"qwen3.5:2b"`의 콜론을 하이픈으로, `"wku-lora"`의 하이픈을 밑줄로) |
| 4 | 과제 기간(선택) | 봇 안의 print | `answer()`의 `documents = retrieve(question)` 다음 줄 | `print("검색한 문서:", [doc["id"] for doc in documents])` 추가 |
| 5 | 과제 기간(선택) | 'JSON만' 지시 빼기 | `SYSTEM_PROMPT`의 마지막 줄 | `JSON 밖의 설명이나 마크다운 코드 블록을 넣지 않는다.` 삭제 |
| 6 | 과제 기간(선택) | 문서를 모두 넣고 컨텍스트 줄이기 | `TOP_K`, `answer()` 요청 options | `TOP_K = 100`, options에 `"num_ctx": N` 추가 |
| 7 | 과제 기간(선택) | 질문 임베딩만 다른 모델 | `rank()`의 `query = embed([question])[0]` | `query = post(EMBED_URL, {"model": "<다른 임베딩 모델>", "input": [question]})["embeddings"][0]` |
| 8 | 과제 기간(선택) | 온도 지우기 | `answer()` 요청 options의 `"temperature": 0` | 그 항목 삭제 |
| 9 | 과제 기간(선택) | 스트리밍 켜기 | `answer()` 요청의 `"stream": False` | 그 항목 삭제 |

- 버그 4는 ex04로 채점할 때도 본다(`BOT = "rag_bot"`). 채점 워커가 봇의 일반 출력을 어디로 보내는지 [lab_shared/worker.py](src/lab_shared/worker.py)에서 찾아 예상과 비교한다.
- 버그 6의 `TOP_K = 100`은 [corpus.json](../../../weeks/week14_chatbot_project/examples/src/shared/data/corpus.json)의 문서 수보다 커서 문서를 모두 보낸다는 뜻이다. N은 준비 3에서 적은 질문 A의 prompt_eval_count를 2로 나눈 정수다.
- 버그 7은 capabilities에 embedding이 있는 다른 모델이 수업 전에 설치된 PC에서만 한다. 수업 중에 모델을 내려받지 않는다. rag_bot은 색인을 첫 질문 때 메모리에 만들므로 `EMBED_MODEL`만 바꾸면 색인과 질문이 함께 새 모델로 바뀌어 섞이지 않는다. 그래서 질문 임베딩 줄만 바꾼다.
- 버그 7의 섞임은 ex07을 켠 뒤 첫 질문에서만 볼 수 있다. rag_bot은 색인을 만드는 임베딩 호출을 첫 질문 때 한 번 보내고, 둘째 질문부터는 질문 임베딩 호출만 보낸다. 두 질문을 볼 때는 질문마다 ex07을 다시 실행해 첫 질문의 [3]과 [6]을 적는다. 색인을 파일에 저장해 두는 봇은 `EMBED_MODEL`만 바꿔도 섞이고, 그때 색인을 만든 호출은 ex07에 잡히지 않아 [3]에는 질문 쪽 모델만 보인다.
- 버그 8은 같은 질문을 세 번 입력해 답을 비교한다.

버그 심기 기록표

| 준비 1의 `git diff -- src/rag_bot/__init__.py` 출력(없으면 '없음') |
|---|
|  |

| 기준값(버그 없음) | capabilities | prompt_eval_count | eval_count | [5] 적재를 뺀 시간 | [5] status | [6]에 나온 줄 |
|---|---|---:|---:|---:|---|---|
| 질문 A |  |  |  |  |  |  |
| 질문 B |  |  |  |  |  |  |

| 번호 | 예상(실행 전) | 관찰: [6]에 새로 나온 증상 | 관찰: [5]의 status | 관찰: ex04 전체 평균과 잃은 점수가 가장 큰 실패 종류 |
|---|---|---|---|---|
| 1 |  |  |  |  |
| 2 |  |  |  |  |
| 3 |  |  |  |  |
| 4 |  |  |  |  |
| 5 |  |  |  |  |
| 6 |  |  |  |  |
| 7 |  |  |  |  |
| 8 |  |  |  |  |
| 9 |  |  |  |  |

## 학습한 모델에서 생기는 버그

학습 직후 transformers로 본 답과 Ollama에 등록한 모델의 답이 다르면, 가중치를 다시 학습하기 전에 두 실행의 입력과 생성 조건이 같은지 본다. 학습 예시와 다른 입력을 받은 모델은 학습한 형식대로 답하지 않을 수 있다.

### 템플릿

학습은 `tokenizer.apply_chat_template`으로 messages를 프롬프트 글 하나로 만든다. 이때 쓰는 템플릿은 모델 폴더에 있다. `uv run prepare`로 받은 기본 모델 폴더(`finetune/models/Qwen2.5-0.5B-Instruct/`)에서는 `tokenizer_config.json`의 `chat_template`이다. transformers 4.57로 저장한 병합 폴더(`finetune/models/wku-lora-merged/`, 7주차의 `models/merged-run-001/`)에서는 `tokenizer_config.json`에 `chat_template`이 없고 같은 폴더의 `chat_template.jinja`에 있다.

Ollama는 `ollama show <모델>`의 template source가 가리키는 템플릿을 쓴다. 7주차의 `week07-lora`는 `gguf_chat_template`이고, `--template` 글이 Qwen2.5-0.5B-Instruct `tokenizer_config.json`의 `chat_template`과 같았다(2,507자 비교). GGUF로 변환할 때 토크나이저의 템플릿이 파일에 들어가고 Ollama가 그 템플릿을 쓴 것으로 본다.

같은 모델의 `ollama show week07-lora --modelfile` 출력에는 `TEMPLATE {{ .Prompt }}` 줄이 나온다. 실제 템플릿은 `--template`과 template source로 확인한다. 이 출력을 복사해 새 Modelfile을 만들 때 그 TEMPLATE 줄이 GGUF 템플릿을 대신하는지는 확인하지 않았다. 새로 등록한 뒤 `ollama show <새 모델>`의 template source가 `gguf_chat_template`인지 본다.

Qwen2.5 템플릿은 messages에 system 메시지가 없으면 `You are Qwen, created by Alibaba Cloud. You are a helpful assistant.`를 넣는다(템플릿 글에서 확인). 학습 예시와 추론 요청은 같은 system 메시지로 시작해야 한다. 특강의 [ex06](src/ex06_make_sft/__init__.py)은 rag_bot의 `messages()`로 학습 예시를 만들어 이 조건을 맞춘다.

### 7주차 Modelfile을 복사할 때 따라오는 값

[7주차 Modelfile](../../../weeks/week07_peft_lora/examples/Modelfile)은 다음과 같다.

```text
FROM ./models/week07-lora.gguf
PARAMETER temperature 0
PARAMETER num_predict 120
SYSTEM 당신은 그리스·로마 신화를 소개하는 안내자입니다. 한국어로 짧게 답하세요.
```

FROM 줄만 바꿔 원광대 챗봇 모델을 등록하면 num_predict 120과 신화 안내자 SYSTEM도 함께 등록된다. rag_bot은 요청에 num_predict 512를 넣으므로 120은 쓰이지 않는다. SYSTEM은 요청에 system 메시지가 있으면 빠지는 것으로 보지만 확인하지 않았다. `ollama run`으로 직접 묻거나 이 값을 보내지 않는 봇에는 두 값이 그대로 쓰인다. 등록한 뒤 ex07 [2]의 모델 정보나 `ollama show <모델> --parameters`, `--system`으로 확인한다. 특강의 [Modelfile.lora](../finetune/Modelfile.lora)는 FROM과 temperature 0만 둔다.

### 학습 데이터와 추론의 검색 설정

ex06은 학습 파일과 함께 그때의 `EMBED_MODEL`·`TOP_K`·`MIN_SCORE`를 특강 폴더의 `outputs/sft/settings.json`에 남긴다. 학습 뒤 rag_bot 상수를 바꾸면 모델은 학습 때와 다른 문서 묶음을 받는다. 상수를 바꿨으면 ex06과 학습을 다시 하거나, 비교할 때 `settings.json`의 값으로 되돌린다.

### 같은 messages로 두 실행 비교(강의자 시연, 선택)

`finetune/`의 명령은 `prepare`, `ft01`, `ft02` 셋이고, 같은 messages로 프롬프트 글과 답을 출력하는 명령은 없다. 그래서 이 비교는 강의자가 시연하는 선택 항목이다. 학생은 과제 기간에 필요하면 이 순서대로 직접 코드를 써서 비교한다.

학습 직후 모델(transformers)과 Ollama 등록 모델에 같은 messages를 넣고 답을 비교한다. 다르면 아래 순서로 한 가지씩 맞춰 가며 원인을 좁힌다. 한 단계를 맞추자 답이 같아지면 그 단계가 원인이다. ex07 [2]의 messages 전문(`SHOW_PROMPT = True`)이 rag_bot이 보낸 그대로다.

transformers 쪽은 `uv run ft02`가 만든 병합 폴더(`finetune/models/wku-lora-merged/`)를 불러 쓴다. 학습과 병합 명령은 [따라하기의 학습과 병합](../walkthrough.md#2-학습과-병합finetune)에 있다.

1. 템플릿. transformers 쪽은 `tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)`로 만든 글을 출력한다. Ollama 쪽은 template source와 `--template` 글을 본다. 두 템플릿이 같으면 다음 단계로 간다.
2. 샘플링 값. 7주차 [answer()](../../../weeks/week07_peft_lora/examples/src/shared/__init__.py)는 `do_sample=False`로 생성하면서 temperature·top_p·top_k만 None으로 지운다. Qwen2.5-0.5B-Instruct의 `generation_config.json`에 있는 `repetition_penalty` 1.1은 지우지 않는다. Ollama 쪽은 Modelfile의 temperature 0과 요청 options가 정하고, Ollama 문서의 Modelfile 표는 repeat_penalty 기본값을 1.0(꺼짐)으로 적는다. GGUF 메타데이터에는 `general.sampling.*` 값(temp 0.7, top_k 20, top_p 0.8, penalty_repeat 1.1)이 들어 있는데(`week07-lora`·`wku-lora`의 `/api/show`에서 확인), Ollama가 이 값을 기본값으로 쓰는지는 확인하지 않았다. 비교할 때는 한쪽 값을 다른 쪽에 맞춘다. 예를 들어 transformers에 `repetition_penalty=1.0`을 주거나 Ollama 요청 options에 `"repeat_penalty": 1.1`을 넣는다.
3. 시스템 메시지. 두 실행의 messages가 같은 system 메시지로 시작하는지 본다. system 메시지가 빠지면 transformers는 Qwen 기본 문장을 넣고, Ollama는 Modelfile SYSTEM이 있으면 그 문장을 넣는 것으로 본다(Ollama 쪽은 확인 필요).
4. 양자화. 7주차와 특강의 `load_model()`은 기본으로 모델을 float32로 올리고, GGUF 변환은 둘 다 `--outtype f16`이다. 정밀도가 다르면 greedy 생성에서도 고르는 토큰이 갈릴 수 있다. f16 GGUF로 먼저 비교하고, Q8_0이나 Q4로 양자화한 모델은 f16 모델과 따로 비교한다.

Ollama 쪽 모델은 `ft02`의 병합 폴더를 [따라하기의 GGUF 변환과 등록](../walkthrough.md#3-gguf-변환과-등록finetune) 명령으로 f16 GGUF로 바꾸고 `Modelfile.lora`로 등록한 것이다. 다시 학습했으면 변환 명령의 입력 폴더를 새 `MERGED_DIR`로 바꿔야 새 모델이 등록된다.

## 학습 중 느려짐과 메모리

`ft01`이 오류 없이 점점 느려지면 GPU 메모리가 넘쳤는지부터 본다. 증상은 두 가지로 나타난다. step 시간이 점점 늘어나는데 오류는 나지 않고, Windows 작업 관리자의 성능 탭에서 GPU의 '공유 GPU 메모리' 사용량이 올라간다.

확인할 값

- `nvidia-smi`의 메모리 사용량. 학습 전에 한 번 재서 다른 프로그램이 쓰는 양을 적고, 학습 중 최고값과 비교한다. 기준 PC의 RTX 5060 8GB는 nvidia-smi에서 전체 8,151MiB로 나왔다.
- torch가 잡아 둔 메모리(reserved)의 최고값. [ft01](../finetune/src/ft01_train/__init__.py)은 끝에 'GPU 최대 할당 메모리'(텐서가 실제로 쓴 양, `max_memory_allocated`)와 'GPU 최대 예약 메모리'(`max_memory_reserved`)를 출력한다. 예약이 VRAM 전체를 넘으면 넘친 것이고, 예약이 할당보다 훨씬 크면 메모리 조각이 쌓인 것이다.

원인 후보

- VRAM 넘침. Windows의 NVIDIA 드라이버는 VRAM이 모자라면 시스템 RAM을 빌려 쓰는 것으로 보인다(sysmem fallback). 그래서 CUDA out of memory 오류 없이 느려진다.
- 메모리 단편화. 예시 길이가 들쑥날쑥하면 step마다 다른 크기의 메모리를 잡았다 놓으면서 조각이 쌓이고, torch가 잡아 두는 양이 계속 늘어난다.

고칠 곳

- [ft01](../finetune/src/ft01_train/__init__.py)의 `DTYPE = torch.bfloat16`과 `GRADIENT_CHECKPOINTING = True`. 둘 다 기본값이다. float32로 바꾸거나 체크포인팅을 끄면 메모리가 늘어난다.
- `ft01`의 `DataCollatorForSeq2Seq(..., pad_to_multiple_of=64)`. 길이를 64토큰 단위로 맞춰 조각이 쌓이는 것을 줄인다. 기본으로 들어 있다.
- 예시 길이와 batch. 예시가 길수록 메모리를 더 쓴다. rag_bot의 `TOP_K`(예시에 들어가는 문서 수)를 줄이고 ex06을 다시 실행하면 예시가 짧아진다. `ft01`의 batch는 `per_device_train_batch_size=1`이고 4건을 모아(`gradient_accumulation_steps=4`) 한 step을 학습한다. batch를 키우면 그만큼 메모리를 더 쓰므로, step마다 보는 예시를 늘리려면 모으는 횟수를 키운다.
- 다른 프로그램의 GPU 사용. `ft01`은 Ollama가 모델을 올려 두었으면 멈추지만, 다른 프로그램이 쓰는 GPU 메모리는 보지 않는다.

기준 PC(Windows 11, RTX 5060 8GB)에서 Qwen2.5-0.5B-Instruct LoRA 학습으로 2026-11-23에 잰 값이다.

| 조건 | 결과 |
|---|---|
| float32, 체크포인팅 없음 | torch reserved 8,962MiB로 VRAM 8,151MiB를 넘었다. 오류 없이 step 시간이 7.7초에서 19.8초로 늘었다. Windows의 sysmem fallback으로 보인다 |
| 학습 예시 197건, 150 step에서 `pad_to_multiple_of=64`를 넣기 전과 뒤 | reserved 9,002MiB에서 3,998MiB로 줄고, step 시간은 1.16초에서 1.04초가 됐다. 이 결과로 `ft01` 기본값에 넣었다 |
| 기본 설정(bfloat16, 체크포인팅, 64토큰 패딩), 공개 학습 문항 40건, 30 step | nvidia-smi 최고 6,299MiB(측정 전 1,042MiB 포함). [따라하기의 기준 PC 실측](../walkthrough.md#기준-pc-실측)에 있다 |

## 고친 뒤 확인

1. 같은 질문을 ex07에 다시 입력한다. [6]에서 고친 증상이 사라졌는지, 새 증상이 생기지 않았는지 본다. [2]의 eval_count와 시간을 고치기 전 기록과 비교한다.
2. [ex04](src/ex04_my_eval/__init__.py)로 점수를 다시 잰다. `BOT`을 고친 봇으로 두고 `QUESTION_SET`을 `"mine"`과 `"public"`으로 바꿔 두 번 실행한다. 한 문항을 고치면 다른 문항이 나빠질 수 있으므로 세트 전체를 잰다.
3. 과제로 제출할 봇은 학생의 14주차 예제 사본에서 `uv run evaluate`로 공개 20문항을 다시 잰다.
4. 바꾼 값, 고치기 전후의 점수, 남은 실패를 [보고서 양식](../../../weeks/week14_chatbot_project/report_template.md)의 3절(기준 구현과 개선 실험)과 4절(실패와 해결 과정)에 적는다.
