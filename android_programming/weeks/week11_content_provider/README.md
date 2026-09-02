# 11주차 — ContentProvider와 센서 이력 경계

## 이번 주 질문

앱의 센서 이력을 다른 컴포넌트나 앱에 노출해야 할 때, 저장소를 직접 열지 않고 어떤 계약으로 안전하게 조회하게 할 수 있을까?

## 측정 가능한 학습 목표

- `ContentResolver → content URI → ContentProvider → 저장소` 호출 경로를 그림과 말로 설명한다.
- collection URI와 item URI를 구분하고, 주어진 URI 6개를 정상·경계·오류로 분류한다.
- 제공된 fake 센서 저장소를 대상으로 projection·selection·sort order를 조합한 조회를 완성한다.
- 알 수 없는 URI, 빈 결과, 잘못된 인자, 읽기 거부가 앱 종료가 아닌 명시적 UI 상태로 나타남을 증명한다.
- 앱 내부 저장과 앱 간 공유의 차이를 `exported` 및 read/write 접근 정책을 포함해 설명한다.

## 1일차 — Provider 계약 읽기

| 구간 | 내용 |
|---|---|
| 설명·라이브 시연 30분 | Provider가 필요한 경우, resolver/provider 경계, authority·path·row ID, MIME type과 접근 범위 |
| 직접 실습 60분 | URI 분류기와 fake resolver로 collection/item 조회, 빈 결과·알 수 없는 URI 검증 |

## 2일차 — 센서 이력 조회와 실패 처리

| 구간 | 내용 |
|---|---|
| 설명·라이브 시연 30분 | projection·selection·정렬, 비동기 조회, 최소 노출과 읽기 전용 계약 |
| 직접 실습 60분 | 센서 이력 필터 UI 연결, 정상·경계·권한 실패 테스트, 계약표 작성 |

두 수업일 모두 정확히 `30분 설명·시연 + 60분 실습`으로 운영한다.

## 선수 지식과 준비물

- 4주차의 RecyclerView 목록, 6주차의 coroutine, 7주차의 `StateFlow`
- 9주차 Service와 10주차 권한·Receiver의 역할 구분
- 강의자가 제공한 starter의 `SensorHistorySource`와 fake 데이터
- Android Studio 기준 프로젝트. 장기 문서에서는 IDE·SDK의 정확한 버전을 고정하지 않는다.

## 자료

- [Marp 슬라이드](slides.md)
- 강의 대본: 강의자 별도 관리(비공개)
- [60분 실습지](lab.md)
- [계약·의사코드 예제](examples/README.md)

## 완료 증거

- collection URI와 item URI 각각의 조회 화면 또는 테스트 로그
- 0건·1건·여러 건 결과를 구분한 검증표
- 알 수 없는 URI와 읽기 거부가 사용자 메시지로 변환된 증거
- 저장소를 UI가 직접 참조하지 않는 호출 경로 그림
- 개인 커밋 SHA와 3문장 회고

## 다음 주

[12주차 — BLE GATT와 연결 상태](../week12_ble_gatt/README.md)에서는 같은 상태·계약 사고를 실제 장치 연결 경계에 적용한다.

## 공식 참고 자료

- [Content provider basics — Android Developers](https://developer.android.com/guide/topics/providers/content-provider-basics)
- [Create a content provider — Android Developers](https://developer.android.com/guide/topics/providers/content-provider-creating)
- [App permissions overview — Android Developers](https://developer.android.com/guide/topics/permissions/overview)
- [Lifecycle-aware coroutines for Views — Android Developers](https://developer.android.com/topic/libraries/architecture/views/coroutines-views)
