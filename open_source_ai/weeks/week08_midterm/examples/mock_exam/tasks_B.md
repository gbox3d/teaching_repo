# 모의 실기 B — Git 개념·사용법과 Ollama 사용법·응용

공개 동형 모의 문제다. 실제 실기 패킷의 문항·값·정답이 아니다. 제한 시간은 30분이며, 답안은 실습 폴더의 `answers_B.md`에 맨 아래 양식으로 쓴다. 허용 자료·AI 도구 범위는 실제 시험에서는 시험 공지를 따른다.

B-1·B-2는 2주차 Git, B-3·B-4는 4주차 Ollama다. B-2와 B-4는 실제로 실행하는 실기이고 B-1·B-3은 개념 문항이다. 명령과 터미널 출력은 그대로 붙이고, 개념 문항은 한두 문장으로 답한다. 확신이 없으면 "확인할 명령이나 문서"를 적는다.

## B-1 · Git 기록 흐름: add·commit·push

2주차에 본 기록 흐름이다.

```text
working tree ──①──▶ staging area ──②──▶ repository(HEAD) ──③──▶ origin(GitHub)
```

### B-1-1 · 세 명령과 네 영역

①·②·③에 들어갈 명령을 쓰고, 네 영역(working tree, staging area, repository, origin)에 각각 무엇이 들어 있는지 한 줄씩 쓴다. "commit은 로컬에서 끝난다"는 말이 무슨 뜻인지도 쓴다.

### B-1-2 · `git status` 읽기

어느 저장소에서 `git status`를 실행했더니 다음과 같이 나왔다.

```text
On branch main
Your branch is ahead of 'origin/main' by 1 commit.

Changes to be committed:
        modified:   main.py

Changes not staged for commit:
        modified:   README.md

Untracked files:
        memo.txt
```

- (a) `main.py`, `README.md`, `memo.txt`는 각각 어느 영역에 있는가? 파일마다 한 줄로 쓴다.
- (b) 지금 바로 `git commit -m "메시지"`를 실행하면 세 파일 중 무엇이 기록되는가?
- (c) 첫 줄의 `ahead of 'origin/main' by 1 commit`은 무슨 뜻이고, 이 상태를 GitHub에 반영하려면 어떤 명령이 필요한가?

### B-1-3 · 명령 순서와 영역

위 상태에서 `README.md`와 `memo.txt`의 변경까지 한 commit으로 기록하고 GitHub에 올리려 한다. 실행할 명령을 순서대로 쓰고, 각 명령이 바꾸는 영역을 괄호로 붙인다.

### B-1-4 · `.gitignore`가 막지 못한 `.env`

`.gitignore`에 `.env`를 추가했는데 `git status`의 `Changes to be committed`에 `new file: .env`가 계속 보인다.

- (a) 왜 `.gitignore`가 막아 주지 못했는가?
- (b) `.env` 파일은 내 PC에 그대로 두고 기록 후보에서만 빼는 명령은?

<details>
<summary>힌트</summary>

2주차 슬라이드의 세 영역 그림을 그대로 쓴다. `git status`의 `Changes to be committed`는 staging area, `Changes not staged for commit`은 working tree, `Untracked files`는 아직 추적하지 않는 파일이다. `.gitignore`는 아직 추적되지 않은 파일만 막으므로 이미 `git add`된 파일은 `git restore --staged`로 내린다(3주차 3교시).
</details>

## B-2 · GitHub에 올리기 (실기)

모의 A의 `week8-hello`(없으면 아무 uv 프로젝트)를 GitHub에 올린다. 2주차 1교시 문제 1에서 한 것과 같다.

### 요구사항

1. GitHub에서 빈 공개 저장소 `week8-hello`를 만든다. README·`.gitignore`·license를 추가하지 않는다(로컬에 이미 commit이 있다).
2. 저장소 페이지의 HTTPS URL로 원격을 연결하고 push한다.

   ```powershell
   git remote add origin <본인 저장소 HTTPS URL>
   git remote -v
   git push -u origin main
   ```

3. `README.md` 끝에 한 줄을 추가하고 `git status` → `git add README.md` → `git commit -m "Update README"` → `git push`를 실행한다.
4. 브라우저에서 저장소 페이지를 새로고침해 commit 수가 2인지 확인한다.

### 완료 조건

- [ ] `git remote -v`에 fetch·push 두 줄이 같은 URL로 보인다.
- [ ] GitHub 저장소 페이지의 commit 수가 2이고, 최신 commit 메시지가 `git log -1`과 같다.
- [ ] `git status`가 clean이고 `ahead` 표시가 없다.

### 답안에 적을 것

- 저장소 URL, `git remote -v` 출력, 3번의 `git status` 출력(push 전), `git log --oneline` 출력.
- (a) 첫 push에 `-u`를 붙인 이유와, 두 번째는 `git push`만으로 된 이유.
- (b) `git log`에는 commit이 있는데 GitHub 페이지에는 없다면 무엇을 빠뜨린 것인가?
- (c) 두 branch가 같은 파일의 같은 줄을 다르게 고친 뒤 merge하면 파일에 어떤 표시가 생기는가? 그때 해야 할 일을 순서대로 쓴다(파일 열기 → 결과 문장 쓰기 → ? → ?).

<details>
<summary>힌트</summary>

2주차 1교시 문제 1·2와 같다. `-u`는 추적 관계를 기억해 다음부터 `git push`만으로 같은 곳에 보낸다. GitHub가 push를 거부하면 저장소를 만들 때 README나 `.gitignore`를 추가하지 않았는지 확인한다. 충돌 표시는 `<<<<<<<`, `=======`, `>>>>>>>`이고, 절차는 `git status` → 파일 열기 → 표시 지우고 결과 문장 쓰기 → `git add` → `git commit`이다.
</details>

## B-3 · Ollama 사용법

### B-3-1 · 터미널 명령

- (a) `ollama list`, `ollama show qwen3.5:2b`, `ollama run qwen3.5:2b --think=false`, `ollama ps` 네 명령이 각각 알려 주는 것(또는 하는 일)을 한 줄씩 쓴다.
- (b) `ollama list`의 SIZE와 `ollama ps`의 SIZE가 다른 이유는?
- (c) `--think=false`가 끄는 것은 무엇인가? 첫 답만 늦게 나오는 이유는?

### B-3-2 · 메시지 세 역할과 기억

```python
messages = [{"role": "system", "content": "초보자용 Python 선생님. 비유 하나로 두 문장."}]
messages.append({"role": "user", "content": "리스트가 무엇이야?"})
response = ollama.chat(model="qwen3.5:2b", messages=messages, think=False)
print(response.message.content)
messages.append(response.message)
```

- (a) `system`, `user`, `assistant` 세 역할은 각각 누구의 말인가?
- (b) `response.message.content`는 무엇인가? 마지막 줄 `messages.append(response.message)`가 없으면 다음 질문에서 무엇이 달라지는가?
- (c) "모델이 기억한다"는 말이 실제로 뜻하는 것은 무엇인가?

### B-3-3 · temperature

- (a) `options={"temperature": 0}`과 `{"temperature": 1}`의 차이는? 같은 질문을 두 번 했을 때 답이 같은가?
- (b) 시험 채점 도우미와 소설 아이디어 도우미에는 각각 어떤 temperature가 맞는가? 이유를 쓴다.

### B-3-4 · 세 가지 "안 된다" 구분

표를 채운다. 원인과 먼저 확인할 것을 한 줄씩 쓴다.

| 메시지 | 원인 | 먼저 확인할 것 |
|---|---|---|
| `Failed to connect to Ollama` |  |  |
| `model 'qwen3.5:2b' not found` |  |  |
| `No module named 'ollama'` |  |  |

그리고 Ollama 서버, 터미널 명령(`ollama run`), Python 라이브러리(`ollama.chat`) 셋의 관계를 "손님"이라는 말을 넣어 한 문장으로 쓴다.

<details>
<summary>힌트</summary>

4주차 보고서 1·2절에 적은 것이다. `ollama ps`의 SIZE에는 대화 내용을 담는 공간(컨텍스트)이 더해진다. "기억"은 지난 질문·답을 `messages`에 쌓아 다시 보내는 것이다. 연결 실패는 서버(앱)가 꺼진 것, 모델 없음은 이름·태그, 모듈 없음은 `uv run`으로 실행하지 않은 것이다.
</details>

## B-4 · Ollama 응용: 툴 콜링 함수 추가 (실기)

준비: 4주차 3교시 `period3` 프로젝트(`C:\classwork\week04\period3`)로 이동한다. 없으면 교재 `week04_ollama_local_llm/examples/period3`를 복사하고 `uv sync`한다. `ollama show qwen3.5:2b`의 Capabilities에 `tools`가 있는지 확인한다.

### B-4-1 · 함수 추가

`src/ex07/tools.py`에 다음 함수를 추가하고 `TOOLS`에 등록한다. 함수에는 `Args:`가 들어간 docstring을 쓴다. 추가한 코드 전체를 답안에 붙인다.

- 함수 이름: `discount_price`
- 인자: `price`(정가), `percent`(할인율, %)
- 반환: 할인된 가격(`price × (1 − percent ÷ 100)`)

### B-4-2 · 실행 기록

`uv run ex07`을 실행하고 `정가 25000원 상품을 20% 할인하면 얼마야?`를 입력한다. 화면의 `[함수 실행]` 줄과 `AI>` 답을 그대로 붙인다. 모델이 새 함수를 부르지 않으면 질문이나 docstring을 바꿔 다시 시도하고, 무엇을 바꿨고 결과가 어땠는지 적는다. `/bye`로 종료한다.

### B-4-3 · 함수 결과와 모델 답

함수가 돌려준 값과 AI의 최종 답이 같은지 비교한다. 다르다면 어느 쪽을 믿어야 하는지와 그 이유를 쓴다. `tools=`를 빼고 같은 계산을 물으면 어떻게 될지 예상을 쓴다(시간이 남으면 실제로 해 본다).

### B-4-4 · 세 단계와 실행 주체

툴 콜링이 동작하는 세 단계(함수 목록 보내기 → 모델의 호출 요청 → 내 프로그램이 실행하고 결과 돌려주기)와, 함수를 실제로 실행한 주체가 누구인지 내 말로 2~3문장으로 쓴다. 4주차 슬라이드를 보지 않고 쓴다.

### B-4-5 · Modelfile 읽기

```text
FROM qwen3.5:2b
SYSTEM """너는 '오픈소스 AI 응용' 수업의 실습 도우미다. 한국어로 다섯 문장 이내로 답한다."""
PARAMETER temperature 0.3
```

- (a) `ollama create student01-helper -f Modelfile`는 무엇을 만드는가? 디스크를 두 배로 쓰는가?
- (b) 이 시스템 프롬프트가 바꿀 수 있는 것과 바꿀 수 없는 것은?
- (c) `ollama rm student01-helper`를 하면 `qwen3.5:2b`도 지워지는가?

<details>
<summary>힌트</summary>

4주차 3교시 문제 3·4·5와 같다. 함수를 `TOOLS`에 넣었는지 먼저 보고, 모델이 함수를 부르지 않으면 질문을 docstring과 비슷하게 바꿔 다시 묻는다. 함수 결과와 `AI>` 답이 다르면 함수 결과가 정답이다. `ollama create`는 가중치를 복사하지 않는다.
</details>

## `answers_B.md` 양식

```markdown
# 모의 실기 B 답안 — student01

## B-1 Git 기록 흐름

### B-1-1
①: ②: ③:
working tree / staging area / repository / origin:
"commit은 로컬에서 끝난다":

### B-1-2
(a) main.py / README.md / memo.txt:
(b):
(c) 뜻 / 명령:

### B-1-3
1. `...` (영역)
2. `...` (영역)
3. `...` (영역)

### B-1-4
(a):
(b):

## B-2 GitHub에 올리기

저장소 URL:
git remote -v:
push 전 git status:
git log --oneline:
(a):
(b):
(c) 표시 / 순서:

## B-3 Ollama 사용법

### B-3-1
(a) list / show / run / ps:
(b):
(c):

### B-3-2
(a):
(b):
(c):

### B-3-3
(a):
(b):

### B-3-4
| 메시지 | 원인 | 먼저 확인할 것 |
|---|---|---|
| Failed to connect to Ollama |  |  |
| model 'qwen3.5:2b' not found |  |  |
| No module named 'ollama' |  |  |
셋의 관계:

## B-4 툴 콜링

### B-4-1 추가한 코드
```

### B-4-2 실행 기록
[함수 실행] 줄:
AI> 답:
다시 시도했다면 바꾼 것과 결과:

### B-4-3
함수 결과 / 모델 답 / 믿을 쪽과 이유:
tools= 없이 물으면:

### B-4-4

### B-4-5
(a):
(b):
(c):

## 못 끝낸 항목 (증상·관찰·시도)
```
