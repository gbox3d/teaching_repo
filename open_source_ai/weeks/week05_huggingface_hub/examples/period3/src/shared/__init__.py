"""3교시 예제들이 함께 쓰는 데이터 위치와 데이터셋 ID. ex06·ex07 이 `from shared import ...` 로 쓴다."""

from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"  # 코드와 함께 패키지 안에 둔 데이터
SAMPLE_QA = DATA_DIR / "sample_qa.jsonl"  # 수업용으로 직접 만든 Q&A 12건
SAMPLE_CARD = DATA_DIR / "README.md"  # 그 데이터의 Dataset Card

HUB_DATASET = "klue/klue"  # 강의자가 다른 공개 데이터셋을 지정하면 여기만 바꾼다
HUB_CONFIG = "ynat"  # 구성(config)이 여러 개인 데이터셋은 이름을 함께 준다
