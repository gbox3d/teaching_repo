"""첫 Python 호출: uv run python hello.py (먼저 Ollama와 모델을 준비한다)."""

from ollama import Client

from config import load_settings

settings = load_settings()
client = Client(host=settings.host, timeout=settings.timeout)

response = client.chat(
    model=settings.model,
    messages=[{"role": "user", "content": "안녕. 한국어로 한 문장만 인사해 줘."}],
    think=False,  # 실습용 Qwen3에서는 긴 생각 출력 없이 답만 받는다.
)
print(response.message.content)
