# uoh-ay26-book-generator

Professional online CrewAI + LaTeX article generator for Assignment 03.

## Authors

Aisha Abu Dahesh and Yousef Asadi

## Assignment Context

This repository implements Assignment 03: generate an approximately 15-page article/book using CrewAI agents, then produce the final PDF through a LaTeX project. The main grading artifact is the PDF, but the repository also documents the product requirements, plan, backlog, code structure, environment setup, and reproducible build process.

The project is online by design. `scripts/generate_online.py` starts a real CrewAI crew with separate planning, research, writing, LaTeX engineering, and QA responsibilities. The crew calls Gemini or OpenAI through CrewAI `LLM`, writes LaTeX section content, sanitizes common generated-LaTeX problems, and compiles the PDF with LuaLaTeX/XeLaTeX.

## Final PDF

The canonical generated PDF is:

`output/agentic_ai_production_2026.pdf`

Topic-specific copies may also appear in `output/`, for example `output/AI_Agents_in_Healthcare.pdf`, when a custom article topic is generated.

The delivered article is a research-style technical paper with a centered title page, abstract on page 2, continuous article body, professional headers and footers, figures, a graph, a table, a formula, real Hebrew/English BiDi text, and numeric references. The assignment target is approximately 15 pages; the latest custom-topic healthcare build is 17 pages.

## Repository Structure

```text
uoh-ay26-book-generator/
|-- README.md
|-- pyproject.toml
|-- requirements.txt
|-- docs/
|   |-- PRD.md
|   |-- PLAN.md
|   `-- TODO.md
|-- latex/
|   |-- main.tex
|   |-- main_template.tex
|   |-- references.bib
|   |-- assets/
|   `-- chapters/
|       `-- online_article.tex
|-- output/
|   `-- agentic_ai_production_2026.pdf
|-- scripts/
|   |-- build.py
|   |-- generate_online.py
|   `-- setup_env.ps1
|-- src/
|   `-- book_generator/
|-- tests/
`-- ref/
```

## CrewAI Architecture

The online workflow uses actual CrewAI primitives, not only a static imitation:

- `Agent` objects define role, goal, backstory, and constraints.
- `Task` objects define expected outputs for each role.
- `Crew` coordinates the work through `Process.sequential`.
- `LLM` connects the crew to Gemini or OpenAI.
- A LaTeX sanitizer protects the build from typical LLM output mistakes, including generated preambles, nested bibliographies, markdown formatting, and malformed list blocks.
- `scripts/build.py` compiles the final PDF with direct `lualatex` or `xelatex`.

The CrewAI roles are:

- Planner Agent: converts the assignment into acceptance criteria and structure.
- Research Agent: frames the scholarly claims and reference needs.
- Writer Agent: produces coherent research-article prose.
- LaTeX Engineer Agent: requests valid LaTeX sections, figures, tables, formulas, references, and BiDi text.
- QA Agent: checks that the article is useful as a PDF submission, not just fluent text.

## Python Modules

The package under `src/book_generator/` is split into small files so every submitted `.py` file remains below 150 lines.

- `config.py` - project metadata and paths.
- `models.py` - dataclasses for local document models.
- `agents.py` - legacy/static role definitions retained for tests and reference.
- `pipeline.py` - deterministic support pipeline retained for local checks.
- `rendering.py` - Markdown rendering helper.
- `cli.py` - command-line entry point.
- `crewai_llm.py` - Gemini/OpenAI CrewAI LLM configuration.
- `crewai_agents.py` - real CrewAI agent definitions.
- `crewai_tasks.py` - real CrewAI task definitions.
- `crewai_pipeline.py` - live Crew execution with fallback model handling.
- `latex_sanitizer.py` - cleanup for generated LaTeX before compilation.

## Environment Setup

CrewAI requires a modern Python version. Use Python 3.12 and the provided setup script. If your terminal prompt shows `(.venv)`, run `deactivate` first; the online CrewAI workflow should run from `(.venv-crewai)`:

```powershell
.\scripts\setup_env.ps1
.\.venv-crewai\Scripts\Activate.ps1
```

The setup installs:

- `crewai[google-genai]` for the online CrewAI workflow.
- `openai` for the optional OpenAI provider.
- `python-dotenv` for `.env` loading.
- `pytest` for validation.

Create your local environment file:

```powershell
Copy-Item .env.example .env
```

For Gemini, set:

```text
LLM_PROVIDER=gemini
GEMINI_API_KEY=your_key_here
GEMINI_MODEL=gemini-2.5-flash-lite
GEMINI_FALLBACK_MODELS=gemini-2.0-flash,gemini-1.5-flash
```

For OpenAI, set:

```text
LLM_PROVIDER=openai
OPENAI_API_KEY=your_key_here
OPENAI_MODEL=gpt-5.2
```

API keys belong only in `.env`; do not commit them.

## Online Generation

Run the assignment workflow from the activated environment:

```powershell
python scripts/generate_online.py
```

The script asks for the article topic in the terminal:

```text
CrewAI article generation
Default topic: Production-Ready AI Agent Architecture in 2026
Enter article topic, or press Enter to use the default:
```

You can also pass the topic directly:

```powershell
python scripts/generate_online.py "AI Agents for Clinical Decision Support"
```

The script then:

1. Loads `.env`.
2. Builds the real CrewAI crew.
3. Sends the topic to the online model provider.
4. Writes the generated article body to `latex/chapters/online_article.tex`.
5. Rewrites `latex/main.tex` from `latex/main_template.tex`.
6. Compiles the PDF through `scripts/build.py`.
7. Writes `output/agentic_ai_production_2026.pdf`.

If Gemini returns a temporary 500/503 high-demand server error or a quota error, the runner tries the configured fallback models. The default starts with `gemini-2.5-flash-lite` because it is usually less overloaded than `gemini-2.5-flash`. This is expected behavior for online LLM workflows.

## Local LaTeX Build

To rebuild the PDF from existing LaTeX sources without asking the agents to write new text:

```powershell
python scripts/build.py
```

The build script avoids the MiKTeX `latexmk`/Perl problem by preferring direct `lualatex` or `xelatex`. LuaLaTeX is recommended because the article contains Unicode and Hebrew text.

## Documentation

The required Markdown documentation is in `docs/`:

- `PRD.md` explains product goals, users, requirements, acceptance criteria, and risks.
- `PLAN.md` explains architecture, workflow, CrewAI design, LaTeX strategy, and quality gates.
- `TODO.md` contains a 900-task professional backlog.

## Quality Notes

The latest project revisions address the requested grading concerns:

- The workflow is real online CrewAI generation, not manual offline writing.
- The PDF uses a continuous article layout with no forced empty book pages.
- The title page is centered and the abstract starts on the next page.
- The body is page-dense without repeating filler paragraphs; exact page count can vary by generated topic length.
- Hebrew is rendered as live right-to-left text, not as a screenshot.
- References are numeric and ordered like a paper bibliography.
- Every submitted `.py` file is below 150 lines.
