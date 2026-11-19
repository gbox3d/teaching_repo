# w11_local_storage · 폼 한 객체 저장

출처: [11주 폼 저장](../../../week11_object_localstorage/examples/day2/ex06/README.md) · 권장 8분 · D 브라우저 저장 2점.

## 제공 파일

index.html은 제목·내용과 저장·불러오기·지우기 버튼, 저장 문자열·상태 영역이다. W3.CSS cdnjs 4.1.0과 shared/examples.css를 제공한다. app.js에는 이벤트·값 없음 처리·try/catch·폼 초기화가 있다. 배열 목록을 작성하는 문제가 아니다.

## 할 일

app.js의 세 TODO만 완성한다. key는 week15-memo-form, 객체 필드는 title·memo다.

1. SAVE: 제공된 entry를 JSON 문자열로 바꾸어 key에 저장한다.
2. LOAD: text를 객체로 파싱하고 titleInput.value·memoInput.value를 복원한다.
3. REMOVE: key 하나만 삭제한다. localStorage.clear()는 사용하지 않는다.

## 확인할 것

- 저장값이 없을 때 불러오기는 저장된 값 없음이며 오류가 없다.
- 제목 과제·내용 보고서 제출을 저장하면 JSON 객체 한 개가 표시된다.
- 입력을 바꾸거나 새로고침한 뒤 불러오기를 누르면 두 칸이 복원된다. 새로고침 직후 자동 복원은 요구하지 않는다.
- 다른 키 other-key=keep를 만든 뒤 지우기를 누른다. week15-memo-form만 없어지고 other-key는 남는다.
- Application에서 자기 키 값을 잘못된 JSON으로 바꾸고 불러오기를 누르면 오류 안내가 나온다. 지우기 후 다시 저장하면 복구된다. 오류 처리 코드는 제공한다.

## 실행

폴더 전체를 수업 전에 복사하고 Node.js 24 정적 서버로 연다. 주소는 http://localhost:8000/w11_local_storage/ 이다. 같은 origin 안에서 저장되며 localhost와 Pages의 저장값은 서로 다르다. file:// 저장 동작은 채점 기준으로 사용하지 않는다. 1일차 공개 업로드는 수업 뒤 진행한다.

문제의 key·필드·확인 값은 시험에서 바뀔 수 있다. 해답은 공개하지 않는다. 시작본 버튼의 요청 처리 문구만으로 정답으로 판단하지 않고 저장값과 복원된 입력을 확인한다.
