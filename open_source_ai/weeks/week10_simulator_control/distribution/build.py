"""Package the week 10 student project. Its dependencies are installed from PyPI."""

import argparse
from pathlib import Path
import subprocess
from tempfile import TemporaryDirectory
import tomllib
import zipfile


WEEK = Path(__file__).resolve().parents[1]
BUNDLE_NAME = "week10-simulator-lab"


def build(out_dir):
    examples = WEEK / "examples"
    subprocess.run(["uv", "lock", "--check"], cwd=examples, check=True)
    manifest = tomllib.loads((examples / "pyproject.toml").read_text(encoding="utf-8"))
    version = manifest["project"]["version"]

    # Only student-editable code and its installation files belong in the archive.
    files = {name: examples / name for name in (".python-version", "pyproject.toml", "uv.lock")}
    files["README.md"] = WEEK / "distribution" / "README.md"
    files["LICENSE"] = WEEK.parents[2] / "LICENSE"
    for path in (examples / "src").rglob("*.py"):
        files[path.relative_to(examples).as_posix()] = path

    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / f"{BUNDLE_NAME}-{version}.zip"
    with TemporaryDirectory(dir=out_dir) as staging:
        temporary = Path(staging) / target.name
        with zipfile.ZipFile(temporary, "w") as archive:
            for name, path in sorted(files.items()):
                info = zipfile.ZipInfo(f"{BUNDLE_NAME}/{name}", date_time=(1980, 1, 1, 0, 0, 0))
                info.create_system = 3
                info.external_attr = 0o100644 << 16
                archive.writestr(info, path.read_bytes(), compress_type=zipfile.ZIP_DEFLATED)
        temporary.replace(target)
    print(target)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-dir", required=True, type=Path, help="Destination for the student ZIP")
    build(parser.parse_args().out_dir)
