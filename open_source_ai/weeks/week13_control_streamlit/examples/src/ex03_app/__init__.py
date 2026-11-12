import subprocess
import sys
from pathlib import Path

PORT = 8501


def main():
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run",
                        str(Path(__file__).with_name("app.py")),
                        "--server.address=127.0.0.1", f"--server.port={PORT}",
                        "--server.headless=true"], check=True)
    except KeyboardInterrupt:
        print("\n제어 앱을 종료합니다.")
