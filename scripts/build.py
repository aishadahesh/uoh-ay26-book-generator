from pathlib import Path
import os
import shutil
import subprocess
import sys
from typing import Optional

ROOT = Path(__file__).resolve().parents[1]
LATEX = ROOT / "latex" / "main.tex"
OUTPUT = ROOT / "output"


def run(command: list[str], timeout: int = 240) -> int:
    print("+", " ".join(command))
    try:
        return subprocess.run(command, cwd=LATEX.parent, timeout=timeout).returncode
    except subprocess.TimeoutExpired:
        print(f"Timed out after {timeout}s: {' '.join(command)}", file=sys.stderr)
        return 124


def find_engine() -> Optional[str]:
    direct = shutil.which("lualatex") or shutil.which("xelatex")
    if direct:
        return direct
    roots = [
        os.environ.get("LOCALAPPDATA"),
        os.environ.get("PROGRAMFILES"),
        os.environ.get("PROGRAMFILES(X86)"),
    ]
    suffixes = [
        r"Programs\MiKTeX\miktex\bin\x64",
        r"MiKTeX\miktex\bin\x64",
        r"MiKTeX 2.9\miktex\bin\x64",
    ]
    for root in filter(None, roots):
        for suffix in suffixes:
            folder = Path(root) / suffix
            for name in ("lualatex.exe", "xelatex.exe"):
                candidate = folder / name
                if candidate.exists():
                    return str(candidate)
    return None


def compile_with_engine(engine: str) -> int:
    command = [engine, "-interaction=nonstopmode", "-halt-on-error", "-file-line-error", "main.tex"]
    for _ in range(2):
        code = run(command)
        if code != 0:
            return code
    if shutil.which("biber"):
        run(["biber", "main"])
        code = run(command)
        if code != 0:
            return code
    code = run(command)
    if code != 0:
        return code
    pdf = LATEX.parent / "main.pdf"
    if pdf.exists():
        target = OUTPUT / "agentic_ai_production_2026.pdf"
        target.write_bytes(pdf.read_bytes())
        print(f"Wrote {target}")
    return 0


def main() -> int:
    OUTPUT.mkdir(exist_ok=True)
    engine = find_engine()
    if engine:
        return compile_with_engine(engine)
    if shutil.which("latexmk") and shutil.which("perl"):
        return run(["latexmk", "-lualatex", "-interaction=nonstopmode", "main.tex"])
    print("No usable LaTeX compiler found. Install MiKTeX/TeX Live with lualatex.", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
