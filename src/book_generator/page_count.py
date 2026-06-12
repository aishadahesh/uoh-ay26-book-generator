from pathlib import Path
import re


def read_pdf_pages(log_path: Path) -> int:
    if not log_path.exists():
        return 0
    text = log_path.read_text(encoding="utf-8", errors="ignore")
    matches = re.findall(r"Output written on .*?\((\d+) pages?,", text)
    return int(matches[-1]) if matches else 0
