// ex06 showList: 목록·안내 문장·개수를 모두 배열에서 다시 만드는 함수 하나
// 열자마자 1번이, [더하기]를 누를 때마다 2번이 showList() 를 부른다. 배열이 비었을 때와 찼을 때를 비교한다.

const textInput = document.querySelector('#text');
const list = document.querySelector('#list');
const empty = document.querySelector('#empty');
const count = document.querySelector('#count');
let items = [];

function showList() {
    list.innerHTML = '';                            // 비운다(ex05 2번)
    for (let i = 0; i < items.length; i++) {        // 처음부터 끝까지(ex02 2번)
        const li = document.createElement('li');    // 한 줄씩 만들어 붙인다(ex03)
        li.textContent = items[i];
        list.append(li);
    }
    count.textContent = `${items.length}개`;        // 개수는 for 밖에서 한 번 쓴다(ex04)
    if (items.length === 0) {                       // 비었으면 안내 문장을 쓰고, 있으면 지운다(5주 ex07)
        empty.textContent = '아직 남긴 글이 없습니다.';
    } else {
        empty.textContent = '';
    }
}

// 1. 열 때 한 번 그린다 — 배열이 비어 있어 안내 문장과 0개
showList();
console.log('1. 열 때 그렸다 :', items.length, '개');

// 2. [더하기]를 누를 때마다 배열에 넣고 다시 그린다
document.querySelector('#add').addEventListener('click', function () {
    items.push(textInput.value);
    showList();
    console.log('2. 넣고 다시 그렸다 :', items.length, '개');
});
