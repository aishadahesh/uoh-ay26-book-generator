from pathlib import Path
import os
import re
import shutil
import subprocess
import sys

if sys.version_info < (3, 10):
    print(
        "CrewAI online generation requires Python 3.10-3.13. "
        "You are using Python " + sys.version.split()[0] + ".\n"
        "Deactivate the old .venv, then run:\n"
        "  .\\.venv-crewai\\Scripts\\Activate.ps1\n"
        "  python scripts/generate_online.py \"Your topic\"",
        file=sys.stderr,
    )
    raise SystemExit(1)

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from book_generator.crewai_pipeline import run_article_crew
from book_generator.latex_sanitizer import sanitize_latex_body

CHAPTER = ROOT / "latex" / "chapters" / "online_article.tex"
MAIN = ROOT / "latex" / "main.tex"
TEMPLATE = ROOT / "latex" / "main_template.tex"
CANONICAL_PDF = ROOT / "output" / "agentic_ai_production_2026.pdf"

HEBREW_SECTION = r"""\section{Bilingual BiDi Demonstration}
\begin{hebrew}
\begin{flushright}
עמוד זה מדגים שילוב אמיתי של עברית ואנגלית בתוך מסמך LaTeX. הטקסט מיושר לימין ונשמר כטקסט חי, לא כתמונה.
\end{flushright}
\end{hebrew}
"""


def choose_topic() -> str:
    default = os.getenv("ARTICLE_TOPIC", "Production-Ready AI Agent Architecture in 2026")
    if len(sys.argv) > 1:
        return " ".join(sys.argv[1:]).strip() or default
    if sys.stdin.isatty():
        print("\nCrewAI article generation")
        print(f"Default topic: {default}")
        answer = input("Enter article topic, or press Enter to use the default: ").strip()
        return answer or default
    return default


def clean_article(article: str) -> str:
    article = article.replace("```latex", "").replace("```", "").strip()
    article = sanitize_latex_body(article)
    if "\\begin{hebrew}" not in article:
        article += "\n\n" + HEBREW_SECTION
    return article


def write_latex_project(topic: str, article: str) -> None:
    CHAPTER.write_text(article + "\n", encoding="utf-8")
    template = TEMPLATE.read_text(encoding="utf-8")
    MAIN.write_text(template.replace("<<ARTICLE_TITLE>>", topic), encoding="utf-8")


def copy_topic_pdf(topic: str) -> None:
    if not CANONICAL_PDF.exists():
        return
    slug = re.sub(r"[^A-Za-z0-9]+", "_", topic).strip("_") or "article"
    target = CANONICAL_PDF.with_name(slug[:80] + ".pdf")
    if target != CANONICAL_PDF:
        shutil.copyfile(CANONICAL_PDF, target)
        print(f"Wrote topic copy: {target}")


def main() -> int:
    if load_dotenv:
        load_dotenv(ROOT / ".env")
    topic = choose_topic()
    print(f"Generating article topic: {topic}")
    try:
        article = clean_article(run_article_crew(topic).strip())
    except Exception as exc:
        print(f"CrewAI online generation failed: {exc}", file=sys.stderr)
        return 2
    if "\\section" not in article:
        print("CrewAI did not return LaTeX section content.", file=sys.stderr)
        return 3
    write_latex_project(topic, article)
    code = subprocess.call([sys.executable, str(ROOT / "scripts" / "build.py")], cwd=ROOT)
    if code == 0:
        copy_topic_pdf(topic)
    return code


if __name__ == "__main__":
    raise SystemExit(main())