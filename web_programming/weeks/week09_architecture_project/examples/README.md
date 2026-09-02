# 9주차 프로젝트 starter

`project-starter`는 static JSON을 module 경계 뒤에서 읽는 walking skeleton이다. UI는 JSON 경로를 모르고 `listItems()`의 반환값만 사용한다.

## 실행

```bash
cd project-starter
python -m http.server 8000
```

`http://localhost:8000`을 열고 Network에서 `items.json` 요청을 확인한다.

## 시작 방법

1. starter 전체를 자신의 프로젝트 폴더에 복사한다.
2. `docs/architecture.md`의 placeholder를 먼저 채운다.
3. `data/items.json`과 data contract를 자신의 entity로 바꾼다.
4. UI 문구와 카드 field를 같은 scope로 맞춘다.
5. empty 배열과 없는 URL을 각각 검증한다.

다음 주에는 `js/data-source.js` 내부만 Supabase 호출로 바꾸는 것이 목표다.
