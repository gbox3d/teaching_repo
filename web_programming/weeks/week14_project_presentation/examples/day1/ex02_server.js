// ex02 로컬 시연은 서버로: fetch 는 서버(http://)나 공개 주소(https://)로 연 페이지에서만 파일을 읽는다
// 같은 페이지를 node server.mjs 로 열 때(http://localhost:8000/, 1번)와 두 번 눌러 열 때(file://, 2번)를 비교한다.

const result = document.querySelector('#result');

async function loadMessage() {                     // 12주 ex05 와 같은 try / catch 모양(response.ok 검사는 뺐다)
    try {
        const response = await fetch('ex02_message.json');
        const data = await response.json();
        // 1. 서버로 열면 파일을 읽어 글을 넣는다
        result.textContent = data.message;
        console.log('1. 서버로 열어 읽었다 :', data.message);
    } catch (error) {
        // 2. 두 번 눌러 열면 파일을 읽지 못해 여기로 온다
        result.textContent = '읽지 못했습니다.';
        console.log('2. 읽지 못했다');
    }
}

loadMessage();
