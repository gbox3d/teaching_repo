// 이름을 받아 한 줄을 출력하는 함수. main 바깥에 정의한다.
fun intro(name: String) {
    println("이름: $name")
}

fun main() {
    // if/else: 점수가 60 이상이면 "합격", 아니면 "불합격"
    val score = 85
    val result = if (score >= 60) "합격" else "불합격"
    println("결과: $result")

    // 함수 호출: 괄호 안의 값이 name으로 들어간다
    intro("홍길동")
    intro("김철수")
}
