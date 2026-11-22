const messageButton = document.querySelector('#message-button');
const errorButton = document.querySelector('#error-button');
const output = document.querySelector('#output');

function wait(ms) {
  return new Promise(function (resolve) {
    setTimeout(function () {
      resolve();
    }, ms);
  });
}

async function makeMessage() {
  await wait(1000);
  return '1초 타이머 완료';
}

async function makeError() {
  await wait(1000);
  throw new Error('타이머 실패');
}

messageButton.addEventListener('click', async function () {
  messageButton.disabled = true;
  errorButton.disabled = true;
  output.textContent = '1. makeMessage() 호출\n';

  const promise = makeMessage();
  console.log(promise);
  output.textContent += '2. 다음 줄 먼저 실행\n';

  const message = await promise;
  output.textContent += `3. 받은 값: ${message}\n`;

  messageButton.disabled = false;
  errorButton.disabled = false;
});

errorButton.addEventListener('click', async function () {
  messageButton.disabled = true;
  errorButton.disabled = true;
  output.textContent = '1. makeError() 호출\n';

  try {
    await makeError();
  } catch (error) {
    output.textContent += `2. 실패 이유: ${error.message}\n`;
  } finally {
    messageButton.disabled = false;
    errorButton.disabled = false;
  }
});
