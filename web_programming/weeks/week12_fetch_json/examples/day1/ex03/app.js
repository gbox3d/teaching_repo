const url = 'https://jsonplaceholder.typicode.com/todos/1';
const button = document.querySelector('#run-button');
const output = document.querySelector('#output');

button.addEventListener('click', async function () {
  button.disabled = true;
  output.textContent = '불러오는 중';

  try {
    const response = await fetch(url);
    if (!response.ok) throw new Error('HTTP ' + response.status);
    const todo = await response.json();
    output.textContent = todo.title;
  } catch (error) {
    output.textContent = '조회 실패 · ' + error.message;
  } finally {
    button.disabled = false;
  }
});
