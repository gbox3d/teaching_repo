const students = [
    { name: '하늘', score: 80 },
    { name: '바다', score: 60 },
    { name: '노을', score: 90 }
];
const resultList = document.querySelector('#result-list');
const returnOutput = document.querySelector('#return-output');
const afterJson = document.querySelector('#after-json');
const status = document.querySelector('#status');
document.querySelector('#source-json').textContent = JSON.stringify(students, null, 2);

document.querySelector('#for-of').addEventListener('click', function () {
    resultList.replaceChildren();
    for (const student of students) {
        const item = document.createElement('li');
        item.textContent = `${student.name}: ${student.score}점`;
        resultList.append(item);
    }
    returnOutput.textContent = '해당 없음 (반복문)';
    afterJson.textContent = JSON.stringify(students, null, 2);
    status.textContent = 'for...of 실행 완료';
});

document.querySelector('#for-each').addEventListener('click', function () {
    resultList.replaceChildren();
    const result = students.forEach(function (student) {
        const item = document.createElement('li');
        item.textContent = `${student.name}: ${student.score}점`;
        resultList.append(item);
    });
    returnOutput.textContent = String(result);
    afterJson.textContent = JSON.stringify(students, null, 2);
    status.textContent = 'forEach 실행 완료';
});
