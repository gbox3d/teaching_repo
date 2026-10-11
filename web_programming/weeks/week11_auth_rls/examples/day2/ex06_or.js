// ex06 || (또는): if 안에서는 "둘 중 하나라도", 값 자리에서는 "앞이 없으면 뒤"
// Console 1~3번을 본다. 4·5행의 두 값(name·message)을 바꿔 가며 새로고침한다.

const name = '하늘';
const message = '';

// 1. if 안의 || — 이름이 비었거나 메시지가 비었으면 참이다
if (name === '' || message === '') {
    console.log('1. 이름과 메시지를 모두 입력하세요.');
} else {
    console.log('1. 둘 다 채웠다.');
}

// 2. 적은 적 없는 키를 꺼내 되살리면 null 이다(getItem 은 ex04, JSON.parse 는 ex05)
const saved = JSON.parse(localStorage.getItem('ex06-none'));
console.log('2. || 없이 :', saved);

// 3. 값 자리의 || — 앞이 null 이면 뒤의 빈 배열 [] 을 쓴다
const items = JSON.parse(localStorage.getItem('ex06-none')) || [];
console.log('3. || [] 를 붙이면 :', items, '/ 개수 :', items.length);

// 4. 주석을 풀면: null 에는 length 가 없다(빨간 줄)
// console.log('4. saved.length :', saved.length);
