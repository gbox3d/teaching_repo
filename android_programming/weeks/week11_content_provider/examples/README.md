# 11주차 예제 — Provider 계약 스케치

이 폴더의 코드는 **설계 토론과 starter 연결을 위한 Kotlin/XML 의사코드**다. 패키지, import, Manifest, Gradle 의존성을 갖춘 빌드 가능한 Android 프로젝트가 아니며 그대로 붙여 넣지 않는다.

## 1. 호출 경계

Android 호출 형태를 먼저 읽는다.

```kotlin
val cursor = context.contentResolver.query(
    readingsUri,
    arrayOf("_id", "recorded_at", "channel", "value"),
    "channel = ?",
    arrayOf(selectedChannel),
    "recorded_at DESC",
)
```

위 코드는 import·null 처리·cursor 변환·dispatcher를 생략한 API 형태 스케치다. 실제로 느릴 수 있는 Provider query는 메인 스레드 밖에서 실행한다.

수업 lab은 아래 fake 가능 계약으로 같은 입력·결과를 연습한다.

```kotlin
interface HistoryClient {
    suspend fun query(request: HistoryQuery): HistoryResult
}

data class HistoryQuery(
    val target: HistoryTarget,
    val columns: Set<HistoryColumn>,
    val channel: String?,
    val newestFirst: Boolean,
)

sealed interface HistoryTarget {
    data object Collection : HistoryTarget
    data class Item(val id: Long) : HistoryTarget
    data class Unknown(val rawUri: String) : HistoryTarget
}

sealed interface HistoryResult {
    data class Rows(val rows: List<SensorRow>) : HistoryResult
    data object NotFound : HistoryResult
    data class Failed(val kind: HistoryFailure) : HistoryResult
}

enum class HistoryFailure { UNSUPPORTED_URI, ACCESS_DENIED, QUERY_FAILED }
```

`Collection` 0건은 `Rows(emptyList())`, 존재하지 않는 `Item`은 `NotFound`, 계약 밖 URI는 `Unknown(rawUri)`를 거쳐 `Failed(UNSUPPORTED_URI)`가 된다. 실제 `ContentResolver` 세부 호출은 강의자가 제공하는 adapter 내부에 있고, 학생 코드는 이 계약의 입력·결과·상태를 설명한다.

## 1-1. Provider 쪽 URI·MIME 스케치

```kotlin
private val matcher = UriMatcher(UriMatcher.NO_MATCH).apply {
    addURI(AUTHORITY, "readings", READINGS)
    addURI(AUTHORITY, "readings/#", READING_ID)
}

override fun query(uri: Uri, /* projection, selection, args, sort */): Cursor? =
    when (matcher.match(uri)) {
        READINGS -> repository.queryCollection(/* ... */)
        READING_ID -> repository.queryItem(uri.lastPathSegment /* ... */)
        else -> error("unsupported URI")
    }

override fun getType(uri: Uri): String = when (matcher.match(uri)) {
    READINGS -> "vnd.android.cursor.dir/vnd.edu.example.reading"
    READING_ID -> "vnd.android.cursor.item/vnd.edu.example.reading"
    else -> error("unsupported URI")
}
```

이 역시 메서드 시그니처 일부와 오류 정책을 축약한 의사코드다. 실제 authority·MIME은 starter에서 확인한다.

## 1-2. CRUD 표면 비교

| Provider 진입점 | 일반적 의미 | 이번 외부 센서 이력 계약 |
|---|---|---|
| `query` | 행 조회 | 허용할 후보 |
| `insert` | 새 행 생성 | 허용하지 않음 |
| `update` | 기존 행 변경 | 허용하지 않음 |
| `delete` | 행 제거 | 허용하지 않음 |

내부 센서 수집기가 기록하는 저장 경로와 외부 client가 Provider를 통해 접근하는 경로는 같은 권한 표면이 아니다.

## 2. UI 상태

```kotlin
sealed interface HistoryUiState {
    data object Loading : HistoryUiState
    data class Data(val rows: List<SensorRow>) : HistoryUiState
    data object Empty : HistoryUiState
    data object NotFound : HistoryUiState
    data class Error(val message: String, val canRetry: Boolean) : HistoryUiState
}
```

## 3. XML View 역할 스케치

```xml
<!-- 구조 스케치: 실제 id/style/string resource는 starter 기준 -->
<LinearLayout>
    <Spinner android:id="@+id/channelFilter" />
    <ProgressBar android:id="@+id/loading" />
    <TextView android:id="@+id/statusMessage" />
    <androidx.recyclerview.widget.RecyclerView android:id="@+id/historyList" />
    <Button android:id="@+id/retryButton" />
</LinearLayout>
```

## 4. 계약 테스트 표본

| case | target | fake result | expected UI |
|---|---|---|---|
| normal-many | `Collection` | `Rows(3 rows)` | `Data(3)` |
| boundary-empty | `Collection` | `Rows(emptyList())` | `Empty` |
| boundary-missing | `Item(404)` | `NotFound` | `NotFound` |
| failure-unknown | `Unknown("content://…/unknown")` | `Failed(UNSUPPORTED_URI)` | `Error`, no retry |
| failure-denied | `Collection` | `Failed(ACCESS_DENIED)` | `Error`, policy 안내 |

위 `HistoryTarget`과 `HistoryResult`가 수업용 공개 계약이다. 실제 starter의 패키지·이름은 달라도 `collection 0건`, `item 없음`, `지원하지 않는 URI`의 세 의미를 하나의 빈 목록으로 뭉개지 않는다.

## 5. 학생이 채울 계약표

| 항목 | 확정값 |
|---|---|
| authority | 강의자 starter에서 확인 |
| collection path | 강의자 starter에서 확인 |
| item ID 형식 | 강의자 starter에서 확인 |
| 읽기 허용 범위 | 수업 정책에서 확인 |
| 쓰기 허용 범위 | 수업 정책에서 확인 |
| 공개 열 | 실습에서 결정 |

## 공식 자료

- [Content provider basics](https://developer.android.com/guide/topics/providers/content-provider-basics)
- [Create a content provider](https://developer.android.com/guide/topics/providers/content-provider-creating)
