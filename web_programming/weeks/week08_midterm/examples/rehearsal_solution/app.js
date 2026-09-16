// 중간 실기 리허설 — app.js

const noticeButton = document.querySelector('#notice-button');
const noticeText = document.querySelector('#notice-text');
const darkButton = document.querySelector('#dark-button');

noticeButton.addEventListener('click', function () {
  noticeText.textContent = '이번 주 모임: 금요일 오후 5시';
});

darkButton.addEventListener('click', function () {
  document.body.classList.toggle('dark');
});

const joinForm = document.querySelector('#join-form');
const nameInput = document.querySelector('#name');
const reasonInput = document.querySelector('#reason');
const result = document.querySelector('#result');

joinForm.addEventListener('submit', function (event) {
  event.preventDefault();
  const name = nameInput.value.trim();
  const reason = reasonInput.value.trim();

  if (name === '') {
    result.textContent = '이름을 입력하세요';
    nameInput.focus();
    return;
  }

  result.textContent = `${name}: ${reason}`;
  joinForm.reset();
  nameInput.focus();
});

console.log('리허설 해답 준비 완료');
