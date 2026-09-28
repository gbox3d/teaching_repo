// val은 값을 한 번만 담는다. var는 나중에 다른 값을 담을 수 있다.
fun main() {
    val name = "홍길동"
    var greeting = "안녕하세요"

    println("$greeting, $name 님")

    greeting = "반갑습니다"
    println("$greeting, $name 님")
}
