# 앱 서버(FastAPI)만 담는다. 모델 서버(Ollama)는 컨테이너 밖(호스트)에서 돌고,
# 컨테이너는 OLLAMA_HOST=http://host.docker.internal:11434 로 그것을 찾아간다.
# 베이스 이미지 태그(Python 버전·OS)는 학기별 환경 기준표에서 확정한다.
FROM ghcr.io/astral-sh/uv:python3.12-trixie-slim

WORKDIR /app
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

# 1) 의존성 레이어 — pyproject.toml(과 있으면 uv.lock)만 먼저 복사한다.
#    코드가 바뀌어도 이 레이어는 캐시에서 재사용된다. uv.lock 을 커밋한 뒤에는 --frozen 을 붙인다.
COPY pyproject.toml uv.lock* ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --no-dev --no-install-project

# 2) 코드 레이어 — 나머지를 복사한다(.dockerignore 가 .env·.venv·outputs 를 뺀다).
COPY . .

ENV PATH="/app/.venv/bin:$PATH" \
    APP_HOST=0.0.0.0 \
    APP_PORT=8000 \
    LOG_DIR=/app/outputs

EXPOSE 8000

# /health 가 200 이면 건강한 것으로 본다. `docker ps` 의 STATUS 열에 (healthy) 로 나타난다.
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s \
    CMD python -c "import httpx, sys; sys.exit(0 if httpx.get('http://127.0.0.1:8000/health', timeout=4).status_code == 200 else 1)"

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
