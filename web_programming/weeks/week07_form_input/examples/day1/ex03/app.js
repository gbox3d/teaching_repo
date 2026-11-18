const form = document.querySelector('#form');
const nameInput = document.querySelector('#name');
const messageInput = document.querySelector('#message');
const result = document.querySelector('#result');

form.addEventListener('submit', function (event) {
  event.preventDefault();
  result.textContent = `${nameInput.value}: ${messageInput.value}`;
});
