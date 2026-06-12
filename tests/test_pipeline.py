from book_generator import BookConfig, BookPipeline
from book_generator.latex_sanitizer import sanitize_latex_body
from book_generator.pdf_outputs import copy_named_outputs, topic_slug


def test_pipeline_generates_required_chapters():
    manuscript = BookPipeline(BookConfig()).run()
    assert manuscript.title
    assert len(manuscript.chapters) >= 3
    assert any("CrewAI" in chapter.body for chapter in manuscript.chapters)
    assert manuscript.qa_notes


def test_named_pdf_outputs_keep_stable_and_timestamped_copies(tmp_path):
    canonical = tmp_path / "agentic_ai_production_2026.pdf"
    canonical.write_bytes(b"%PDF")

    assert topic_slug("AI Agents in Healthcare!") == "AI_Agents_in_Healthcare"
    targets = copy_named_outputs(canonical, "AI Agents in Healthcare!", "book", "english")

    assert len(targets) == 2
    assert targets[0].name == "AI_Agents_in_Healthcare_book_english.pdf"
    assert targets[1].name.startswith("AI_Agents_in_Healthcare_book_english_")
    assert all(target.exists() for target in targets)


def test_sanitizer_removes_generated_layout_commands():
    raw = "\\chapter{Intro}\n\\header{Algorithmic Hair | Page 1}\n\\footer{Confidential}\nBody"
    cleaned = sanitize_latex_body(raw)

    assert "\\header" not in cleaned
    assert "\\footer" not in cleaned
    assert "\\chapter" not in cleaned
    assert "\\section{Intro}" in cleaned
