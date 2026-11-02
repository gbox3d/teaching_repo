// ex10 new Date(): 지금 시각을 담은 값
// Console 에 1~6번이 찍힌다. 새로고침할 때마다 다시 잰다.
//   1. now.getHours()     — 시, 0~23
//   2. now.getMinutes()   — 분, 0~59
//   3. now.getFullYear()  — 연도
//   4. now.getMonth()     — 월. 0부터 센다(1월이 0)
//   5. now.getMonth() + 1 — 사람이 읽는 월
//   6. now.getDay()       — 요일, 0 = 일요일

const now = new Date();     // 이 줄이 실행된 순간의 날짜·시각을 담은 값
console.log('now :', now);
console.log('1. now.getHours() →', now.getHours());     // 값에게 "몇 시야?"를 묻는다
console.log('2. now.getMinutes() →', now.getMinutes());
console.log('3. now.getFullYear() →', now.getFullYear());
console.log('4. now.getMonth() →', now.getMonth());
console.log('5. now.getMonth() + 1 →', now.getMonth() + 1);
console.log('6. now.getDay() →', now.getDay());
// web-week05 의 new Date().getHours() 는 위 두 줄(now 만들기 → getHours)을 한 줄로 이어 쓴 것이다
