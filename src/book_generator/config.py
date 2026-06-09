from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class BookConfig:
    topic: str = "Production-Ready AI Agent Architecture in 2026"
    author: str = "Aisha Abu Dahesh and Yousef Asadi"
    course: str = "Orchestration of AI Agents"
    lecturer: str = "Dr. Yoram Segal"
    language_note: str = "English with a Hebrew/English BiDi demonstration"
    root: Path = Path.cwd()

    @property
    def latex_dir(self) -> Path:
        return self.root / "latex"

    @property
    def output_dir(self) -> Path:
        return self.root / "output"
