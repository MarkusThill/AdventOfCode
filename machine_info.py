#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import platform
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone
from hashlib import sha256
from typing import Any


# ----------------------------
# helpers
# ----------------------------

def run(cmd: list[str], timeout: float = 2.0) -> str | None:
    try:
        p = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            timeout=timeout,
        )
        return p.stdout.strip() or None
    except Exception:
        return None


def human_bytes(n: int) -> str:
    for unit in ["B", "KiB", "MiB", "GiB", "TiB"]:
        if n < 1024:
            return f"{n:.0f} {unit}"
        n /= 1024
    return f"{n:.2f} PiB"


def ascii_table(rows: list[tuple[str, str]]) -> str:
    w1 = max(len(k) for k, _ in rows)
    w2 = max(len(v) for _, v in rows)

    sep = f"+{'-'*(w1+2)}+{'-'*(w2+2)}+"
    out = [sep]
    for k, v in rows:
        out.append(f"| {k.ljust(w1)} | {v.ljust(w2)} |")
    out.append(sep)
    return "\n".join(out)


def fingerprint(obj: Any) -> str:
    blob = json.dumps(obj, sort_keys=True).encode()
    return sha256(blob).hexdigest()[:16]


# ----------------------------
# collectors
# ----------------------------

def core_info() -> dict[str, str]:
    info: dict[str, str] = {}

    # OS
    info["OS"] = f"{platform.system()} {platform.release()}"

    # Distro (Linux)
    if sys.platform.startswith("linux"):
        osr = run(["bash", "-lc", "source /etc/os-release 2>/dev/null && echo $PRETTY_NAME"])
        if osr:
            info["Distribution"] = osr

    info["Architecture"] = platform.machine()

    # CPU
    cpu = platform.processor() or "Unknown CPU"
    info["CPU"] = cpu

    phys = log = None
    try:
        import psutil  # type: ignore
        phys = psutil.cpu_count(logical=False)
        log = psutil.cpu_count(logical=True)
    except Exception:
        log = os.cpu_count()

    if phys and log:
        info["Cores (phys/log)"] = f"{phys} / {log}"
    elif log:
        info["Cores"] = str(log)

    # RAM
    try:
        import psutil  # type: ignore
        info["RAM"] = human_bytes(psutil.virtual_memory().total)
    except Exception:
        pass

    # GPU
    gpu = "None / Unknown"
    if shutil.which("nvidia-smi"):
        q = run([
            "nvidia-smi",
            "--query-gpu=name,memory.total",
            "--format=csv,noheader,nounits",
        ])
        if q:
            name, mem = [x.strip() for x in q.split(",")]
            gpu = f"NVIDIA {name} ({mem} MiB)"
    info["GPU"] = gpu

    # Python
    info["Python"] = f"{platform.python_implementation()} {platform.python_version()}"

    # Compiler
    for cc in ("gcc", "clang"):
        if shutil.which(cc):
            v = run([cc, "--version"])
            if v:
                info["Compiler"] = v.splitlines()[0]
                break

    return info


def full_info() -> dict[str, Any]:
    return {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "platform": {
            "system": platform.system(),
            "release": platform.release(),
            "version": platform.version(),
            "machine": platform.machine(),
            "processor": platform.processor(),
        },
        "python": {
            "version": platform.python_version(),
            "implementation": platform.python_implementation(),
            "executable": sys.executable,
        },
        "env": {k: os.environ[k] for k in [
            "OMP_NUM_THREADS",
            "MKL_NUM_THREADS",
            "CUDA_VISIBLE_DEVICES",
        ] if k in os.environ},
    }


# ----------------------------
# main
# ----------------------------

def main() -> None:
    p = argparse.ArgumentParser(description="Machine info for benchmarking")
    g = p.add_mutually_exclusive_group()
    g.add_argument("--core", action="store_true", help="Show only core benchmarking info")
    g.add_argument("--full", action="store_true", help="Show full info")

    f = p.add_mutually_exclusive_group()
    f.add_argument("--table", action="store_true", help="Human-readable ASCII table")
    f.add_argument("--json", action="store_true", help="JSON output")

    args = p.parse_args()

    if args.full:
        data = full_info()
    else:
        data = core_info()

    fp = fingerprint(data)

    if args.table or not args.json:
        rows = list(data.items())
        rows.append(("Fingerprint", fp))
        print(ascii_table(rows))
    else:
        data["fingerprint"] = fp
        print(json.dumps(data, indent=2))


if __name__ == "__main__":
    main()
