// defer 유무에 따라 이 줄이 실행되는 시점이 다르다.
console.log('3. defer 로 연결한 파일 :', document.body);
scriptResults += document.body === null ? ' → 3: null' : ' → 3: body';
