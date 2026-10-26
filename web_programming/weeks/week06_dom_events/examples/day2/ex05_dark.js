// ex05 다크 모드: 색은 CSS 에 미리 적어 두고, JS 는 body 의 class 만 뒤집는다

const darkButton = document.querySelector('#btn-dark');

darkButton.addEventListener('click', function () {
    document.body.classList.toggle('dark');   // document.body 는 <body> 요소. 찾지 않고 바로 쓴다
});
