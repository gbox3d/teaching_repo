const name = 'student01';
const hour = new Date().getHours();

function greet(name) {
  return '이름 연결 전'; // 수정 1: name을 넣은 템플릿 문자열
}

function hello(hour) {
  if (hour >= 24) { // 수정 2: 오후 시작 시각
    return '좋은 오후입니다.';
  } else {
    return '좋은 아침입니다.';
  }
}

const message = `${greet(name)} ${hello(hour)}`;

console.log(hour);
console.log(message);

document.querySelector('#greeting').textContent = '출력 연결 전'; // 수정 3: message 출력
