from dataclasses import dataclass, field


@dataclass(frozen=True)
class AgentSpec:
    role: str
    goal: str
    backstory: str


@dataclass
class Chapter:
    title: str
    body: str
    citations: list[str] = field(default_factory=list)


@dataclass
class Manuscript:
    title: str
    subtitle: str
    chapters: list[Chapter]
    qa_notes: list[str]
