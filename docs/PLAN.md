# PLAN - Online CrewAI and LaTeX Delivery Plan

## Architecture Overview

The project is organized as a professional document-generation pipeline. The Python layer runs the online CrewAI workflow, the LaTeX layer owns publication quality, the docs layer records requirements and planning, and the output folder stores the generated PDF artifact.

The main assignment path is:

1. User chooses an article topic in the terminal.
2. CrewAI agents generate the article online with Gemini or OpenAI.
3. Python sanitizes the generated LaTeX body.
4. The LaTeX template is filled with the selected title.
5. LuaLaTeX/XeLaTeX compiles the final PDF.

## Module Boundaries

- `scripts/generate_online.py` is the main executable assignment workflow.
- `scripts/build.py` compiles the LaTeX project and writes the PDF to `output/`.
- `scripts/setup_env.ps1` creates `.venv-crewai` and installs dependencies.
- `src/book_generator/crewai_llm.py` configures Gemini/OpenAI for CrewAI.
- `src/book_generator/crewai_agents.py` defines CrewAI agents.
- `src/book_generator/crewai_tasks.py` defines CrewAI tasks.
- `src/book_generator/crewai_pipeline.py` creates and runs the CrewAI crew with fallback model handling.
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
3. Enter a custom topic or press Enter for `ARTICLE_TOPIC` / default topic.
4. The script loads `.env` and selects the configured provider.
5. CrewAI sends the task sequence to Gemini or OpenAI.
6. If Gemini fails with transient 500/503 errors, configured fallback models are tried.
7. The article body is sanitized and written to `latex/chapters/online_article.tex`.
8. `latex/main.tex` is regenerated from `latex/main_template.tex`.
9. `scripts/build.py` compiles the document.
10. The resulting PDF is copied to the canonical `output/agentic_ai_production_2026.pdf`; topic-specific PDF copies may also be kept in `output/`.

## LaTeX Strategy

The publication uses an `article` layout rather than a `book` layout to avoid forced blank pages. The title page is centered, the abstract starts on page 2, and the body uses continuous numbered sections. LuaLaTeX is preferred because it handles Unicode and Hebrew text correctly through `fontspec` and `polyglossia`.

The template includes support for:

- readable margins and 12pt text,
- professional headers and footers,
- figures and generated assets,
- mathematical notation,
- tables,
- code/listing cleanup,
- real Hebrew/English BiDi text,
- numeric references.

## Build Strategy

The build script uses direct `lualatex` or `xelatex`. This avoids the MiKTeX issue where `latexmk` is installed but cannot run because Perl is missing. Multiple LaTeX passes are used so references and page layout settle correctly.

## Documentation Strategy

- `README.md` explains how to run the project and what the reviewer should inspect.
- `docs/PRD.md` defines product requirements and acceptance criteria.
- `docs/PLAN.md` defines architecture and workflow.
- `docs/TODO.md` provides a 900-task professional delivery backlog.

## Quality Gates

- Real CrewAI imports compile successfully.
- `scripts/generate_online.py` topic selection works from command-line arguments and interactive terminals.
- Every submitted `.py` file is below 150 lines.
- The generated PDF is approximately 15 pages; the latest custom-topic mental-health-crisis build is 15 pages.
- The article body avoids repeated filler paragraphs.
- Hebrew text is right-to-left and remains actual extractable PDF text.
- Numeric references appear clearly in the bibliography.
- README, PRD, PLAN, TODO, LaTeX source, generated article, and final PDF are present.

## Current Implementation Evidence

The implementation has been exercised with a custom terminal topic: **AI Agents for Early Detection of Mental Health Crises Using Multimodal Data**. The generated LaTeX body is stored in `latex/chapters/online_article.tex`, the canonical PDF is stored in `output/agentic_ai_production_2026.pdf`, and a topic-specific copy is stored in `output/AI_Agents_for_Early_Detection_of_Mental_Health_Crises_Using_Multimodal_Data.pdf`.

The README includes `output/imgs/terminal-output.png` as evidence of the terminal run. The latest local build reports 15 pages. The build script now skips `biber` unless `main.bcf` exists, preventing a misleading `Cannot find main.bcf` message for this non-`biblatex` article template.

The TODO backlog has been updated so completed implementation areas are checked while future or optional work remains open.