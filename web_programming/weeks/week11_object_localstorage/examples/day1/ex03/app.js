// ex03 객체를 목록 한 줄로: 객체를 통째로 글자 자리에 넣으면 [object Object] 가 된다
// 화면의 두 목록을 비교한다. 1번은 객체를 그대로, 2번은 점 표기로 꺼낸 값을 넣었다.

const list1 = document.querySelector('#list1');
const list2 = document.querySelector('#list2');
const items = [];
items.push({ name: '하늘', message: '안녕하세요', date: '2026. 11. 11.' });
items.push({ name: '바다', message: '잘 봤습니다', date: '2026. 11. 11.' });

for (let i = 0; i < items.length; i++) {            // 10주차 목록 그리기: 만들고 → 글자 넣고 → 붙인다
    const li1 = document.createElement('li');
    li1.textContent = items[i];                       // 1. 객체를 그대로 → [object Object]
    list1.append(li1);

    const li2 = document.createElement('li');
    li2.textContent = `${items[i].name}: ${items[i].message} (${items[i].date})`;   // 2. 점 표기로 하나씩
    list2.append(li2);
}
