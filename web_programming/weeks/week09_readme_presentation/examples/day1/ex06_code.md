<!-- ex06 소스 코드: 짧은 코드는 백틱 하나로 감싸고, 여러 줄은 백틱 세 개 줄 사이에 넣는다 -->
<!-- 2·3번은 코드가 같고 여는 줄의 언어 이름만 다르다. 코드 안의 기호는 모양으로 바뀌지 않는다 -->

1번 — 문장 안의 짧은 코드는 백틱 하나로 감싼다:

버튼을 찾을 때는 `document.querySelector` 를 쓴다.

2번 — 여러 줄은 백틱 세 개 줄 사이에. 언어 이름이 없다:

```
const button = document.querySelector('#hello-button');
button.addEventListener('click', function () {
  console.log('눌렀다');
});
```

3번 — 2번과 같은 코드. 여는 줄에 언어 이름 js:

```js
const button = document.querySelector('#hello-button');
button.addEventListener('click', function () {
  console.log('눌렀다');
});
```

4번 — 코드 블록 안에서는 마크다운 기호도 글자 그대로다:

```text
# 이 줄은 제목이 아니다
- 이 줄은 목록이 아니다
```
