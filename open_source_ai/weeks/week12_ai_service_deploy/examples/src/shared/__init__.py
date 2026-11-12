from pathlib import Path
from bleuno_control import Board, chat, load_cases
from bleuno_control.models import needle_predictor
from bleuno_control.evaluation import evaluate
from bleuno_control.training import read_training, train, trained_path

DATA_FILE = Path(__file__).parent / "data" / "train_examples.jsonl"
MODELS_DIR = Path(__file__).resolve().parents[2] / "models"
