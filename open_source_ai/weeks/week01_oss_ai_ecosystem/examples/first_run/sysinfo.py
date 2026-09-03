"""sysinfo.py — 1주차 첫 uv 실행 예제.

OS·CPU·RAM·디스크·GPU·Python·환경변수 값을 모아 outputs/sysinfo.json으로 남긴다.
GPU는 nvidia-smi를 호출해 읽고, 실패하면 "GPU 없음"과 사유를 기록한 뒤 계속 진행한다.
외부 패키지는 python-dotenv 하나이며, 없어도 동작한다(.env를 읽지 않을 뿐이다).
사용자 이름·홈 경로가 보고서에 들어가지 않도록 경로는 프로젝트 기준 상대 경로만 남긴다.
"""

from __future__ import annotations

import argparse
import json
import os
import platform
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    from dotenv import load_dotenv
except ImportError:  # uv run --no-project 처럼 의존성 없이 실행하면 dotenv가 없을 수 있다
    load_dotenv = None

# 수업 공통 환경변수와 기본값. 모델 ID·서버 주소는 코드에 박지 않고 여기서만 읽는다.
ENV_DEFAULTS: dict[str, str] = {"OLLAMA_HOST": "http://localhost:11434", "OLLAMA_MODEL": "qwen3:8b"}
GIB = 1024**3
OUTSIDE = "(프로젝트 폴더 밖)"
NVSMI_ARGS = ["--query-gpu=name,memory.total,driver_version", "--format=csv,noheader"]


def memory_total_gb() -> float | None:
    """총 물리 메모리(GiB). 표준 라이브러리만 쓰고, 읽지 못하면 None을 돌려준다."""
    try:
        if platform.system() == "Windows":
            import ctypes

            fields = [("dwLength", ctypes.c_ulong), ("dwMemoryLoad", ctypes.c_ulong)]
            fields += [(name, ctypes.c_ulonglong) for name in (
                "ullTotalPhys", "ullAvailPhys", "ullTotalPageFile", "ullAvailPageFile",
                "ullTotalVirtual", "ullAvailVirtual", "ullAvailExtendedVirtual")]

            class MemoryStatus(ctypes.Structure):
                _fields_ = fields

            status = MemoryStatus()
            status.dwLength = ctypes.sizeof(MemoryStatus)
            if ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(status)):
                return round(status.ullTotalPhys / GIB, 1)
        elif platform.system() == "Linux":
            for line in Path("/proc/meminfo").read_text(encoding="utf-8").splitlines():
                if line.startswith("MemTotal:"):
                    return round(int(line.split()[1]) * 1024 / GIB, 1)
    except (OSError, ValueError, AttributeError):
        pass
    return None


def disk_info(project_dir: Path) -> dict[str, Any]:
    """프로젝트가 있는 드라이브의 용량. 경로는 드라이브 루트만 남긴다."""
    usage = shutil.disk_usage(project_dir)
    path = project_dir.anchor or str(project_dir)
    return {"path": path, "total_gb": round(usage.total / GIB, 1), "free_gb": round(usage.free / GIB, 1)}


def gpu_info(skip: bool) -> dict[str, Any]:
    """nvidia-smi로 GPU 이름·VRAM·드라이버를 읽는다. 실패하면 사유를 남기고 계속 진행한다."""
    def missing(reason: str) -> dict[str, Any]:
        return {"available": False, "reason": f"GPU 없음: {reason}", "devices": []}

    if skip:
        return missing("--no-gpu 옵션으로 건너뜀")
    exe = shutil.which("nvidia-smi")
    if exe is None:
        return missing("nvidia-smi 명령을 찾을 수 없음(NVIDIA GPU 또는 드라이버 없음)")
    try:
        result = subprocess.run([exe, *NVSMI_ARGS], capture_output=True, text=True, timeout=20, check=True)
    except subprocess.CalledProcessError as exc:
        detail = (exc.stderr or exc.stdout or "").strip()[:200]
        return missing(f"nvidia-smi 종료 코드 {exc.returncode} — {detail}")
    except (subprocess.SubprocessError, OSError) as exc:
        return missing(f"nvidia-smi 실행 실패 — {exc}")
    devices: list[dict[str, str]] = []
    for line in result.stdout.strip().splitlines():
        parts = [part.strip() for part in line.split(",")]
        if len(parts) >= 3:
            devices.append({"name": parts[0], "memory_total": parts[1], "driver_version": parts[2]})
    if not devices:
        return missing("nvidia-smi 출력이 비어 있음")
    return {"available": True, "reason": "", "devices": devices}


def python_info(project_dir: Path) -> dict[str, Any]:
    """어느 Python이 실행 중인지. 경로는 프로젝트 기준 상대 경로만 남긴다."""
    try:
        location = Path(sys.prefix).resolve().relative_to(project_dir).as_posix()
    except ValueError:
        location = OUTSIDE
    in_venv = sys.prefix != sys.base_prefix and location != OUTSIDE
    return {"version": platform.python_version(), "implementation": platform.python_implementation(),
            "in_project_venv": in_venv, "venv_location": location}


def env_info() -> dict[str, dict[str, str]]:
    """수업 공통 환경변수. 값을 호출에 쓰지는 않고(4주차) 어디서 왔는지만 기록한다."""
    report: dict[str, dict[str, str]] = {}
    for key, default in ENV_DEFAULTS.items():
        if key in os.environ:
            report[key] = {"value": os.environ[key], "source": ".env 또는 환경변수"}
        else:
            report[key] = {"value": default, "source": "기본값"}
    return report


def build_report(project_dir: Path, skip_gpu: bool) -> dict[str, Any]:
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "os": {"system": platform.system(), "release": platform.release(),
               "version": platform.version(), "machine": platform.machine()},
        "cpu": {"name": platform.processor() or "(알 수 없음)", "logical_cores": os.cpu_count()},
        "memory": {"total_gb": memory_total_gb()},
        "disk": disk_info(project_dir),
        "gpu": gpu_info(skip_gpu),
        "python": python_info(project_dir),
        "env": env_info(),
    }


def summarize(report: dict[str, Any]) -> list[str]:
    gpu = report["gpu"]
    gpu_line = gpu["reason"]
    if gpu["available"]:
        gpu_line = ", ".join(f"{d['name']} ({d['memory_total']}, driver {d['driver_version']})" for d in gpu["devices"])
    model = report["env"]["OLLAMA_MODEL"]
    return [
        f"OS       : {report['os']['system']} {report['os']['release']} ({report['os']['machine']})",
        f"CPU      : {report['cpu']['name']} / 논리 코어 {report['cpu']['logical_cores']}",
        f"RAM      : {report['memory']['total_gb']} GiB",
        f"디스크   : {report['disk']['path']} 여유 {report['disk']['free_gb']} / {report['disk']['total_gb']} GiB",
        f"GPU      : {gpu_line}",
        f"Python   : {report['python']['version']} @ {report['python']['venv_location']}",
        f"모델 설정: OLLAMA_MODEL={model['value']} [{model['source']}]",
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description="PC 정보를 모아 JSON 보고서로 남긴다(1주차 첫 uv 실행).")
    parser.add_argument("--out", default="outputs/sysinfo.json", help="보고서 경로. 상대 경로는 이 스크립트 폴더 기준")
    parser.add_argument("--no-gpu", action="store_true", help="nvidia-smi를 호출하지 않고 GPU 없음 경로를 재현한다")
    parser.add_argument("--print", dest="print_json", action="store_true", help="보고서 JSON 전체를 화면에도 출력한다")
    args = parser.parse_args()

    project_dir = Path(__file__).resolve().parent
    if load_dotenv is not None:
        load_dotenv(project_dir / ".env")  # .env가 없으면 아무 일도 하지 않는다
    else:
        print("[안내] python-dotenv가 없어 .env를 읽지 않는다. 환경변수는 셸에서 직접 설정한다.")

    report = build_report(project_dir, args.no_gpu)
    out_path = Path(args.out) if Path(args.out).is_absolute() else project_dir / args.out
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    for line in summarize(report):
        print(line)
    if args.print_json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    try:
        shown = out_path.relative_to(project_dir).as_posix()
    except ValueError:
        shown = out_path.name
    print(f"저장: {shown}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
