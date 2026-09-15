# 3주차 실습 — 생명주기 로그와 회전해도 남는 숫자

2주차 `StudentCard` 프로젝트를 이어서 쓴다. 이번 주에는 XML을 고치지 않고 `MainActivity.kt`만 고친다.
모든 단계와 전체 코드는 [따라하기](walkthrough.md)에 있다.

## 1일차 — 생명주기 로그와 Toast (60분)

| 시간 | 할 일 |
|---|---|
| 0–10분 | 2주차 프로젝트를 열어 실행하고 Logcat 창에 `package:mine tag:Life` 필터를 건다 |
| 10–20분 | `onCreate`에 `Log.d`를 넣고 Logcat에 한 줄이 보이는지 확인한다 |
| 20–35분 | 콜백 6개를 추가하고 실행·홈·복귀·회전·뒤로의 순서를 기록표에 적는다 |
| 35–45분 | `+1` 버튼에 Toast를 넣는다 |
| 45–55분 | 회전 때의 Logcat을 캡처하고 기록표를 정리한다 |
| 55–60분 | 프로젝트를 저장하고 오늘 확인할 것을 점검한다 |

### 1. 프로젝트 실행하고 Logcat 열기

1. 2주차 `StudentCard`를 열고 실행해 버튼 세 개가 동작하는지 확인한다.
   없거나 동작하지 않으면 [따라하기 1단계](walkthrough.md#1-2주차-프로젝트-열기)대로 2주차 완성 코드를 넣는다.
2. 아래쪽 **Logcat** 창을 열고 필터 칸에 `package:mine tag:Life`를 입력한다.

### 2. onCreate에 Log.d 넣기

`super.onCreate(savedInstanceState)` 줄 바로 아래에 `Log.d("Life", "onCreate")`를 넣고 실행한다.

- `Log`가 빨간색이면 **Alt+Enter**(맥 ⌥+Enter)로 import한다.
- Logcat에 `onCreate` 한 줄이 보이면 다음 단계로 간다. 안 보이면 필터 철자와 기기 선택을 확인한다.

### 3. 콜백 6개 추가하고 순서 기록표 채우기

[따라하기 4단계](walkthrough.md#4-나머지-콜백-6개-추가하기)의 코드를 `onCreate`의 마지막 `}` 아래에 넣는다.
그다음 아래 다섯 행동을 하나씩 하면서 Logcat에 찍히는 순서를 적는다. 행동마다 Logcat의 휴지통으로 지우고 보면 읽기 쉽다.

| 행동 | 예상 순서 | 실제 순서(Logcat) |
|---|---|---|
| 실행 |  |  |
| 홈 버튼 |  |  |
| 복귀(앱 아이콘 다시 누르기) |  |  |
| 회전 |  |  |
| 뒤로 |  |  |

- 회전에서 `onDestroy` 뒤에 무엇이 오는지 본다. 숫자가 `0`이 되는 이유가 거기에 있다.
- 홈 버튼 뒤 복귀와 회전의 차이를 한 문장으로 적는다.

### 4. +1 버튼에 Toast 넣기

`plusButton.setOnClickListener { }` 안에 `Toast.makeText(this, "지금 숫자: $count", Toast.LENGTH_SHORT).show()`를 넣는다.

- `Toast`가 빨간색이면 import한다.
- `+1`을 누를 때 화면 아래에 `지금 숫자: 1`이 잠깐 보이면 성공이다. 안 보이면 끝의 `.show()`를 확인한다.

### 5. 오늘 확인할 것

- [ ] Logcat에 `package:mine tag:Life` 필터를 걸고 `onCreate`·`onStart`·`onResume`을 보았다.
- [ ] 다섯 행동의 실제 순서를 기록표에 적었다.
- [ ] `+1`을 누르면 Toast가 뜬다.
- [ ] 회전 때의 Logcat을 캡처했다.

프로젝트는 2일차에 그대로 이어서 사용한다. 제출은 2일차 마지막에 한 번만 한다.

## 2일차 — 회전해도 숫자가 남게 (60분)

| 시간 | 할 일 |
|---|---|
| 0–10분 | 1일차 프로젝트를 실행해 `3`을 만들고 회전해 `0`이 되는 것을 다시 본다 |
| 10–20분 | `count`를 class 바로 안으로 옮기고 `onSaveInstanceState`에서 저장한다 |
| 20–35분 | `onCreate`에서 `?.`와 `?:`로 꺼내 화면에 쓴다 |
| 35–45분 | `3` → 회전 → `3`을 확인하고 캡처 2장을 남긴다 |
| 45–55분 | 확인표를 채우고, 시간이 남으면 추가 과제를 한다 |
| 55–60분 | 최종 파일과 캡처를 정리해 제출한다 |

### 1. 문제 다시 보기

실행 → `+1` 세 번 → 회전. 숫자와 Logcat이 어떻게 되는지 한 줄로 적는다.

### 2. count 옮기고 저장하기

1. `onCreate` 안의 `var count = 0` 줄을 지우고, `class MainActivity : AppCompatActivity() {` 바로 아래에 `var count = 0`을 넣는다. 실행해서 전과 같이 동작하는지 본다.
2. `onCreate`의 마지막 `}` 아래에 `onSaveInstanceState`를 추가한다. 매개변수는 `outState: Bundle`이고 `?`가 없다.
   안에서 `super.onSaveInstanceState(outState)`를 먼저 부르고, `outState.putInt("count", count)`로 숫자를 넣는다.
3. `Log.d("Life", "onSaveInstanceState count=$count")`도 넣어 둔다.

- 실행 → `3` → 회전. 숫자는 아직 `0`이지만 Logcat에 `onSaveInstanceState count=3`이 보이면 저장은 성공이다.
- `count`가 빨간색이면 1번에서 class 바로 안으로 옮겼는지 본다.

### 3. onCreate에서 복원하기

`val countText = findViewById<TextView>(R.id.countText)` 줄 위아래에 두 줄을 넣는다.

- 위: `count = savedInstanceState?.getInt("count") ?: 0`
- 아래: `countText.text = "$count"`

힌트:

- `savedInstanceState`는 `Bundle?`이다. 처음 실행에는 null이므로 `.`이 아니라 `?.`로 부른다.
- `?.getInt(...)`의 결과는 `Int?`다. `count`는 `Int`이므로 `?: 0`으로 null일 때 쓸 값을 정해 준다.
- 넣을 때 쓴 이름표 `"count"`와 꺼낼 때 이름표가 같은지 본다.
- 숫자를 꺼냈으면 화면에도 다시 써야 한다.

### 4. 검증하고 캡처하기

| 확인 | 예상 | 실제 |
|---|---|---|
| `+1` 세 번 → 회전 |  |  |
| 회전한 채로 `+1` 한 번 |  |  |
| 홈 버튼 → 복귀 |  |  |
| 뒤로 → 앱 다시 실행 |  |  |

- **캡처 1**: 회전한 뒤에도 `3`이 보이는 화면
- **캡처 2**: 회전할 때 `onSaveInstanceState count=3` → `onDestroy` → `onCreate`가 찍힌 Logcat

마지막 줄이 `0`으로 돌아가는 것은 정상이다. 뒤로로 끝낸 앱은 저장하지 않는다.

## 막혔을 때

| 상황 | 확인할 것 |
|---|---|
| `Unresolved reference 'Log'.` 오류 | `Log`에 커서를 두고 **Alt+Enter**(맥 ⌥+Enter)로 import한다. `import android.util.Log`가 생겨야 한다 |
| `Unresolved reference 'Toast'.` 오류 | 같은 방법으로 import한다. `import android.widget.Toast` |
| `'onStart' hides member of supertype 'AppCompatActivity' and needs an 'override' modifier.` 오류 | `fun onStart()` 앞에 `override`를 붙인다 |
| 실행하자마자 앱이 꺼지는데 Logcat에 아무것도 없다 | 필터에서 `tag:Life`를 지우고 `package:mine`만 남긴 뒤 빨간 줄(`FATAL EXCEPTION`)을 읽는다. `did not call through to super.onStart()`가 보이면 그 콜백 안의 `super.onStart()` 줄을 지운 것이다. 되살린다. 다 읽으면 필터를 `package:mine tag:Life`로 되돌린다 |
| `'onSaveInstanceState' overrides nothing.` 오류 | 매개변수를 `outState: Bundle`로 쓴다. `Bundle?`이 아니다 |
| `Only safe (?.) or non-null asserted (!!.) calls are allowed on a nullable receiver of type 'android.os.Bundle?'.` 오류 | `savedInstanceState.getInt`를 `savedInstanceState?.getInt`로 바꾼다. `!!`는 쓰지 않는다 |
| `Assignment type mismatch: actual type is 'kotlin.Int?', but 'kotlin.Int' was expected.` 오류 | 끝에 `?: 0`을 붙인다 |
| `onSaveInstanceState` 안에서 `Unresolved reference 'count'.` 오류 | `var count = 0`이 아직 `onCreate` 안에 있다. class 바로 안으로 옮긴다 |
| 빌드는 되는데 회전하면 `0`이 된다 | Logcat에 `onSaveInstanceState count=3`이 보이는지 본다. 보이면 꺼낼 때 이름표 철자(`"count"`)가 다르거나 `countText.text = "$count"`가 빠진 것이다 |
| Logcat에 아무것도 안 보인다 | 필터가 `package:mine tag:Life`인지, Logcat 왼쪽 위의 기기가 실행 중인 에뮬레이터인지 본다 |
| 화면이 돌지 않는다 | 에뮬레이터 화면 위쪽을 아래로 끌어 빠른 설정에서 **자동 회전**을 켠다 |
| 노란색 경고 표시가 있다 | 실행에는 문제가 없다. 빨간 오류부터 해결한다 |

한 번에 한 곳만 바꾸고 다시 실행한다. 해결되지 않으면 오류 메시지가 보이는 화면을 그대로 보여 주고 도움을 받는다.

## 제출 — 세 가지

1. **`MainActivity.kt`**: 콜백 7개 로그, Toast, 저장·복원이 있는 최종 코드
2. **캡처 1**: 회전한 뒤에도 숫자 `3`이 보이는 화면
3. **캡처 2**: 회전할 때 `onSaveInstanceState count=3`이 찍힌 Logcat

콜백 로그와 Toast까지 되면 기본 성공이다. 저장·복원은 예제와 도움을 받아 마무리해도 된다.
제출 위치와 마감은 수업 공지를 따른다.

## 먼저 끝났다면

- 2일차: 이름 TextView의 글자도 저장해 본다. `onSaveInstanceState`에서 `outState.putString("name", …)`으로 넣고,
  `onCreate`에서 `val savedName = savedInstanceState?.getString("name")`으로 꺼낸다. 꺼낸 값이 null이면 지금처럼 `"이름: $name"`을 쓴다.
  화면은 회전 전후가 같아 보이므로 Logcat 줄로 확인한다. `Log.d("Life", "저장된 이름: $savedName")`을 넣으면
  처음 실행에는 `null`, 회전 뒤에는 저장한 글자가 찍힌다.
- 2일차: 회전 뒤 복원했을 때만 Toast `복원했습니다`를 띄워 본다. `savedInstanceState`가 null이 아닐 때가 복원한 때다. 1주차 `if`를 쓴다.
  힌트: `if (savedInstanceState != null) { … }` — `!=`는 "같지 않다"라는 뜻이다.

추가 과제는 선택 사항이다.
