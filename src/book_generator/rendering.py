from pathlib import Path

from .models import Manuscript


def render_markdown(manuscript: Manuscript, output_path: Path) -> None:
    lines = [f"# {manuscript.title}", "", f"_{manuscript.subtitle}_", ""]
    for chapter in manuscript.chapters:
        lines.extend([f"## {chapter.title}", "", chapter.body, ""])
    lines.extend(["## QA Notes", ""])
    lines.extend(f"- {note}" for note in manuscript.qa_notes)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines), encoding="utf-8")
