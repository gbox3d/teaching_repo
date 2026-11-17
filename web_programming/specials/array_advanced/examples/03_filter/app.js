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
    const minimum = document.querySelector('#minimum-score').valueAsNumber;
    if (!Number.isFinite(minimum)) {
        status.textContent = '최소 점수를 숫자로 입력하세요.';
        return;
    }

    // true를 반환한 학생만 새 배열에 포함한다. 원본에서 삭제하지 않는다.
    const selected = students.filter(function (student) {
        return student.score >= minimum;
    });

    original.textContent = JSON.stringify(students, null, 2);
    result.textContent = JSON.stringify(selected, null, 2);
    document.querySelector('#count').textContent = selected.length + '명';
    status.textContent = selected.length === 0 ? '조건에 맞는 학생 없음' : '필터 완료';
});
