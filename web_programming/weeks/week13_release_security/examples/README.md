# Week 13 audit examples

## security-demo.html

같은 입력을 textContent와 innerHTML로 출력했을 때 차이를 관찰한다. “위험 출력”은 보안 교육을 위한 로컬 예제이며 실제 프로젝트에 복사하지 않는다.

## release-check.mjs

지정 폴더에서 다음을 확인하는 작은 읽기 전용 도구다.

- 필수 README와 index.html
- secret key로 의심되는 문자열
- config·environment 비밀 파일명
- innerHTML 사용 위치

실행:

~~~text
node release-check.mjs ../../my-project
~~~

결과는 보안 보증이 아니라 수동 검사를 시작하기 위한 힌트다.

## test_matrix.md

프로젝트 폴더로 복사해 예상 결과, 실제 결과, 증거와 수정 commit을 기록한다.
