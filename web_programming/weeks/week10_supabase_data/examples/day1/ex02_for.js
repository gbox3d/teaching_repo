// ex02 for: i 를 0 부터 하나씩 올리며 배열을 처음부터 끝까지 훑는다
// Console 에 1번 세 줄, 2번 네 줄이 찍힌다. 몇 번째인지(i)와 그 값(items[i])을 함께 본다.

let items = ['student01: 안녕하세요', 'student02: 고맙습니다', 'student03: 반갑습니다'];   // 처음 값을 넣어 만든 배열(ex01 6번)
items.push('student04: 또 왔습니다');        // 하나 더 넣어 이제 4개다(ex01)

// for (시작; 계속할 조건; 한 바퀴 끝날 때마다) — i++ 는 i = i + 1 과 같다
// 1. 끝을 숫자 3 으로 적었다 — 넷째 값을 빠뜨린다
for (let i = 0; i < 3; i++) {
    console.log('1.', i, items[i]);
}

// 2. 끝을 items.length 로 적었다 — 몇 개가 들어 있든 끝까지 간다
for (let i = 0; i < items.length; i++) {
    console.log('2.', i, items[i]);
}
