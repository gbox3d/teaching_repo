const students = [
    { name: '하늘', score: 80 },
    { name: '바다', score: 60 },
    { name: '노을', score: 90 }
];
const original = document.querySelector('#original');
const result = document.querySelector('#result');
const status = document.querySelector('#status');
original.textContent = JSON.stringify(students, null, 2);

document.querySelector('#run-button').addEventListener('click', function () {
    const bonus = document.querySelector('#bonus').valueAsNumber;
    if (!Number.isFinite(bonus)) {
        status.textContent = '가산점을 숫자로 입력하세요.';
        return;
    }

    // 매번 원본으로 계산하고 새 객체를 만든다. student.score에는 대입하지 않는다.
    const adjusted = students.map(function (student) {
        return { name: student.name, score: student.score + bonus };
    });

    original.textContent = JSON.stringify(students, null, 2);
    result.textContent = JSON.stringify(adjusted, null, 2);
    document.querySelector('#count').textContent = adjusted.length + '명';
    status.textContent = '변환 완료';
});
