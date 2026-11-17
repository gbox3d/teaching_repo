const students = [
    { name: '하늘', score: 80 },
    { name: '바다', score: 60 },
    { name: '노을', score: 90 }
];
const original = document.querySelector('#original');
const stepRows = document.querySelector('#steps');
original.textContent = JSON.stringify(students, null, 2);

document.querySelector('#run-button').addEventListener('click', function () {
    const input = document.querySelector('#empty-array').checked ? [] : students;
    const steps = [];

    const total = input.reduce(function (accumulator, current, index) {
        const next = accumulator + current.score;
        // 실제 콜백이 실행될 때 전달받은 값과 반환할 값을 기록한다.
        steps.push({ step: index + 1, accumulator: accumulator, current: current.score, next: next });
        return next;
    }, 0);

    stepRows.replaceChildren();
    for (const step of steps) {
        const row = document.createElement('tr');
        for (const value of [step.step, step.accumulator, step.current, step.next]) {
            const cell = document.createElement('td');
            cell.textContent = value;
            row.append(cell);
        }
        stepRows.append(row);
    }

    original.textContent = JSON.stringify(students, null, 2);
    document.querySelector('#input-summary').textContent = input.length === 0 ? '[] (빈 배열)' : '학생 3명';
    document.querySelector('#sum').textContent = total;
    document.querySelector('#calls').textContent = steps.length + '회';
    document.querySelector('#status').textContent = steps.length === 0 ? '초깃값 반환 · 콜백 호출 없음' : '합계 계산 완료';
});
