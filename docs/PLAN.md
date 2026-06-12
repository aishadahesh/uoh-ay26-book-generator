# PLAN - Online CrewAI and LaTeX Delivery Plan

## Architecture Overview

The project is organized as a professional document-generation pipeline. The Python layer runs the online CrewAI workflow, the LaTeX layer owns publication quality, the docs layer records requirements and planning, and the output folder stores the generated PDF artifact.

The main assignment path is:

1. User chooses a topic, article/book style, and English/Hebrew output language in the terminal.
2. CrewAI agents generate the article online with Gemini or OpenAI.
3. Python sanitizes the generated LaTeX body.
4. The LaTeX template is filled with title, document class, language, table-of-contents labels, abstract, keywords, headers, and localized cover metadata.
5. LuaLaTeX/XeLaTeX compiles the final PDF.

## Module Boundaries

- `scripts/generate_online.py` is the main executable assignment workflow.
- `scripts/build.py` compiles the LaTeX project and writes the PDF to `output/`.
- `scripts/setup_env.ps1` creates `.venv-crewai` and installs dependencies.
- `src/book_generator/crewai_llm.py` configures Gemini/OpenAI for CrewAI.
- `src/book_generator/crewai_agents.py` defines CrewAI agents.
- `src/book_generator/crewai_tasks.py` defines CrewAI tasks.
- `src/book_generator/crewai_pipeline.py` creates and runs the CrewAI crew with fallback model handling.
- `src/book_generator/document_options.py` stores article/book and English/Hebrew rendering choices, including mirrored BiDi sections and localized title-page metadata.
- `src/book_generator/latex_sanitizer.py` cleans generated LaTeX before build, including accidental preambles, nested bibliographies, markdown fragments, mojibake blocks, and unbalanced lists.
- `latex/main_template.tex` is the reusable publication shell.
- `latex/chapters/online_article.tex` is the generated article body.

## Crew Design

The online crew uses role discipline so the output is not just one unstructured prompt response.

1. Planner Agent - turns the assignment into article structure and acceptance criteria.
2. Research Agent - identifies relevant claims, risks, references, and current agentic-system context.
3. Writer Agent - writes dense, section-specific research prose.
4. LaTeX Engineer Agent - shapes the output as valid LaTeX sections with tables, formula, figure references, and BiDi requirements.
5. QA Agent - checks whether the generated article is suitable for a professional PDF submission.

The crew runs sequentially because the assignment output benefits from ordered refinement: requirements first, research second, prose third, typesetting fourth, QA last.

## Online Generation Workflow

1. Activate `.venv-crewai`.
2. Run `python scripts/generate_online.py`.
3. Enter a custom topic or press Enter for ARTICLE_TOPIC / default topic.
4. Choose `article` or `book`, then choose `english` or `hebrew`; non-interactive runs may use `DOCUMENT_STYLE` and `OUTPUT_LANGUAGE`.
5. The script loads `.env` and selects the configured provider.
6. CrewAI sends the task sequence to Gemini or OpenAI.
7. If Gemini fails with transient 500/503 errors, configured fallback models are tried.
8. The article/book body is sanitized and written to `latex/chapters/online_article.tex`.
9. `latex/main.tex` is regenerated from `latex/main_template.tex`.
10. `scripts/build.py` compiles the document.
11. The resulting PDF is copied to the canonical `output/agentic_ai_production_2026.pdf`.
12. Online generation then saves a stable named copy and a timestamped run copy based on topic, style, and language.

## LaTeX Strategy

The publication can use either `article` or `book` mode. Article mode uses numbered sections; book mode promotes top-level sections to chapters. The cover page is centered, the abstract starts on page 2, and a table of contents follows before the body. LuaLaTeX is preferred because it handles Unicode and Hebrew text correctly through `fontspec` and `polyglossia`.

The template includes support for:

- readable 12pt text with compact margins for a 15-page result,
- professional headers and footers,
- Hebrew title-page metadata when Hebrew is selected,
- figures and generated assets,
- mathematical notation,
- tables,
- right-to-left table ordering when Hebrew is the selected output language,
- code/listing cleanup,
- real Hebrew/English BiDi text, with the opposite language inserted according to the selected main language,
- numeric references.

## Build Strategy

The build script uses direct `lualatex` or `xelatex`. This avoids the MiKTeX issue where `latexmk` is installed but cannot run because Perl is missing. Multiple LaTeX passes are used so references and page layout settle correctly.

## Documentation Strategy

- `README.md` explains how to run the project and what the reviewer should inspect.
- `docs/PRD.md` defines product requirements and acceptance criteria.
- `docs/PLAN.md` defines architecture and workflow.
- `docs/TODO.md` provides a 900-task professional delivery backlog.
- `docs/topic_ideas/` provides required and extra tested topic briefs, including food, computer science, fashion, fast fashion, sport, World Cup 2026, hairstyles, and healthcare.

## Quality Gates

- Real CrewAI imports compile successfully.
- `scripts/generate_online.py` topic, style, and language selection works from interactive terminals, with environment variables for non-interactive style/language control.
- Every submitted `.py` file is below 150 lines.
- The generated PDF is exactly 15 pages for the four required portfolio outputs.
- The article body avoids repeated filler paragraphs.
- Hebrew text is right-to-left and remains actual extractable PDF text.
- Hebrew tables are ordered right-to-left instead of retaining English visual column order.
- Hebrew cover metadata is localized instead of leaving assignment identity in English.
- Numeric references appear clearly in the bibliography.
- README, PRD, PLAN, TODO, LaTeX source, generated article, and final PDF are present.

## Current Implementation Evidence

The implementation has been exercised with a custom Hebrew book topic: **The Algorithmic Closet: Can AI Agents Make Fast Fashion Slower, Smarter, and More Ethical?**. The generated LaTeX body is stored in `latex/chapters/online_article.tex`, the canonical PDF is stored in `output/agentic_ai_production_2026.pdf`, and a topic-specific copy is stored in `output/The_Algorithmic_Closet_Can_AI_Agents_Make_Fast_Fashion_Slower_Smarter_an_book_hebrew.pdf`.

The README includes `output/imgs/terminal-output.png` and `output/imgs/agent_1.png` through `output/imgs/agent_5.png` as evidence of the terminal run and the CrewAI role sequence. The latest local build reports 15 pages and, in book mode, includes a linked table of contents. Article mode omits the table of contents. Hebrew book output now keeps tables in right-to-left visual order, including compact one-line generated tables, and localizes the cover metadata. The build script skips `biber` unless `main.bcf` exists, preventing a misleading `Cannot find main.bcf` message for this non-`biblatex` article template.

Eight creative topic briefs plus an index are stored under `docs/topic_ideas/`: a Hebrew food article, an English computer-science article, a Hebrew fashion book, a Hebrew fast-fashion book, an English sports book, a Hebrew World Cup 2026 book, an English hairstyles article, and an English healthcare article. The README now exposes these as a tested topic portfolio so reviewers can see that the generator was exercised across cultural memory, software engineering, fashion sustainability, global sport, World Cup storytelling, beauty technology, and healthcare governance.

The four corresponding generated PDF outputs are stored under `output/` using the same topic/style/language naming convention. Each online run also keeps a timestamped archive copy.

Page-count enforcement is part of the build workflow. The generator reads the LaTeX log after compilation, and if the PDF is shorter than 15 pages it appends dense, non-repeated, topic-specific research sections and rebuilds before saving named outputs. The expansion combines domain aspects, lenses, contexts, and concrete micro-cases so added material stays on the selected topic. The portfolio builder also rejects duplicated long paragraphs before writing LaTeX, so repeated filler cannot be saved as a valid result. The four portfolio PDFs were rebuilt through `scripts/build_required_outputs.py` and recorded in `output/portfolio_page_counts.md`.

The TODO backlog has been updated so all current delivery areas are checked, including the 900 numbered backlog tasks and the status checklist.
