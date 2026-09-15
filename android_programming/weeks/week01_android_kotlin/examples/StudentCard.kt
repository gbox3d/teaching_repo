// 이름을 받아 "이름: ..." 한 줄을 출력하는 함수
fun intro(name: String) {
    println("이름: $name")
}

fun main() {
    val studentId = "20260001"
    val name = "홍길동"
    val score = 85

    println("학번: $studentId")
    intro(name)

    val result = if (score >= 60) "합격" else "불합격"
    println("결과: $result")
}
