# 9주차 Service 예제 조각

다음은 강의자 기준 Android 프로젝트에 복사해 lifecycle/thread를 관찰하는 조각이다. **독립적으로 빌드 가능한 Gradle 프로젝트가 아니며**, package, target SDK, notification/foreground service type·permission과 라이브러리 버전은 학기 기준표의 `TBD`를 따른다.

## 1. Service callback thread 관찰

```kotlin
class DemoStatusService : Service() {
    override fun onCreate() {
        super.onCreate()
        Log.d("DemoService", "onCreate thread=${Thread.currentThread().name}")
    }

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        Log.d("DemoService", "onStartCommand thread=${Thread.currentThread().name}")
        startFakeWork()
        return START_NOT_STICKY
    }

    override fun onBind(intent: Intent?): IBinder? = null
}
```

예상 관찰: 기본 설정에서 Activity callback과 Service callback 모두 hosting process의 `main` thread 이름을 남긴다. 따라서 `onStartCommand`에서 blocking I/O를 직접 하면 안 된다.

## 2. Service-owned coroutine

```kotlin
private val serviceJob = SupervisorJob()
private val serviceScope = CoroutineScope(serviceJob + Dispatchers.Default)
private var workerJob: Job? = null

private fun startFakeWork(failAtTick: Int? = null) {
    if (workerJob?.isActive == true) {
        Log.d("DemoService", "duplicate start ignored: worker active")
        return
    }

    workerJob = serviceScope.launch {
        try {
            repeat(4) {
                delay(250)
                if (it == failAtTick) {
                    throw IOException("simulated worker failure at tick=$it")
                }
                Log.d("DemoService", "tick=$it thread=${Thread.currentThread().name}")
            }
        } catch (cancelled: CancellationException) {
            Log.d("DemoService", "worker cancelled")
            throw cancelled
        } catch (error: Exception) {
            Log.e("DemoService", "worker failed", error)
        } finally {
            Log.d("DemoService", "worker cleanup")
        }
    }
}

override fun onDestroy() {
    workerJob?.cancel()
    serviceJob.cancel()
    Log.d("DemoService", "onDestroy")
    super.onDestroy()
}
```

예상 관찰:

- child의 thread가 Service callback의 `main`과 다를 수 있다.
- 중복 `startService()`가 active worker를 발견하면 `duplicate start ignored`를 기록하고 새 child를 만들지 않는다. 완료 뒤의 새 start는 새 worker를 시작한다.
- `failAtTick`을 지정한 fake 실패는 `worker failed → worker cleanup`으로 기록되고 uncaught exception으로 process를 종료하지 않는다.
- Service를 stop하면 child cancellation을 다시 던진 뒤 `worker cleanup`을 실행한다. `onDestroy`와 cleanup 로그의 상대 순서는 비동기 취소 때문에 고정하지 않는다.
- process 강제 종료에서 `onDestroy()` 호출을 절대 보장한다고 가정하지 않는다.

## 3. 내부 전용 manifest 선언

```xml
<service
    android:name=".DemoStatusService"
    android:exported="false" />
```

예상 관찰: 명시적 Intent로 앱 내부에서 시작할 수 있고 다른 앱의 implicit 진입점으로 노출하지 않는다.

## 선택 전 질문

```text
화면 밖에서도 계속되어야 하는가?
사용자가 지속 작업을 인지해야 하는가?
client-server 상호작용이 필요한가?
지연/예약/보장 실행에 더 알맞은 API가 있는가?
blocking 작업을 어느 dispatcher에서 실행·취소할 것인가?
```

Foreground Service 코드는 target SDK별 선언·권한·시작 제한을 확정한 뒤 공식 문서에 맞춰 제공한다. 이 예제에서 임의로 고정하지 않는다.
