# 6주차 예제

## starter

[starter/index.html](starter/index.html)은 의미 있는 HTML과 CSS, DOM 참조, submit 관찰 코드까지만 제공한다. CRUD 핵심은 `starter/app.js`의 `TODO`를 따라 직접 구현한다.

```bash
cd starter
python -m http.server 8000
```

브라우저에서 `http://localhost:8000`을 열고 Console을 함께 본다.

## 관찰 순서

1. 빈 입력과 정상 입력을 제출해 현재 starter의 상태 문구를 비교한다.
2. Elements에서 `#todo-list`, `#empty-message`, `#status`를 찾는다.
3. Console에서 selector 오타가 `null`을 반환하는지 확인한다.
4. Application → Local Storage에서 `todos:v1` key를 관찰한다.

starter는 완성 답안이 아니다. 요구사항과 검증표는 [실습 문서](../lab.md)를 따른다.
