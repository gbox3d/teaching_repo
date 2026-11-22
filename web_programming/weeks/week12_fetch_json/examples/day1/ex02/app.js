const url = 'https://jsonplaceholder.typicode.com/todos/1';
const button = document.querySelector('#run-button');
const output = document.querySelector('#output');

button.addEventListener('click', function () {
  button.disabled = true;
  output.textContent = '불러오는 중';

  fetch(url)
    .then(function (response) {
      if (!response.ok) throw new Error('HTTP ' + response.status);
      return response.json();
    })
    .then(function (todo) {
      console.log(todo);
      output.textContent = todo.title;
    })
    .catch(function (error) {
      output.textContent = '조회 실패 · ' + error.message;
    })
    .finally(function () {
      button.disabled = false;
    });
});
