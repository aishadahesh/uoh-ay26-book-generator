from pathlib import Path
import os
import subprocess
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

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
from book_generator.document_options import (
    DocumentOptions,
    adapt_body_for_style,
    bidi_section,
    normalize_choice,
)
from book_generator.latex_sanitizer import sanitize_latex_body
from book_generator.latex_project import write_latex_project
from book_generator.page_count import read_pdf_pages
from book_generator.page_expander import expansion_count, expansion_pages
from book_generator.page_limiter import trim_to_page_limit
from book_generator.pdf_outputs import copy_named_outputs

CHAPTER = ROOT / "latex" / "chapters" / "online_article.tex"
MAIN = ROOT / "latex" / "main.tex"
TEMPLATE = ROOT / "latex" / "main_template.tex"
CANONICAL_PDF = ROOT / "output" / "agentic_ai_production_2026.pdf"


def ask_choice(prompt: str, default: str, allowed: tuple[str, ...]) -> str:
    try:
        answer = input(f"{prompt} [{default}]: ").strip() if sys.stdin.isatty() else ""
    except EOFError:
        answer = ""
    return normalize_choice(answer or default, allowed, default)


def choose_options() -> DocumentOptions:
    default_topic = os.getenv("ARTICLE_TOPIC", "Production-Ready AI Agent Architecture in 2026")
    topic = " ".join(sys.argv[1:]).strip() if len(sys.argv) > 1 else ""
    style = normalize_choice(os.getenv("DOCUMENT_STYLE", "article"), ("article", "book"), "article")
    language = normalize_choice(os.getenv("OUTPUT_LANGUAGE", "english"), ("english", "hebrew"), "english")
    if sys.stdin.isatty():
        print("\nCrewAI LaTeX generation")
        print(f"Default topic: {default_topic}")
        if not topic:
            try:
                topic = input("Enter topic, or press Enter to use the default: ").strip()
            except EOFError:
                topic = ""
        style = ask_choice("Choose document style: article or book", style, ("article", "book"))
        language = ask_choice("Choose output language: english or hebrew", language, ("english", "hebrew"))
    return DocumentOptions(topic or default_topic, style, language)


def clean_article(article: str, options: DocumentOptions) -> str:
    article = article.replace("```latex", "").replace("```", "").strip()
    article = sanitize_latex_body(article)
    if "Bilingual BiDi Demonstration" not in article:
        article += "\n\n" + bidi_section(options.output_language)
    return adapt_body_for_style(article, options.document_style)


def copy_topic_pdf(options: DocumentOptions) -> None:
    targets = copy_named_outputs(
        CANONICAL_PDF,
        options.topic,
        options.document_style,
        options.output_language,
    )
    for target in targets:
        print(f"Wrote named output: {target}")


def build_pdf(options: DocumentOptions, article: str) -> int:
    added = 0
    for _ in range(4):
        write_latex_project(CHAPTER, MAIN, TEMPLATE, options, article)
        code = subprocess.call([sys.executable, str(ROOT / "scripts" / "build.py")], cwd=ROOT)
        pages = read_pdf_pages(ROOT / "latex" / "main.log")
        if code != 0:
            return code
        if pages > 15:
            paths = (CHAPTER, MAIN, TEMPLATE, ROOT)
            article, pages, code = trim_to_page_limit(
                options, article, paths, write_latex_project, read_pdf_pages
            )
            if code != 0:
                return code
        if pages == 15:
            return 0
        missing = 15 - pages
        article += expansion_pages(options, missing, added)
        added += expansion_count(missing)
    return 5


def main() -> int:
    if load_dotenv:
        load_dotenv(ROOT / ".env")
    options = choose_options()
    print(f"Generating {options.output_language} {options.document_style}: {options.topic}")
    try:
        article = clean_article(run_article_crew(options).strip(), options)
    except Exception as exc:
        print(f"CrewAI online generation failed: {exc}", file=sys.stderr)
        return 2
    if "\\section" not in article and "\\chapter" not in article:
        print("CrewAI did not return LaTeX section/chapter content.", file=sys.stderr)
        return 3
    code = build_pdf(options, article)
    if code == 0:
        copy_topic_pdf(options)
    return code


if __name__ == "__main__":
    raise SystemExit(main())
