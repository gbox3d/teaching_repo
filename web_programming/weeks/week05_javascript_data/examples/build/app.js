const name = 'student01';
const hour = new Date().getHours();

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

const message = `${greet(name)} ${hello(hour)}`;

console.log(hour);
console.log(message);

document.querySelector('#greeting').textContent = message;
