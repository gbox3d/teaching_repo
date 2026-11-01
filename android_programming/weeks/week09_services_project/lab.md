# 9주차 실습 — Service 시작·중지와 Fragment 바꿔 끼우기

1일차 60분에는 7주차까지 만든 `SmartIO`에 화면 없는 컴포넌트 `LogService`를 넣고, 버튼으로 시작·중지하며 Logcat에서 스레드 이름을 확인한다.
2일차 60분에는 작은 연습 프로젝트를 새로 만들어 `FragmentContainerView` 자리의 조각을 바꿔 끼운다.
단계별 코드와 넣을 위치는 [따라하기](walkthrough.md)에 있고, 완성 파일은 [예제 설명](examples/README.md)에 있다.

이번 주에 만드는 것은 10주차 시작점이 아니다. 10주차는 7주차 완성본에서 다시 시작하므로, 1일차에 더한 서비스 버튼은 남겨 두어도 되고 지워도 된다.

## 1일차 — SmartIO에 LogService 넣기 (60분)

| 시간 | 할 일 |
|---|---|
| 0–5분 | 7주차까지 만든 `SmartIO`를 열고 실행해 [검색]이 도는지 본다. 없으면 7주차 완성본(`week07/examples/day2`)을 받아 시작한다 |
| 5–15분 | `LogService.kt`를 만든다(1번) |
| 15–22분 | Manifest에 `<service>`를 적는다(2번) |
| 22–35분 | 버튼 두 개를 만든다(3번) |
| 35–45분 | 버튼에서 `startService`·`stopService`를 부른다(4번) |
| 45–55분 | Logcat 관찰표를 채운다(5번) |
| 55–60분 | 캡처 1장을 남기고 오늘 확인할 것을 점검한다(6번) |

### 1. LogService.kt 만들기

`SmartIO`의 package 폴더에 `LogService` 클래스를 새로 만든다(New › Kotlin Class/File › Class).

- 선언은 `class LogService : Service()`다. 7주차 `class ConnViewModel : ViewModel()`과 같은 모양이다.
- 함수 세 개를 넣는다. `onStartCommand`에서 `Thread.currentThread().name`을 `Log.d("Service", …)`로 찍고 `START_NOT_STICKY`를 돌려준다. `onDestroy`에서 로그 한 줄을 찍는다. `onBind`는 `null`을 돌려주는 틀이다.
- `onBind`의 인자와 반환형에 `?`를 붙인다. 붙이지 않으면 `return null` 줄에 오류가 난다.
- 전체 코드는 [따라하기 2단계](walkthrough.md#2-logservicekt-만들기)에 있다. 먼저 스스로 쓰고 비교한다.

| 확인 | 결과 |
|---|---|
| 빨간 글자가 없다 | import 네 줄(`Service`·`Intent`·`IBinder`·`Log`)이 들어 있다 |
| 실행한다 | 화면은 7주차와 같다. 아직 Service를 부르는 버튼이 없다 |

### 2. Manifest에 service 적기

`AndroidManifest.xml`의 `<application>` 안, `</application>` 위에 `<service>`를 적는다.

- `android:name=".LogService"`의 앞 점은 "이 앱 package 안의"라는 뜻이다. 4주차 `.ControlActivity`와 같다.
- `android:exported="false"`는 이 앱 안에서만 쓴다는 뜻이다.
- 이 세 줄을 빠뜨려도 **빌드는 된다**. 나중에 버튼을 눌렀을 때 Logcat이 비어 있으면 먼저 이 줄을 본다.
- 넣을 자리는 [따라하기 3단계](walkthrough.md#3-manifest에-service-적기)에 있다.

### 3. 버튼 두 개 만들기

`strings.xml`에 글자 두 개(`service_start`·`service_stop`)를 넣고, `activity_main.xml` 맨 아래에 버튼 두 개짜리 가로 줄을 넣는다.

- `id`는 `serviceStartButton`·`serviceStopButton`으로 한다. 코드에서 `binding.serviceStartButton`으로 부른다.
- 가로 줄 만들기는 7주차 [검색]·[중지]·[해제] 줄과 같은 모양이다. 그 줄을 복사해 고치면 빠르다.
- 실행해서 화면 맨 아래에 [서비스 시작] [서비스 중지]가 보이면 된다. 아직 눌러도 아무 일이 없다.
- 전체 XML은 [따라하기 4단계](walkthrough.md#4-버튼-두-개-추가하기)에 있다.

이 화면은 가로로 돌리면 맨 아래 줄이 잘릴 수 있다. 오늘 확인은 세로로 한다.

### 4. startService·stopService 연결하기

`MainActivity.kt`의 `onCreate()` 끝에 리스너 두 개를 넣는다.

- 4주차 [연결] 버튼과 같은 모양이다. `Intent(this, LogService::class.java)`를 만들고 `startService(intent)`를 부른다.
- [서비스 중지]는 같은 두 줄에서 `startService` 자리에 `stopService(intent)`를 쓴다.
- `Intent(this, LogService)`처럼 `::class.java`를 빼면 빌드가 안 된다.
- 새 import는 없다. `Intent`는 4주차부터 들어 있고 `LogService`는 같은 package다.
- 넣을 자리와 전체 코드는 [따라하기 5단계](walkthrough.md#5-startservicestopservice-연결하기)에 있다.

### 5. Logcat 관찰표

Logcat 필터를 `package:mine tag:Service`로 두고 순서대로 누르며 마지막 칸을 채운다.

| 조작 | 화면 | Logcat에 찍힌 줄 |
|---|---|---|
| [서비스 시작] | | |
| [서비스 시작] 한 번 더 | | |
| [서비스 중지] | | |
| 멈춘 상태에서 [서비스 중지] 한 번 더 | | |
| [검색] 카운트다운 중에 [서비스 시작] | | |

- 세 번째 줄까지 채우면 `onStartCommand`가 누를 때마다 불리고 `onDestroy`는 멈출 때 한 번 불린다는 것이 보인다.
- 다섯째 줄에서 카운트다운이 끊기지 않는 이유를 한 문장으로 적어 둔다. 6번에서 쓴다.
- 찍힌 스레드 이름이 무엇인지 반드시 읽는다. 이 이름이 오늘의 결론이다.

### 6. 오늘 확인할 것과 캡처

- [ ] Logcat에 `onStartCommand thread=main` 두 줄과 `onDestroy` 한 줄이 순서대로 보인다.
- [ ] `thread=main`이 5주차에 본 메인 스레드와 같은 스레드라는 것을 말할 수 있다.
- [ ] "Service는 따로 스레드를 만들지 않는다"와 "오래 걸리는 일은 스레드·코루틴으로 보낸다"를 각각 한 문장으로 말할 수 있다.
- [ ] 캡처 1장: 앱 화면과 Logcat이 함께 보이거나, Logcat 창만 보이는 캡처. 서비스 시작 줄 두 개·중지 줄 하나·스레드 이름이 모두 읽혀야 한다.

캡처에 계정 이름 같은 개인정보가 보이지 않는지 확인한다.

## 2일차 — Fragment 바꿔 끼우기 (60분)

| 시간 | 할 일 |
|---|---|
| 0–10분 | 새 프로젝트 `FragmentDemo`(package `com.example.fragmentdemo`)를 만들고 ViewBinding을 켠 뒤 `Hello World!`까지 실행한다 |
| 10–20분 | 버튼 두 개와 조각을 끼울 빈 자리를 만든다(1번) |
| 20–30분 | 조각 layout 두 개를 만든다(2번) |
| 30–42분 | 조각 클래스 두 개를 만든다(3번) |
| 42–54분 | 처음 끼우기와 버튼 두 개의 바꾸기 세 줄을 넣는다(4번) |
| 54–60분 | 관찰표를 채우고 캡처 2장을 남긴다(5번) |

새 프로젝트 만들기와 `build.gradle.kts` 설정(ViewBinding 켜기)은 4주차와 같다. 막히면 [따라하기 8단계](walkthrough.md#8-fragmentdemo-새-프로젝트-만들기)를 본다.

### 1. 버튼 줄과 빈 자리 만들기

`strings.xml`에 글자 네 개를 넣고 `activity_main.xml`을 버튼 가로 줄 + 빈 자리로 바꾼다.

- 버튼 `id`는 `firstButton`·`secondButton`, 빈 자리는 `androidx.fragment.app.FragmentContainerView`에 `id`를 `fragmentContainer`로 둔다.
- 빈 자리는 `layout_height="0dp"`와 `layout_weight="1"`로 버튼 줄 아래 남은 높이를 모두 차지하게 한다.
- 실행하면 위에 버튼 두 개가 보이고 아래는 비어 있다. 여기까지가 정상이다.
- 전체 XML은 [따라하기 9단계](walkthrough.md#9-stringsxml과-activity_mainxml)에 있다.

### 2. 조각 layout 두 개 만들기

`res › layout` 폴더에 `fragment_first.xml`과 `fragment_second.xml`을 만든다(New › Layout Resource File).

- 두 파일은 가운데 `TextView` 하나만 있으면 된다. 글자는 `여기는 FirstFragment`·`여기는 SecondFragment`로 구분한다.
- 두 파일의 차이는 `android:text`에 넣은 글자 하나뿐이다. 첫 파일을 복사해 고치면 된다.
- 전체 XML은 [따라하기 10단계](walkthrough.md#10-조각-layout-두-개-만들기)에 있다.

### 3. FirstFragment·SecondFragment 만들기

package 폴더에 클래스 두 개를 만든다(New › Kotlin Class/File › Class).

- 선언은 `class FirstFragment : Fragment()`다. import는 `androidx.fragment.app.Fragment`를 고른다. `android.app.Fragment`를 고르면 뒤에서 오류가 난다.
- `onCreateView`를 재정의하고 `inflater.inflate(R.layout.fragment_first, container, false)`를 돌려준다. 그 위에 `Log.d("Fragment", …)` 한 줄을 찍어 둔다.
- `SecondFragment`는 layout 이름과 로그 글자만 다르다.
- 전체 코드는 [따라하기 11단계](walkthrough.md#11-firstfragmentsecondfragment-만들기)에 있다.

### 4. 끼우고 바꾸기

`MainActivity.kt`를 ViewBinding 틀로 바꾼 뒤 조각을 끼우는 코드와 버튼 리스너 두 개를 넣는다.

- 처음 끼우기는 `if (savedInstanceState == null) { … }` 안에 둔다. 회전 뒤에는 시스템이 보던 조각을 되살리므로 다시 끼우지 않는다.
- 바꾸기는 세 줄이다. `supportFragmentManager.beginTransaction()` → `transaction.replace(R.id.fragmentContainer, SecondFragment())` → `transaction.commit()`.
- `commit()`을 빼도 빌드는 된다. 그러면 눌러도 화면이 바뀌지 않는다. 눌러도 안 바뀌면 이 줄을 먼저 본다.
- 넣을 자리와 전체 코드는 [따라하기 12단계](walkthrough.md#12-mainactivity에서-조각-끼우고-바꾸기)에 있다.

### 5. 관찰표와 캡처 2장

Logcat 필터를 `package:mine tag:Fragment`로 두고 누르며 채운다.

| 조작 | 화면 | Logcat에 찍힌 줄 |
|---|---|---|
| 앱 시작 | | |
| [두 번째 조각] | | |
| [첫 번째 조각] | | |
| 같은 버튼을 두 번 | | |
| 두 번째 조각을 보다가 회전 | | |
| 조각을 바꾼 뒤 뒤로 가기 | | |

- 버튼 줄이 그대로 있고 아래 글자만 바뀌는지 본다. 이것이 "조각만 바꿔 끼운다"의 뜻이다.
- 캡처 2장: 같은 버튼 줄 아래에 `여기는 FirstFragment`가 보이는 화면과 `여기는 SecondFragment`가 보이는 화면.
- 두 캡처에서 버튼 줄이 같은 자리에 있어야 한다. 조각만 바뀐 것을 보여 주는 캡처다.

## 막혔을 때

7주차 코드에서 나는 오류는 [7주차 막혔을 때](../week07_flow_ui_state/lab.md#막혔을-때)를 본다.
아래 표의 오류 문구와 증상은 2026-09-15·16에 Android 14 에뮬레이터와 Kotlin 2.0.21로 확인한 것이다. 쓰는 도구 버전에 따라 문구가 조금 다를 수 있으니, 글자가 똑같지 않아도 밑줄 그어진 이름이 같으면 같은 문제로 본다.

| 상황 | 확인할 것 |
|---|---|
| `Null cannot be a value of a non-null type 'android.os.IBinder'.`가 `return null` 줄에 난다 | (1일차) `onBind`의 반환형을 `IBinder?`로, 인자를 `intent: Intent?`로 바꾼다. `?`가 없는 타입에는 `null`을 넣을 수 없다(3주차). New › Service › Service 메뉴로 만들면 이 모양이 생긴다 |
| `Class 'LogService' is not abstract and does not implement abstract base class member 'onBind'.` | (1일차) `Service`를 물려받으면 `onBind`가 꼭 있어야 한다. `override fun onBind(intent: Intent?): IBinder? { return null }`을 넣는다 |
| `None of the following candidates is applicable:`와 `Classifier 'class LogService : Service' does not have a companion object, so it cannot be used as an expression.` | (1일차) `Intent(this, LogService)`로 썼다. 4주차처럼 `Intent(this, LogService::class.java)`로 쓴다 |
| `Unresolved reference 'serviceStartButton'.` | (1일차) 오류는 Kotlin 파일에 나오지만 원인은 XML이다. `activity_main.xml`의 `android:id="@+id/serviceStartButton"` 철자를 코드와 맞춘다 |
| 빌드는 되는데 [서비스 시작]을 눌러도 Logcat `tag:Service`에 아무것도 찍히지 않는다 | (1일차) `AndroidManifest.xml`의 `<application>` 안에 `<service android:name=".LogService" android:exported="false" />`가 있는지 본다. 필터를 풀면 `Unable to start service … not found` 줄이 보인다 |
| `onStartCommand`에 `Thread.sleep`을 넣었더니 [서비스 시작] 뒤 화면이 멈춘다 | (1일차) 버그가 아니다. Service도 메인 스레드에서 돈다. 멈춘 동안 버튼을 누르면 응답 없음 창이 뜰 수 있다. 관찰했으면 그 줄을 지운다 |
| Service를 시작한 채 뒤로 가기로 앱을 닫았더니 잠시 뒤 Logcat에 `onDestroy`가 찍힌다 | (1일차) 버그가 아니다. Android 8 이상은 백그라운드로 간 앱의 Service를 멈춘다(확인한 에뮬레이터에서는 약 1분 뒤). 관찰은 앱을 연 채로 한다 |
| `Unresolved reference 'Fragment'.`와 `'onCreateView' overrides nothing.` | (2일차) `Fragment`에 커서를 두고 Alt+Enter(맥 ⌥+Enter) → `androidx.fragment.app.Fragment`를 고른다. 첫 줄을 고치면 `MainActivity.kt`의 타입 불일치 오류도 함께 사라진다 |
| `Unresolved reference 'fragmentContainer'.` | (2일차) `activity_main.xml`의 `android:id="@+id/fragmentContainer"` 철자가 코드의 `R.id.fragmentContainer`와 같은지 본다 |
| 빌드는 되는데 [두 번째 조각]을 눌러도 `여기는 FirstFragment` 그대로다 | (2일차) 그 리스너에 `transaction.commit()` 줄이 있는지 본다. 두 버튼의 코드를 나란히 놓고 줄 수를 비교하면 빠진 줄이 보인다 |
| 버튼을 눌러도 아래가 계속 비어 있다 | (2일차) 처음 끼우는 코드와 리스너가 모두 `onCreate()` 안에 있는지, `replace`의 첫 인자가 `R.id.fragmentContainer`인지 본다 |
| 조각을 바꾼 뒤 뒤로 가기를 누르면 앞 조각으로 가지 않고 앱이 닫힌다 | (2일차) 버그가 아니다. 조각의 뒤로 가기 기록은 따로 넣어야 생기며 이번 주 범위 밖이다 |

한 번에 한 곳만 바꾸고 다시 실행한다. 해결되지 않으면 오류 메시지가 보이는 화면을 그대로 보여 주고 도움을 받는다.

## 제출 — 캡처 3장

1. **1일차 캡처 1장**: Logcat `tag:Service`에 `onStartCommand thread=main` 두 줄과 `onDestroy` 한 줄이 보이는 화면
2. **2일차 캡처 2장**: `여기는 FirstFragment`가 보이는 화면과 `여기는 SecondFragment`가 보이는 화면(버튼 줄이 같은 자리에 있어야 한다)

파일 이름·제출 위치·마감은 수업 공지를 따른다. 캡처에 계정·알림 내용 같은 개인정보가 보이지 않는지 확인한다.

## 먼저 끝났다면

- 1일차: `onStartCommand` 안에 `Thread.sleep(5000)`을 넣고 [서비스 시작]을 누른 뒤 화면을 눌러 본다. 어떤 일이 생기는지 적고 그 줄을 지운다. 5주차 시연과 같은 이유다.
- 1일차: [서비스 시작]을 누른 뒤 뒤로 가기로 앱을 닫고 Logcat을 한동안 켜 둔다. `onDestroy`가 언제 찍히는지 적어 둔다.
- 2일차: 조각 layout에 버튼이나 글자를 더 넣어 본다. 조각이 바뀔 때 그 안의 내용이 함께 바뀌는지 본다.
- 2일차: `commit()`을 일부러 지우고 눌러 본다. 오류가 나지 않는 것을 확인한 뒤 되돌린다.
- 2일차: 두 번째 조각을 보는 중에 회전해 보고, 어떤 조각이 남는지와 Logcat에 찍히는 줄을 적어 둔다.

추가 과제는 선택 사항이며 채점하지 않는다.
