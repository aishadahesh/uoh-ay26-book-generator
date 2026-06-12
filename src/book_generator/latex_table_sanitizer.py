import re


def wrap_hebrew_table_cells(text: str) -> str:
    text = _expand_compact_tables(text)
    lines = []
    in_table = False
    for line in text.splitlines():
        if "\\begin{tabular}" in line:
            in_table = True
        if in_table and "&" in line and "\\hline" not in line:
            line = _wrap_cells(line)
        lines.append(line)
        if "\\end{tabular}" in line:
            in_table = False
    return "\n".join(lines)


def _expand_compact_tables(text: str) -> str:
    text = re.sub(r"(\\hline)\s+", r"\1\n", text)
    text = re.sub(r"\s+(\\\\)\s*(\\hline)", r" \1\n\2", text)
    return text.replace("\\end{tabular}", "\n\\end{tabular}")


def shrink_wide_table_columns(text: str) -> str:
    return re.sub(r"p\{0\.[7-9]\\textwidth\}", r"p{0.42\\textwidth}", text)


def _wrap_cells(line: str) -> str:
    end = "\\\\" if line.rstrip().endswith("\\\\") else ""
    body = line.rstrip()[:-2] if end else line
    cells = body.split("&")
    if _is_hebrew_row(cells):
        cells = list(reversed(cells))
    cells = [_wrap_hebrew_cell(cell) for cell in cells]
    return " & ".join(cells) + (" " + end if end else "")


def _is_hebrew_row(cells: list[str]) -> bool:
    meaningful = [cell for cell in cells if cell.strip()]
    return len(meaningful) > 1 and all(re.search(r"[\u0590-\u05FF]", cell) for cell in meaningful)


def _wrap_hebrew_cell(cell: str) -> str:
    stripped = cell.strip()
    if re.search(r"[\u0590-\u05FF]", stripped) and "\\begin{hebrew}" not in stripped:
        wrapped = "\\begin{hebrew}\\raggedleft " + stripped + "\\end{hebrew}"
        return cell.replace(stripped, wrapped)
    return cell
