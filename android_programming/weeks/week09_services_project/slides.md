---
marp: true
theme: default
paginate: true
header: 모바일프로그래밍 · 9주차
footer: 앱 컴포넌트 비교 · Service와 Fragment
---

# 앱 컴포넌트 비교: Service와 Fragment

2~7주차에 만든 화면은 모두 **Activity**였습니다.
1일차에는 화면이 없는 컴포넌트 **Service**를 직접 넣어 시작·중지해 보고,
2일차에는 화면 한 자리를 갈아 끼우는 **Fragment**를 직접 만들어 봅니다.

```text
1일차: 네 컴포넌트 비교 · Service 세 종류 · LogService 시작·중지
2일차: Fragment 바꿔 끼우기 · Notification 시연·예고
```

---

# 1일차 — 앱 컴포넌트 비교와 Service

`30분 설명·시연 → 60분 실습`

1. Activity·Service·BroadcastReceiver·ContentProvider 한 표로 비교하기
2. Service 세 종류와 `LogService` 코드 읽기
3. `startService`·`stopService`와 Manifest `<service>` 등록
4. Logcat으로 "Service도 메인 스레드에서 돈다" 확인하기

---

## 1일차 · 0–8분 ① — 앱을 이루는 네 가지 컴포넌트

| 컴포넌트 | 무엇 | 언제 쓰나 | 화면 | 예 |
|---|---|---|---|---|
| Activity | 사용자가 보는 화면 하나 | 누르고 입력받을 때 | 있음 | SmartIO 연결 화면 |
| Service | 화면 없이 일을 맡는 것 | 화면을 떠나도 이어져야 할 때 | 없음 | 음악 재생 |
| BroadcastReceiver | 시스템이 보내는 소식을 받는 것 | 배터리·충전 상태가 바뀔 때 | 없음 | 배터리 잔량 표시 |
| ContentProvider | 다른 앱에 데이터를 내주는 창구 | 연락처·사진을 읽을 때 | 없음 | 연락처 앱 |

- 넷 중 화면이 있는 것은 Activity 하나입니다.
- 넷 다 Android가 직접 부를 수 있는 **앱의 입구**입니다.
- 그래서 `AndroidManifest.xml`에 적습니다(BroadcastReceiver는 코드로 등록하기도 합니다).

---

## 1일차 · 0–8분 ② — 이 과목에서 언제 만나나

| 컴포넌트 | 이 과목 | 우리 코드 |
|---|---|---|
| Activity | 2~7주 매주 | `MainActivity`, `ControlActivity` |
| Service | **오늘 1일차** | `LogService` |
| BroadcastReceiver | 10주 | 배터리 변화 받기 |
| ContentProvider | 11주 비교·시연 | 연락처 이름 읽기 |

- 4주차에 Manifest에서 `<activity android:name=".ControlActivity" …>` 줄을 봤습니다.
- 오늘은 그 옆에 `<service android:name=".LogService" …>` 줄이 생깁니다.
- 오늘 넣는 Service는 SmartIO 본줄기가 아닙니다. 10주차는 7주차 완성본에서 다시 시작합니다.

---

## 1일차 · 8–14분 ① — Service 세 종류

| 종류 | 누가 시작하나 | 언제 끝나나 | 사용자에게 보이나 |
|---|---|---|---|
| started | 화면이 `startService(intent)` | `stopService`를 부르거나 스스로 멈출 때 | 보장되지 않음 |
| bound | 화면이 `bindService`로 묶음 | 묶은 화면이 모두 풀릴 때 | 묶은 화면과 함께 |
| foreground | started + 알림 띄우기 | 멈출 때까지 | **알림이 꼭 보인다** |

- 오늘 만드는 것은 **started** 하나입니다. bound·foreground는 이름만 알아 둡니다.
- 음악 앱이 재생 중에 알림을 띄워 두는 것이 foreground Service입니다.
- 사용자가 알고 있는 일이라 시스템이 foreground Service를 쉽게 멈추지 않습니다.

---

## 1일차 · 8–14분 ② — LogService: 화면 없는 컴포넌트

```kotlin
class LogService : Service() {
    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        val name = Thread.currentThread().name
        Log.d("Service", "onStartCommand thread=$name")
        return START_NOT_STICKY
    }
    override fun onDestroy() { … Log.d("Service", "onDestroy") }   // 줄여 적음
    override fun onBind(intent: Intent?): IBinder? { … return null }
}
```

- 7주차 `ConnViewModel : ViewModel()`처럼 `Service()`를 물려받습니다. layout 파일이 없습니다.
- `onStartCommand`: `startService`를 부를 **때마다** 불립니다.
- `onDestroy`: 멈출 때 한 번. `onBind`: 오늘은 `null`을 돌려주는 **틀**입니다.

---

## 1일차 · 14–20분 ① — 시작·중지와 Manifest 등록

```kotlin
binding.serviceStartButton.setOnClickListener {
    val intent = Intent(this, LogService::class.java)
    startService(intent)
}
```

```xml
<service
    android:name=".LogService"
    android:exported="false" />
```

- 4주차 `Intent(this, ControlActivity::class.java)` → `startActivity(intent)`와 같은 모양입니다.
- [서비스 중지]는 같은 두 줄에서 `startService` 자리에 `stopService(intent)`를 씁니다.
- `<service>` 줄이 없어도 **빌드는 됩니다**. 그래도 눌러도 Service가 시작되지 않습니다.

---

## 1일차 · 14–20분 ② — 시연: Service도 메인 스레드에서 돈다

Logcat 필터 `package:mine tag:Service`

| 누른 버튼 | 화면 | Logcat |
|---|---|---|
| [서비스 시작] | 그대로 | `onStartCommand thread=main` |
| [서비스 시작] 한 번 더 | 그대로 | `onStartCommand thread=main` 한 줄 더 |
| [서비스 중지] | 그대로 | `onDestroy` |

- `thread=main`: 5주차에 본 **메인 스레드**와 같은 스레드입니다.
- Service는 "뒤에서 도는 스레드"가 아닙니다. `onStartCommand`에서 `Thread.sleep`하면 화면이 멈춥니다.
- 오래 걸리는 일은 Service 안에서도 5·6주차처럼 스레드·코루틴으로 보냅니다.

---

## 1일차 · 20–26분 ① — 네 컴포넌트를 한 표로 다시

| 컴포넌트 | Manifest 태그 | 누가 시작하나 | 이 과목에서 만드나 |
|---|---|---|---|
| Activity | `<activity>` | 사용자가 앱을 켜거나 `startActivity` | 2주차부터 매주 |
| Service | `<service>` | 화면이 `startService`·`bindService` | 오늘 1일차 |
| BroadcastReceiver | `<receiver>` 또는 코드 등록 | 시스템이 소식을 보낼 때 | 10주차 1일차 |
| ContentProvider | `<provider>` | 다른 앱이 데이터를 물을 때 | 11주차는 쓰기만 |

- Manifest에 적는 자리가 다르고, **누가 불러 주는지**가 다릅니다.
- Activity만 `setContentView`로 화면을 가집니다. 나머지 셋은 화면이 없습니다.
- Service는 `onCreate`·`onDestroy`로, BroadcastReceiver는 `onReceive` 한 번으로, ContentProvider는 `onCreate`로 Android가 불러 줍니다(3주차 생명주기와 같은 생각).

---

## 1일차 · 20–26분 ② — Service를 쓸 자리와 쓰지 않을 자리

| 하려는 일 | 이 과목에서 쓰는 것 |
|---|---|
| 화면을 보는 동안의 기다림(카운트다운, 가짜 연결) | 6주차 코루틴 + 7주차 ViewModel |
| 회전해도 살아 있어야 하는 상태 | 7주차 ViewModel·StateFlow |
| 화면을 떠나도 이어져야 하는 일(음악 재생, 긴 업로드) | Service |
| 사용자에게 계속 보여야 하는 긴 작업 | foreground Service(알림 필수) |

- SmartIO는 학기 끝까지 Service를 쓰지 않습니다. 화면을 보는 동안만 연결하기 때문입니다.
- "화면 없이 도는 일은 모두 Service"가 아닙니다. 기준은 **화면을 떠나도 이어져야 하는가**입니다.
- Service를 쓰더라도 오래 걸리는 일은 그 안에서 또 스레드·코루틴으로 보냅니다.

---

## 1일차 · 26–30분 — 이제 직접 해 보기

[1일차 실습](lab.md#1일차--smartio에-logservice-넣기-60분) · [따라하기](walkthrough.md#1일차)

1. `LogService.kt`를 새로 만들고 함수 세 개(`onStartCommand`·`onDestroy`·`onBind`)를 넣습니다.
2. Manifest `<application>` 안에 `<service>` 세 줄을 적습니다. 이것을 빠뜨리면 로그가 비어 있습니다.
3. [서비스 시작]·[서비스 중지] 버튼을 만들고 `startService`·`stopService`를 부릅니다.
4. Logcat 필터를 `package:mine tag:Service`로 두고 관찰표를 채운 뒤 **캡처 1장**을 남깁니다.

```text
onStartCommand thread=main   ← 두 번 누르면 두 줄
onDestroy                    ← [서비스 중지]
```

**설명 합계: 8+6+6+6+4 = 30분**

---

# 2일차 — Fragment 바꿔 끼우기

`30분 설명·시연 → 60분 실습`

1. Fragment가 Activity 안의 화면 조각이라는 것 보기
2. `FragmentContainerView`로 빈 자리 만들기
3. `onCreateView`로 조각의 화면 돌려주기
4. `beginTransaction()` → `replace()` → `commit()` 세 줄로 바꿔 끼우기

---

## 2일차 · 0–6분 ① — Fragment: Activity 안의 화면 조각

```text
┌ MainActivity ────────────────────┐
│ [첫 번째 조각] [두 번째 조각]     │  ← 그대로 있다
│ ┌ FragmentContainerView ───────┐ │
│ │  여기는 FirstFragment         │ │  ← 이 자리만
│ │  (또는 SecondFragment)        │ │     바꿔 끼운다
│ └──────────────────────────────┘ │
└──────────────────────────────────┘
```

- Fragment는 **자기 layout**(`fragment_first.xml`)을 가진 화면 조각입니다.
- 버튼 줄은 Activity의 것이라 그대로 있고, 빈 자리의 조각만 바뀝니다.
- 4주차 2일차에 예고한 "Activity 안의 화면 조각"을 오늘 직접 만듭니다.

---

## 2일차 · 0–6분 ② — Activity와 Fragment의 역할

| | Activity | Fragment |
|---|---|---|
| Manifest | `<activity>`로 적는다 | 적지 않는다 |
| 화면 정하기 | `onCreate`에서 `setContentView` | `onCreateView`가 View를 돌려준다 |
| 혼자 설 수 있나 | 앱의 입구라서 혼자 선다 | Activity 안에 끼워야 보인다 |
| 바꾸는 방법 | `startActivity`로 새 화면 | `replace`로 자리의 조각만 |

- 오늘 만드는 앱은 Activity **하나**와 조각 **둘**입니다.
- 화면 전체를 넘기면 Activity, 한 자리만 갈아 끼우면 Fragment입니다.
- SmartIO는 학기 끝까지 Activity 두 개로 갑니다. 오늘 연습은 새 프로젝트에서 합니다.

---

## 2일차 · 6–14분 ① — 빈 자리: FragmentContainerView

```xml
<androidx.fragment.app.FragmentContainerView
    android:id="@+id/fragmentContainer"
    android:layout_width="match_parent"
    android:layout_height="0dp"
    android:layout_weight="1" />
```

- 조각을 끼울 **빈 자리**입니다. 처음에는 비어 있습니다.
- `layout_height="0dp"` + `layout_weight="1"`: 버튼 줄을 뺀 남은 높이를 모두 차지합니다(2주차).
- 이 `id`를 코드에서 `R.id.fragmentContainer`로 부릅니다. 철자가 다르면 Kotlin 쪽에 오류가 납니다.
- 자리만 만들고 실행하면 버튼 줄만 보이고 아래는 비어 있습니다.

---

## 2일차 · 6–14분 ② — 조각 클래스와 onCreateView

```kotlin
class FirstFragment : Fragment() {
    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        Log.d("Fragment", "FirstFragment onCreateView")
        return inflater.inflate(R.layout.fragment_first, container, false)
    }
}
```

- `inflater.inflate(…)`가 layout 파일을 View로 만들어 돌려줍니다. Activity의 `setContentView` 자리입니다.
- import는 `androidx.fragment.app.Fragment`입니다. `android.app.Fragment`(옛 방식)를 고르지 않습니다.
- `SecondFragment`는 이 코드에서 layout 이름과 로그 글자만 다릅니다.

---

## 2일차 · 14–22분 ① — 바꾸기 세 줄

```kotlin
binding.secondButton.setOnClickListener {
    val transaction = supportFragmentManager.beginTransaction()
    transaction.replace(R.id.fragmentContainer, SecondFragment())
    transaction.commit()
}
```

```kotlin
if (savedInstanceState == null) {
    … FirstFragment()를 같은 세 줄로 끼운다
}
```

- 바꾸기 시작 → 자리에 조각 넣기 → **확정(commit)**. `commit()`을 빼면 아무것도 바뀌지 않습니다.
- 처음 끼우는 코드는 `if (savedInstanceState == null)` 안에 둡니다.
- 회전 뒤에는 보던 조각을 시스템이 되살립니다(3주차 복원). 그래서 다시 끼우지 않습니다.

---

## 2일차 · 14–22분 ② — 시연: 조각만 바뀐다

Logcat 필터 `package:mine tag:Fragment`

| 조작 | 화면 | Logcat |
|---|---|---|
| 앱 시작 | 버튼 줄 + `여기는 FirstFragment` | `FirstFragment onCreateView` |
| [두 번째 조각] | 버튼 줄 그대로, 글자만 `여기는 SecondFragment` | `SecondFragment onCreateView` |
| 같은 버튼을 두 번 | 글자는 같다 | 누를 때마다 한 줄씩 |
| 조각을 바꾼 뒤 회전 | 보던 조각이 남는다 | 그 조각의 줄 한 개 |

- 같은 버튼을 두 번 누르면 새 조각을 만들어 끼우기 때문에 로그가 두 줄 찍힙니다.
- 뒤로 가기를 누르면 앞 조각으로 가지 않고 앱이 닫힙니다. 조각의 뒤로 가기 기록은 따로 넣어야 생깁니다.

---

## 2일차 · 22–27분 — Notification: 화면 밖에서 알리기

```text
상태 표시줄을 내리면
┌──────────────────────────────────┐
│ Smart I/O Controller             │
│ 연결이 끊겼습니다                │
└──────────────────────────────────┘
```

- 알림(Notification) = 앱 화면을 보고 있지 않은 사용자에게 알리는 것입니다.
- 1일차 Service 표의 셋째 줄, foreground Service는 **알림을 꼭 띄워야** 합니다.
- Android 13부터는 알림을 띄우려면 사용자에게 **권한**을 받아야 합니다.
- 런타임 권한은 10주차 2일차 내용이라, 오늘은 **시연으로만 보고 실습에는 넣지 않습니다**.

---

## 2일차 · 27–30분 — 이제 직접 해 보기

[2일차 실습](lab.md#2일차--fragment-바꿔-끼우기-60분) · [따라하기](walkthrough.md#2일차)

1. 새 프로젝트 `FragmentDemo`(package `com.example.fragmentdemo`)를 만듭니다. SmartIO와 섞지 않습니다.
2. 버튼 두 개와 `FragmentContainerView` 자리를 만들고, 조각 layout 두 개를 만듭니다.
3. `FirstFragment`·`SecondFragment`를 만들어 `onCreateView`에서 자기 layout을 돌려줍니다.
4. 처음 끼우기와 버튼 두 개의 바꾸기 세 줄을 넣고, 조각이 바뀐 **캡처 2장**을 남깁니다.

```text
여기는 FirstFragment      →   여기는 SecondFragment
```

**설명 합계: 6+8+8+5+3 = 30분**

---

## 제출하기

1일차 캡처 한 장, 2일차 캡처 두 장을 남깁니다.

1. **1일차 캡처 1장**: Logcat `tag:Service`에 `onStartCommand thread=main` 두 줄과 `onDestroy` 한 줄이 보이는 화면
2. **2일차 캡처 2장**: `여기는 FirstFragment` 화면과 `여기는 SecondFragment` 화면(버튼 줄이 같은 자리에 있어야 합니다)

파일 이름·제출 위치·마감은 수업 공지를 따릅니다. 캡처에 개인정보가 보이지 않는지 확인합니다.

---

## 다음 주 미리 보기

1일차 표의 셋째 줄, **BroadcastReceiver**를 직접 만듭니다.

- 에뮬레이터의 배터리를 바꾸면 SmartIO 화면의 `배터리 80% · 충전 중`이 따라 바뀌게 합니다.
- 12주차 BLE를 쓰려면 사용자에게 **권한**을 받아야 합니다. 그 흐름을 10주차 2일차에 만듭니다.
- 오늘 본 알림 권한도 같은 런타임 권한입니다. 10주차 시작점은 7주차 완성본입니다.
