// ex01 지금 실행 vs 클릭할 때 실행: 이 파일은 위에서 아래로 한 번 실행된다
// F12 › Console 에서 A·B·C 가 찍히는 순서를 본다. 버튼을 여러 번 눌러 본다.

console.log('A. 페이지를 열자마자 실행된다');
// 제공 출력 코드
const result = document.querySelector('#result');
result.textContent = 'A. 페이지 실행';
// 버튼을 찾아(찾는 법은 ex09) 클릭할 때 할 일을 등록만 해 둔다
document.getElementById('btn').addEventListener('click', function () {
    console.log('B. 버튼을 누를 때마다 실행된다');
    result.textContent += '\nB. 클릭 실행';
});
console.log('C. A 바로 다음에 실행된다. B 보다 먼저');
// 작년 예제는 function () { } 대신 () => { } 로 썼다. 여기서는 뜻이 같다

result.textContent += '\nC. A 다음 실행';
