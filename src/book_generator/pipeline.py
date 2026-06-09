from .agents import AGENTS
from .config import BookConfig
from .models import Chapter, Manuscript


class BookPipeline:
    '''Deterministic CrewAI-style pipeline used when live CrewAI is unavailable.'''

    def __init__(self, config: BookConfig) -> None:
        self.config = config

    def run(self) -> Manuscript:
        chapters = [
            Chapter(
                "From Prompt Demo to Runtime",
                "A production agent is not a long prompt. It is a runtime with planning, memory, tools, verification, monitoring, and policy boundaries.",
                ["segal2026lecture"],
            ),
            Chapter(
                "The Crew as an Organization",
                "CrewAI encourages decomposition into roles: planner, researcher, writer, reviewer, and publication engineer. The context passed between tasks becomes the glue of the workflow.",
                ["crewai2026docs"],
            ),
            Chapter(
                "Control, Observability, and Risk",
                "As tool permissions grow, the control layer becomes more important than the model itself. Logs, evaluations, human gates, and sandboxing are core design material.",
                ["nist2024ai", "owasp2025agents"],
            ),
        ]
        return Manuscript(
            title=self.config.topic,
            subtitle="From prompt demos to governed agent runtime systems",
            chapters=chapters,
            qa_notes=[
                f"Agents modeled: {len(AGENTS)}",
                "Includes Markdown-first workflow and LaTeX output boundary.",
                "Assignment checklist is represented in docs and LaTeX source.",
            ],
        )
