from pathlib import Path
import subprocess
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from book_generator.document_options import DocumentOptions
from book_generator.localized_titles import localized_title
from book_generator.page_count import read_pdf_pages
from book_generator.page_expander import expansion_count, expansion_pages_for_count
from book_generator.pdf_outputs import copy_named_outputs, topic_slug
from book_generator.portfolio_bodies import TOPICS, base_body

CHAPTER = ROOT / "latex" / "chapters" / "online_article.tex"
MAIN = ROOT / "latex" / "main.tex"
TEMPLATE = ROOT / "latex" / "main_template.tex"
CANONICAL = ROOT / "output" / "agentic_ai_production_2026.pdf"
MANIFEST = ROOT / "output" / "portfolio_page_counts.md"


def duplicate_paragraphs(body):
    seen = set()
    duplicates = []
    for paragraph in body.split("\n\n"):
        text = " ".join(paragraph.split())
        if len(text) < 120 or text.startswith("\\begin") or text.startswith("\\["):
            continue
        if text in seen:
            duplicates.append(text[:100])
        seen.add(text)
    return duplicates


def template_values(options):
    title = localized_title(options.topic, options.output_language)
    return {
        "<<DOCUMENT_CLASS_LINE>>": options.class_line,
        "<<ARTICLE_TITLE>>": title,
        "<<ARTICLE_SUBTITLE>>": options.subtitle,
        "<<COVER_AUTHORS>>": options.cover_authors,
        "<<COVER_COURSE>>": options.cover_course,
        "<<COVER_ASSIGNMENT>>": options.cover_assignment,
        "<<COVER_LECTURER>>": options.cover_lecturer,
        "<<COVER_UNIVERSITY>>": options.cover_university,
        "<<COVER_DATE>>": options.cover_date,
        "<<MAIN_LANGUAGE>>": options.main_language,
        "<<OTHER_LANGUAGE>>": options.other_language,
        "<<CONTENTS_NAME>>": options.contents_name,
        "<<ABSTRACT_TITLE>>": options.abstract_title,
        "<<ABSTRACT_TEXT>>": options.abstract_text,
        "<<KEYWORDS_LABEL>>": options.keywords_label,
        "<<KEYWORDS>>": options.keywords,
        "<<TOC_LEVEL>>": options.toc_level,
        "<<HEADER_LEFT>>": title[:46],
        "<<HEADER_RIGHT>>": options.header_right,
        "<<TOC_BLOCK>>": options.toc_block,
    }


def write_project(options, body):
    duplicates = duplicate_paragraphs(body)
    if duplicates:
        raise ValueError(f"Repeated paragraph detected: {duplicates[0]}")
    CHAPTER.write_text(body + "\n", encoding="utf-8")
    text = TEMPLATE.read_text(encoding="utf-8")
    for key, value in template_values(options).items():
        text = text.replace(key, value)
    MAIN.write_text(text, encoding="utf-8")


def build_once():
    return subprocess.call([sys.executable, str(ROOT / "scripts" / "build.py")], cwd=ROOT)


def build_to_15(options, domain):
    base = base_body(options, domain)
    write_project(options, base)
    code = build_once()
    pages = read_pdf_pages(ROOT / "latex" / "main.log")
    if code != 0 or pages > 15:
        return code or 4, pages
    if pages == 15:
        copy_named_outputs(CANONICAL, options.topic, options.document_style, options.output_language)
        return 0, pages
    estimate = expansion_count(15 - pages)
    for count in range(max(1, estimate - 8), estimate + 41):
        body = base + "\n\n" + expansion_pages_for_count(domain, count)
        write_project(options, body)
        code = build_once()
        pages = read_pdf_pages(ROOT / "latex" / "main.log")
        print(f"  candidate sections={count}: {pages} pages")
        if code != 0:
            return code, pages
        if pages == 15:
            copy_named_outputs(CANONICAL, options.topic, options.document_style, options.output_language)
            return 0, pages
        if pages > 15:
            return 4, pages
    return 5, read_pdf_pages(ROOT / "latex" / "main.log")


def write_manifest(rows):
    lines = [
        "# Portfolio PDF Page Counts",
        "",
        "Generated on June 12, 2026.",
        "",
        "| Output | Style | Language | Pages |",
        "|---|---|---|---:|",
    ]
    for filename, style, language, pages in rows:
        lines.append(f"| `{filename}` | {style.title()} | {language.title()} | {pages} |")
    lines.extend([
        "",
        "The page count is enforced by the LaTeX build workflow. If a generated body is too short, the project appends dense, non-repeated, topic-specific research sections for the selected domain and rebuilds before saving the named PDF output.",
    ])
    MANIFEST.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    rows = []
    for topic, style, language, domain in TOPICS:
        options = DocumentOptions(topic, style, language)
        code, pages = build_to_15(options, domain)
        print(f"{topic} -> {pages} pages")
        if code != 0:
            return code
        rows.append((f"{topic_slug(topic)}_{style}_{language}.pdf", style, language, pages))
    write_manifest(rows)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
