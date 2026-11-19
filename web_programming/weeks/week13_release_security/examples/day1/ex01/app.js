const form = document.querySelector('#example-form');
const messageInput = document.querySelector('#message');
const output = document.querySelector('#output');
form.addEventListener('submit', function (event) {
  event.preventDefault();
  const item = { book_id: 'student01', name: 'student01', message: messageInput.value };
  const body = JSON.stringify(item);
  output.textContent = body;
});
