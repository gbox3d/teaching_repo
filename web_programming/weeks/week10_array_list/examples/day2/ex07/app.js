// ex07 삭제 버튼 틀: 줄마다 [삭제] 버튼을 붙인다. 누르면 배열에서 하나 빼고 다시 그린다
// 가운데 줄의 [삭제]를 눌러 남은 줄, "N개", Console 의 items 를 본다.

const list = document.querySelector('#list');
const count = document.querySelector('#count');
let items = ['student01: 안녕하세요', 'student02: 고맙습니다', 'student03: 반갑습니다'];

function showList() {                               // 비우고 다시 그리는 함수(ex06)
    list.innerHTML = '';                            // 비운다(ex05 2번)
    for (let i = 0; i < items.length; i++) {        // 처음부터 끝까지(ex02 2번)
        const li = document.createElement('li');    // 한 줄씩 만들어 붙인다(ex03)
        li.textContent = items[i];
        // ↓ 삭제 버튼 틀(일곱 줄). 그대로 옮겨 쓴다. showList() 가 다시 그릴 때 버튼마다 번호를 새로 붙인다
        const removeButton = document.createElement('button');
        removeButton.textContent = '삭제';
        removeButton.addEventListener('click', function () {
            items.splice(i, 1);              // 1. 배열에서 i 번째 하나를 뺀다
            showList();                      // 2. 바뀐 배열대로 다시 그린다
        });
        li.append(removeButton);             // 3. 버튼을 그 줄(li) 안에 붙인다
        // ↑ 삭제 버튼 틀 끝
        list.append(li);                            // 줄을 목록에 붙인다(ex03)
    }
    count.textContent = `${items.length}개`;        // 개수는 배열의 length(ex04 3번)
    console.log('그린 뒤 items :', items);
}

showList();                                         // 열 때 한 번 그린다(ex06 1번)
