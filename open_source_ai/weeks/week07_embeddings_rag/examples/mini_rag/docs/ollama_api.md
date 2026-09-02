# Ollama 서버와 REST API

Ollama는 로컬 PC에서 언어 모델을 실행하는 서버 프로그램이다. 서버가 켜져 있으면 기본 주소 `http://localhost:11434`에서 REST API 요청을 받는다. 설치된 모델 목록은 `GET /api/tags`로 확인한다.

`POST /api/generate`는 프롬프트 한 덩어리를 보내 이어지는 텍스트를 받는 단발 호출이다. `POST /api/chat`은 system, user, assistant 역할이 붙은 메시지 배열을 보내 대화 형식으로 답을 받는다.

요청 JSON의 `stream`을 false로 두면 응답이 한 번에 오고, true면 줄 단위 NDJSON으로 조각이 흘러온다. `options`에는 `temperature`, `num_ctx`(컨텍스트 길이), `num_predict`(최대 생성 토큰 수)를 넣는다.

Qwen3 계열처럼 생각(thinking) 출력을 지원하는 모델은 `think`를 false로 두어야 답만 받는다. 응답의 `eval_count`와 `eval_duration`으로 생성 토큰 수와 초당 토큰 속도를 계산할 수 있다.
