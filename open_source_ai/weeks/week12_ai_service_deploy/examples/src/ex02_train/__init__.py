import time
from shared import DATA_FILE, MODELS_DIR, train

EPOCHS = 4
BATCH_SIZE = 4
MAX_LEN = 1024
LEARNING_RATE = 1e-4


def main():
    started = time.perf_counter()
    train(DATA_FILE, MODELS_DIR, epochs=EPOCHS, batch_size=BATCH_SIZE,
          max_len=MAX_LEN, learning_rate=LEARNING_RATE)
    print(f"준비·학습·저장 소요: {time.perf_counter() - started:.1f}초")
