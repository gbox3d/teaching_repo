// ex05 다시 그리기: 목록을 비우고(innerHTML = '') 배열 전체를 처음부터 그린다
// 배열은 늘 세 개다. 1번과 2번 버튼을 몇 번씩 눌러 화면의 줄 수와 Console 을 비교한다.

const list = document.querySelector('#list');
let items = ['student01: 안녕하세요', 'student02: 고맙습니다', 'student03: 반갑습니다'];

// 1. 비우지 않고 그리기 — 앞에 그린 줄이 남아 누를 때마다 세 줄씩 늘어난다
document.querySelector('#btn-1').addEventListener('click', function () {
    for (let i = 0; i < items.length; i++) {        // 처음부터 끝까지(ex02 2번)
        const li = document.createElement('li');    // 한 줄씩 만들어 붙인다(ex03)
        li.textContent = items[i];
        list.append(li);
    }
    console.log('1. 비우지 않고 그렸다. 배열은', items.length, '개');
});

// 2. 비우고 그리기 — 몇 번을 눌러도 배열과 같은 세 줄이다
document.querySelector('#btn-2').addEventListener('click', function () {
    list.innerHTML = '';                            // 목록을 통째로 비운다. 이 수업에서 innerHTML 은 비우기에만 쓴다
    for (let i = 0; i < items.length; i++) {        // 처음부터 끝까지(ex02 2번)
        const li = document.createElement('li');    // 한 줄씩 만들어 붙인다(ex03)
        li.textContent = items[i];
        list.append(li);
    }
    console.log('2. 비우고 그렸다. 배열은', items.length, '개');
});
