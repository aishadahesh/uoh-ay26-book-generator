from dataclasses import dataclass
import re
from book_generator.cover_metadata import cover_value


@dataclass(frozen=True)
class DocumentOptions:
    topic: str
    document_style: str
    output_language: str

    @property
    def class_line(self) -> str:
        opts = "12pt,a4paper,openany" if self.document_style == "book" else "12pt,a4paper"
        return f"\\documentclass[{opts}]{{{self.document_style}}}"

    @property
    def subtitle(self) -> str:
        kind = "Research Book" if self.document_style == "book" else "Research Article"
        if self.output_language == "hebrew":
            kind = "ספר מחקרי" if self.document_style == "book" else "מאמר מחקרי"
            return f"תוצר מקוון של CrewAI ו-LaTeX - {kind}"
        return f"Online CrewAI + LaTeX {kind}"

    @property
    def cover_authors(self) -> str:
        return cover_value(self.output_language, "authors")

    @property
    def cover_course(self) -> str:
        return cover_value(self.output_language, "course")

    @property
    def cover_assignment(self) -> str:
        return cover_value(self.output_language, "assignment")

    @property
    def cover_lecturer(self) -> str:
        return cover_value(self.output_language, "lecturer")

    @property
    def cover_university(self) -> str:
        return cover_value(self.output_language, "university")

    @property
    def cover_date(self) -> str:
        return cover_value(self.output_language, "date")

    @property
    def main_language(self) -> str:
        return "hebrew" if self.output_language == "hebrew" else "english"

    @property
    def other_language(self) -> str:
        return "english" if self.output_language == "hebrew" else "hebrew"

    @property
    def contents_name(self) -> str:
        return "תוכן עניינים" if self.output_language == "hebrew" else "Contents"

    @property
    def abstract_title(self) -> str:
        return "תקציר" if self.output_language == "hebrew" else "Abstract"

    @property
    def abstract_text(self) -> str:
        if self.document_style == "book":
            return self._book_abstract()
        return self._article_abstract()

    def _book_abstract(self) -> str:
        if self.output_language == "hebrew":
            return "ספרון מחקרי זה מציג מסגרת רחבה לדיון בנושא, בונה רקע מושגי, מציע מדדי הערכה, ומדגים כיצד CrewAI ו-LaTeX יכולים להפיק מסמך מקצועי, מבוקר ורב-לשוני."
        return "This research booklet gives a broad conceptual frame, evaluation model, and production workflow for the selected topic while demonstrating a controlled CrewAI and LaTeX publication pipeline."

    def _article_abstract(self) -> str:
        if self.output_language == "hebrew":
            return f"מאמר זה בוחן את הנושא {self.topic}, מציג טענה מחקרית ממוקדת, מסביר את ההקשר המקצועי, ומדגים כיצד סוכני CrewAI יכולים לייצר מסמך LaTeX בר-בדיקה."
        return f"This article examines {self.topic}, develops a focused research argument, and demonstrates how CrewAI agents can generate a verifiable LaTeX publication."

    @property
    def keywords_label(self) -> str:
        return "מילות מפתח" if self.output_language == "hebrew" else "Keywords"

    @property
    def keywords(self) -> str:
        if self.output_language == "hebrew":
            return "ספורט, גביע העולם 2026, סוכני AI, CrewAI, LaTeX, BiDi, הערכה"
        return "sport, World Cup 2026, AI agents, CrewAI, LaTeX, BiDi, evaluation"

    @property
    def toc_level(self) -> str:
        return "chapter" if self.document_style == "book" else "section"

    @property
    def toc_block(self) -> str:
        if self.document_style != "book":
            return ""
        return "\\tableofcontents\n\\clearpage"

    @property
    def header_left(self) -> str:
        return self.topic[:46]

    @property
    def header_right(self) -> str:
        return "CrewAI + LaTeX Book" if self.document_style == "book" else "CrewAI + LaTeX Article"


def normalize_choice(value: str, allowed: tuple[str, ...], default: str) -> str:
    candidate = value.strip().lower()
    return candidate if candidate in allowed else default


def bidi_section(language: str) -> str:
    return ENGLISH_BIDI_SECTION if language == "hebrew" else HEBREW_BIDI_SECTION


def adapt_body_for_style(article: str, style: str) -> str:
    article = strip_generated_front_matter(article)
    if style != "book":
        return re.sub(r"\\chapter\{", r"\\section{", article)
    article = re.sub(r"\\subsubsection\{", r"\\subsection{", article)
    article = re.sub(r"\\chapter\{", r"\\section{", article)
    return re.sub(r"\\section\{", r"\\chapter{", article, count=1)


def strip_generated_front_matter(article: str) -> str:
    article = re.sub(r"(?ms)^\s*\\title\{.*?\}\s*", "", article)
    article = re.sub(r"(?ms)^\s*\\author\{.*?\}\s*", "", article)
    article = re.sub(r"(?ms)^\s*\\date\{.*?\}\s*", "", article)
    article = re.sub(r"(?im)^\s*\\maketitle\s*", "", article)
    article = re.sub(r"(?is)\\begin\{abstract\}.*?\\end\{abstract\}\s*", "", article)
    return re.sub(r"(?im)^\s*\\tableofcontents\s*", "", article).strip()


HEBREW_BIDI_SECTION = r"""
\section{Bilingual BiDi Demonstration}
\begin{hebrew}\begin{flushright}
עמוד זה מדגים פסקה עברית חיה בתוך מסמך שמוגדר בעיקר באנגלית. הטקסט מיושר לימין, נשבר לשורות בצורה טבעית, ונשמר כטקסט אמיתי שאפשר לבחור, להעתיק ולבדוק. כדי למנוע ערבוב כיווניות, הפסקה משתמשת בעברית רציפה ואינה משלבת מונחים לועזיים באמצע המשפט.
\end{flushright}\end{hebrew}
"""


ENGLISH_BIDI_SECTION = r"""
\section{Bilingual BiDi Demonstration}
\begin{english}\begin{flushleft}
This section is real English text inside a Hebrew document. It proves that the publication can switch from right-to-left Hebrew discussion into left-to-right technical explanation without using an image.
\end{flushleft}\end{english}
"""
