// 수업 전 이 파일을 개인 web-week06의 app.js로 복사한다.
const name = 'student01';
const hour = new Date().getHours();
const greeting = document.querySelector('#greeting');
const countBox = document.querySelector('#count');
const helloButton = document.querySelector('#hello-button');
const darkButton = document.querySelector('#dark-button');
let count = 0;

function greet(name) {
  return `안녕하세요, ${name}님!`;
}

function hello(hour) {
  if (hour >= 12) {
    return '좋은 오후입니다.';
  } else {
    return '좋은 아침입니다.';
  }
}

function countUp() {
  count = count + 1;
  countBox.textContent = `클릭 ${count}회`;
}

greeting.textContent = `${greet(name)} ${hello(hour)}`;

helloButton.addEventListener('click', function () {
  greeting.textContent = '반갑습니다. 오늘도 좋은 하루 되세요.';
  // TODO: countUp 함수를 호출한다.
});

darkButton.addEventListener('click', function () {
  // TODO: body의 dark 클래스를 toggle한다.
  // TODO: countUp 함수를 호출한다.
});
