from pathlib import Path
from bleuno_control import Board, chat, load_cases
from bleuno_control.models import needle_predictor
from bleuno_control.evaluation import evaluate
from bleuno_control.training import trained_path

# 12주차에 저장한 결과를 이어 쓴다. 모델 파일을 교시마다 복사하지 않는다.
MODELS_DIR = Path(__file__).resolve().parents[4] / "week12_control_lora" / "examples" / "models"
