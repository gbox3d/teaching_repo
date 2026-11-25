"""Build the editable week 10 lab ZIP and its wleno release artifacts.

Run with Python 3.12 and uv on PATH. The student project is prepared in a
temporary directory; the teaching project's pyproject.toml and uv.lock stay unchanged.
"""

import argparse
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import tomllib
import zipfile


WEEK = Path(__file__).resolve().parents[1]
REPOSITORY = WEEK.parents[2]
BUNDLE_NAME = "week10-simulator-lab"


def student_manifest(source, wheel, version):
    """Keep the original project and entry points, replacing its local source."""
    manifest = tomllib.loads(source)
    if manifest["project"]["dependencies"] != [f"wleno=={version}"]:
        raise ValueError("The week 10 project must depend on the current wleno version.")
    if set(manifest["tool"]["uv"]["sources"]) != {"wleno"}:
        raise ValueError("Review the distribution sources: only wleno is expected.")
    result, count = re.subn(
        r"(?ms)^\[tool\.uv\.sources\]\s*\n.*?(?=^\[|\Z)",
        '[tool.uv.sources]\nwleno = { path = "wheels/' + wheel.name + '" }\n',
        source,
    )
    if count != 1:
        raise ValueError("The project must contain one [tool.uv.sources] table.")
    return result


def write_zip(project, destination):
    """Use stable member order, timestamps and permissions for repeat builds."""
    with zipfile.ZipFile(destination, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in sorted(project.rglob("*")):
            if not path.is_file():
                continue
            info = zipfile.ZipInfo(
                f"{BUNDLE_NAME}/{path.relative_to(project).as_posix()}",
                date_time=(1980, 1, 1, 0, 0, 0),
            )
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            archive.writestr(info, path.read_bytes())


def build(out_dir):
    uv = shutil.which("uv")
    if uv is None:
        raise RuntimeError("Install uv and make it available on PATH before building.")
    examples = WEEK / "examples"
    readme = WEEK / "distribution" / "README.md"
    if not readme.is_file():
        raise FileNotFoundError("The student distribution/README.md is required.")
    package = tomllib.loads((REPOSITORY / "tools" / "pyproject.toml").read_text(encoding="utf-8"))["project"]
    if package["name"] != "wleno":
        raise ValueError("tools/pyproject.toml must build the wleno distribution.")
    version = package["version"]
    env = os.environ.copy()
    env["SOURCE_DATE_EPOCH"] = "315532800"
    env["PYTHONDONTWRITEBYTECODE"] = "1"

    with tempfile.TemporaryDirectory(prefix="week10-distribution-") as temporary:
        staging = Path(temporary)
        artifacts = staging / "artifacts"
        # uv builds the wheel from the sdist, checking that the source release is complete.
        subprocess.run(
            [uv, "build", str(REPOSITORY / "tools"), "--out-dir", str(artifacts)],
            check=True, env=env,
        )
        wheel = artifacts / f"wleno-{version}-py3-none-any.whl"
        sdist = artifacts / f"wleno-{version}.tar.gz"
        if not wheel.is_file() or not sdist.is_file():
            raise RuntimeError("The build did not produce the expected universal wheel and sdist.")

        project = staging / BUNDLE_NAME
        shutil.copytree(
            examples / "src", project / "src",
            ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "*.pyo"),
        )
        shutil.copy2(examples / ".python-version", project / ".python-version")
        shutil.copy2(readme, project / "README.md")
        shutil.copy2(REPOSITORY / "LICENSE", project / "LICENSE")
        (project / "wheels").mkdir()
        shutil.copy2(wheel, project / "wheels" / wheel.name)
        manifest = student_manifest((examples / "pyproject.toml").read_text(encoding="utf-8"), wheel, version)
        (project / "pyproject.toml").write_text(manifest, encoding="utf-8", newline="\n")
        # Only the bundled wheel is resolved; no model or package registry is needed.
        subprocess.run([uv, "lock", "--offline"], cwd=project, check=True, env=env)
        subprocess.run([uv, "lock", "--check", "--offline"], cwd=project, check=True, env=env)
        archive = artifacts / f"{BUNDLE_NAME}-{version}.zip"
        write_zip(project, archive)

        out_dir.mkdir(parents=True, exist_ok=True)
        for artifact in (wheel, sdist, archive):
            target = out_dir / artifact.name
            shutil.copy2(artifact, target)
            print(f"{target} ({target.stat().st_size:,} bytes)")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-dir", required=True, type=Path, help="Directory for the ZIP, wheel and sdist")
    args = parser.parse_args()
    build(args.out_dir.expanduser().resolve())


if __name__ == "__main__":
    main()
