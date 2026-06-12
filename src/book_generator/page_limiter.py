import subprocess
import sys


def split_sections(article: str) -> list[str]:
    parts = []
    current = []
    for line in article.splitlines():
        if line.startswith("\\section{") and current:
            parts.append("\n".join(current).strip())
            current = []
        current.append(line)
    if current:
        parts.append("\n".join(current).strip())
    return [part for part in parts if part]


def trim_to_page_limit(options, article, paths, writer, page_reader) -> tuple[str, int, int]:
    chapter, main, template, root = paths
    sections = split_sections(article)
    for keep in range(len(sections) - 1, 2, -1):
        candidate = "\n\n".join(sections[:keep])
        writer(chapter, main, template, options, candidate)
        code = subprocess.call([sys.executable, str(root / "scripts" / "build.py")], cwd=root)
        pages = page_reader(root / "latex" / "main.log")
        if code == 0 and pages <= 15:
            return candidate, pages, 0
    return article, page_reader(root / "latex" / "main.log"), 7
