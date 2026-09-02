"""OS·CPU·RAM·GPU 정보를 모아 dict 로 돌려준다.

1주차 `sysinfo.py` 와 같은 항목을 수집한다. 표준 라이브러리만 쓴다.
GPU 는 `nvidia-smi --query-gpu=name,memory.total --format=csv,noheader` 로 읽고,
실행 파일이 없거나 실패하면 "GPU 없음" 으로 기록한다(예외를 밖으로 던지지 않는다).
"""

from __future__ import annotations

import ctypes
import os
import platform
import shutil
import subprocess
from datetime import datetime, timezone

GPU_QUERY = ["--query-gpu=name,memory.total", "--format=csv,noheader"]


def ram_total_gb() -> float | None:
    """총 물리 메모리(GB). 알 수 없으면 None."""
    system = platform.system()
    try:
        if system == "Windows":

            class MemoryStatus(ctypes.Structure):
                _fields_ = [
                    ("dwLength", ctypes.c_ulong),
                    ("dwMemoryLoad", ctypes.c_ulong),
                    ("ullTotalPhys", ctypes.c_ulonglong),
                    ("ullAvailPhys", ctypes.c_ulonglong),
                    ("ullTotalPageFile", ctypes.c_ulonglong),
                    ("ullAvailPageFile", ctypes.c_ulonglong),
                    ("ullTotalVirtual", ctypes.c_ulonglong),
                    ("ullAvailVirtual", ctypes.c_ulonglong),
                    ("ullAvailExtendedVirtual", ctypes.c_ulonglong),
                ]

            status = MemoryStatus()
            status.dwLength = ctypes.sizeof(MemoryStatus)
            ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(status))  # type: ignore[attr-defined]
            return round(status.ullTotalPhys / 1024**3, 1)
        if hasattr(os, "sysconf"):
            pages = os.sysconf("SC_PHYS_PAGES")
            page_size = os.sysconf("SC_PAGE_SIZE")
            return round(pages * page_size / 1024**3, 1)
    except (OSError, ValueError, AttributeError):
        return None
    return None


def gpu_info() -> dict[str, object]:
    """nvidia-smi 결과. GPU 가 없어도 예외 대신 이유를 담아 돌려준다."""
    exe = shutil.which("nvidia-smi")
    if exe is None:
        return {"available": False, "reason": "nvidia-smi 를 찾지 못함 (GPU 없음 또는 드라이버 미설치)"}
    try:
        result = subprocess.run(
            [exe, *GPU_QUERY], capture_output=True, text=True, timeout=10, check=False
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {"available": False, "reason": f"nvidia-smi 실행 실패: {exc}"}
    if result.returncode != 0:
        return {
            "available": False,
            "reason": f"nvidia-smi 종료 코드 {result.returncode}: {result.stderr.strip()}",
        }
    devices: list[dict[str, str]] = []
    for line in result.stdout.strip().splitlines():
        parts = [part.strip() for part in line.split(",")]
        if len(parts) >= 2:
            devices.append({"name": parts[0], "memory_total": parts[1]})
    if not devices:
        return {"available": False, "reason": "nvidia-smi 출력을 해석하지 못함"}
    return {"available": True, "devices": devices}


def collect() -> dict[str, object]:
    """모든 항목을 한 번에 수집한다. 1주차 sysinfo.json 과 같은 키를 쓴다."""
    return {
        "collected_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "os": platform.system(),
        "os_release": platform.release(),
        "machine": platform.machine(),
        "cpu": platform.processor() or "unknown",
        "cpu_count": os.cpu_count(),
        "ram_total_gb": ram_total_gb(),
        "python": platform.python_version(),
        "gpu": gpu_info(),
    }


def format_text(info: dict[str, object]) -> str:
    """사람이 읽을 요약. JSON 이 필요하면 cli.py 가 json.dumps 로 처리한다."""
    gpu = info["gpu"]
    assert isinstance(gpu, dict)
    if gpu.get("available"):
        gpu_line = ", ".join(f"{d['name']} ({d['memory_total']})" for d in gpu["devices"])
    else:
        gpu_line = f"없음: {gpu.get('reason')}"
    lines = [
        f"OS      : {info['os']} {info['os_release']} ({info['machine']})",
        f"CPU     : {info['cpu']} x {info['cpu_count']}",
        f"RAM     : {info['ram_total_gb']} GB",
        f"Python  : {info['python']}",
        f"GPU     : {gpu_line}",
    ]
    return "\n".join(lines)
