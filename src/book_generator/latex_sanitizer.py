import re

from book_generator.latex_table_sanitizer import shrink_wide_table_columns, wrap_hebrew_table_cells


PREAMBLE_COMMANDS = (
    "documentclass",
    "usepackage",
    "setmainlanguage",
    "setotherlanguage",
    "setmainfont",
    "settextfont",
    "newfontfamily",
    "geometry",
)

LAYOUT_COMMANDS = ("header", "footer", "pagestyle", "thispagestyle")


def sanitize_latex_body(text: str) -> str:
    text = text.replace("```latex", "").replace("```", "").strip()
    text = _strip_document_commands(text)
    text = _drop_generated_layout_commands(text)
    text = text.replace("\\chapter", "\\section")
    text = _drop_generated_references(text)
    text = _drop_listing_blocks(text)
    text = _drop_mojibake_lines(text)
    text = _drop_control_characters(text)
    text = _markdown_links_to_text(text)
    text = _inline_code_to_latex(text)
    text = _markdown_bold_to_latex(text)
    text = text.replace("\\textit or \\textit{other agents}", "agents or other agents")
    text = text.replace("Human-in-the-Loop (HITL)", "Human-in-the-Loop")
    text = text.replace("language=LaTeX", "language=TeX")
    text = wrap_hebrew_table_cells(text)
    text = shrink_wide_table_columns(text)
    text = _escape_ampersands_outside_tables(text)
    text = _escape_specials_outside_commands(text)
    return _balance_lists(text).strip()


def _strip_document_commands(text: str) -> str:
    text = re.sub(r"(?im)^\s*\\documentclass(?:\[[^\]]*\])?\{[^}]+\}\s*", "", text)
    text = re.sub(r"(?is)^.*?\\begin\{document\}", "", text)
    text = re.sub(r"(?is)\\end\{document\}.*$", "", text)
    lines = []
    for line in text.splitlines():
        stripped = line.strip()
        command_match = re.match(r"^\\([A-Za-z]+)", stripped)
        if command_match and command_match.group(1) in PREAMBLE_COMMANDS:
            continue
        lines.append(line)
    return "\n".join(lines).strip()


def _drop_generated_layout_commands(text: str) -> str:
    pattern = r"(?im)^\s*\\(" + "|".join(LAYOUT_COMMANDS) + r")(?:\{[^}]*\})?\s*$"
    return re.sub(pattern, "", text)


def _drop_listing_blocks(text: str) -> str:
    lines = []
    in_listing = False
    for line in text.splitlines():
        if "\\begin{lstlisting}" in line:
            in_listing = True
            continue
        if "\\end{lstlisting}" in line:
            in_listing = False
            continue
        if not in_listing:
            lines.append(line)
    return "\n".join(lines)


def _drop_mojibake_lines(text: str) -> str:
    return "\n".join(line for line in text.splitlines() if "Ãƒâ€”" not in line and "ÃƒÆ’" not in line)


def _drop_control_characters(text: str) -> str:
    return re.sub(r"[\x00-\x08\x0B\x0C\x0E-\x1F\x7F-\x9F]", "", text)


def _drop_generated_references(text: str) -> str:
    patterns = (
        r"(?im)^\s*\\section\*?\{references\}\s*$",
        r"(?im)^\s*\\bibliography\{[^}]+\}\s*$",
        r"(?im)^\s*\\bibliographystyle\{[^}]+\}\s*$",
        r"(?im)^\s*\\begin\{thebibliography\}\{[^}]+\}\s*$",
    )
    starts = []
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            starts.append(match.start())
    return text[: min(starts)].rstrip() if starts else text


def _markdown_links_to_text(text: str) -> str:
    return re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", text)


def _inline_code_to_latex(text: str) -> str:
    def repl(match):
        code = match.group(1).replace("\\", "\\textbackslash{}")
        for old, new in (("_", "\\_"), ("#", "\\#"), ("%", "\\%"), ("{", "\\{"), ("}", "\\}")):
            code = code.replace(old, new)
        return "\\texttt{" + code + "}"
    return re.sub(r"`([^`]+)`", repl, text)


def _markdown_bold_to_latex(text: str) -> str:
    return re.sub(r"\*\*([^*]+)\*\*", r"\\textbf{\1}", text)


def _escape_ampersands_outside_tables(text: str) -> str:
    lines = []
    in_table = False
    for line in text.splitlines():
        if "\\begin{tabular}" in line or "\\begin{align" in line:
            in_table = True
        if not in_table:
            line = re.sub(r"(?<!\\)&", r"\\&", line)
        lines.append(line)
        if "\\end{tabular}" in line or "\\end{align" in line:
            in_table = False
    return "\n".join(lines)


def _escape_specials_outside_commands(text: str) -> str:
    fixed = []
    for line in text.splitlines():
        if line.lstrip().startswith("\\"):
            fixed.append(line)
            continue
        line = re.sub(r"(?<!\\)%", r"\\%", line)
        line = re.sub(r"(?<!\\)#", r"\\#", line)
        fixed.append(line)
    return "\n".join(fixed)


def _balance_lists(text: str) -> str:
    for env in ("itemize", "enumerate"):
        opens = len(re.findall(r"\\begin\{" + env + r"\}", text))
        closes = len(re.findall(r"\\end\{" + env + r"\}", text))
        if opens > closes:
            text += "\n" + "\n".join(f"\\end{{{env}}}" for _ in range(opens - closes))
    return text
