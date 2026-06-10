# uoh-ay26-book-generator

**Online CrewAI + LaTeX research-article generator for Assignment 03**

This project turns the assignment into a working production-style pipeline: a real CrewAI crew receives an article topic, writes a research-level LaTeX article online through Gemini/OpenAI, sanitizes the generated LaTeX, compiles the result with LuaLaTeX/XeLaTeX, and stores the final PDF as a submission artifact.

## Authors

Aisha Abu Dahesh and Yousef Asadi

## What This Project Does

The assignment asks for a 15-page article/book generated with CrewAI and LaTeX. This repository implements that as a complete software project, not as a one-time pasted answer.

The workflow is:

```text
Topic from terminal
      |
      v
CrewAI planner, researcher, writer, LaTeX engineer, QA reviewer
      |
      v
Generated LaTeX article body
      |
      v
Sanitizer for generated-LaTeX problems
      |
      v
LuaLaTeX/XeLaTeX build
      |
      v
15-page research-style PDF in output/
```

Example terminal execution:

![Terminal output example](output/imgs/terminal-output.png)

## Final Results

The latest successful generated topic was:

**AI Agents for Early Detection of Mental Health Crises Using Multimodal Data**

Generated outputs:

- Canonical PDF: `output/agentic_ai_production_2026.pdf`
- Topic-specific PDF: `output/AI_Agents_for_Early_Detection_of_Mental_Health_Crises_Using_Multimodal_Data.pdf`
- Previous topic example: `output/AI_Agents_in_Healthcare.pdf`

Latest verified build result:

```text
Output written on main.pdf (15 pages, 261859 bytes)
pytest: 1 passed
Python source files: all below 150 lines
TODO backlog: 900 tasks, 660 checked, 240 open
```

The PDF includes a centered title page, abstract on page 2, dense research prose, generated figures, chart, table, formula, numeric references, and live Hebrew/English BiDi text.

## Visual Evidence

### Runtime Architecture

The article includes a visual explanation of the governed agent runtime used as the conceptual backbone for the paper.

![Agent runtime architecture](latex/assets/agent_runtime_architecture.png)

### Readiness Evaluation

The generated chart supports the readiness/evaluation section of the article and shows how the PDF combines prose, figures, and code-generated evidence.

![Readiness chart](latex/assets/readiness_chart.png)

### BiDi Rendering Requirement

The project supports Hebrew as real right-to-left text in LaTeX through `polyglossia`, rather than treating Hebrew as an image-only artifact.

![BiDi page preview](latex/assets/bidi_hebrew_page.png)


### Implementation Pipeline

This generated diagram shows the actual execution path from terminal topic input through CrewAI, sanitization, LaTeX compilation, and PDF output.

![Implementation pipeline](output/imgs/implementation-pipeline.png)
## Repository Structure

```text
uoh-ay26-book-generator/
|-- README.md                         # Main reviewer guide, run instructions, results, self-score
|-- pyproject.toml                    # Python package metadata, dependencies, pytest config
|-- requirements.txt                  # Installable runtime/test dependency list
|-- .env.example                      # Safe API-key template; copy to .env locally
|-- docs/
|   |-- PRD.md                        # Product goals, acceptance criteria, risks, delivered evidence
|   |-- PLAN.md                       # Architecture, workflow, quality gates, current implementation evidence
|   `-- TODO.md                       # 900-task backlog with completed work checked
|-- src/book_generator/
|   |-- crewai_agents.py              # CrewAI Agent roles
|   |-- crewai_tasks.py               # Planner, research, writer, LaTeX, QA task chain
|   |-- crewai_pipeline.py            # Sequential Crew runner and fallback model loop
|   |-- crewai_llm.py                 # Gemini/OpenAI LLM setup for CrewAI
|   |-- latex_sanitizer.py            # Cleans generated LaTeX before compilation
|   |-- online_providers.py           # Provider utilities retained for compatibility/reference
|   |-- pipeline.py                   # Deterministic support pipeline used by tests
|   |-- models.py                     # Local manuscript dataclasses
|   |-- config.py                     # Shared paths and metadata
|   |-- rendering.py                  # Markdown rendering helper
|   `-- cli.py                        # Package CLI entry point
|-- scripts/
|   |-- setup_env.ps1                 # Creates .venv-crewai with Python 3.12
|   |-- generate_online.py            # Main online CrewAI generator with topic prompt
|   `-- build.py                      # Direct LuaLaTeX/XeLaTeX builder, no Perl/latexmk dependency
|-- latex/
|   |-- main.tex                      # Current generated publication entry point
|   |-- main_template.tex             # Reusable article shell
|   |-- references.bib                # Reference database retained with LaTeX project
|   |-- assets/                       # Figures and chart assets
|   `-- chapters/
|       `-- online_article.tex        # Latest generated article body after sanitization
|-- output/
|   |-- agentic_ai_production_2026.pdf
|   |-- AI_Agents_for_Early_Detection_of_Mental_Health_Crises_Using_Multimodal_Data.pdf
|   |-- AI_Agents_in_Healthcare.pdf
|   `-- imgs/
|       |-- terminal-output.png       # Terminal run screenshot used in this README
|       `-- implementation-pipeline.png # Generated diagram of the online CrewAI-to-PDF flow
|-- tests/
|   `-- test_pipeline.py              # Smoke test for package import and pipeline behavior
`-- ref/                              # Local course/reference material, ignored by git
```

## Implementation Highlights

### Real Online CrewAI Flow

The central executable is `scripts/generate_online.py`. It is intentionally small and orchestration-focused: it loads environment variables, chooses the article topic, calls the CrewAI pipeline, sanitizes the returned LaTeX body, writes the LaTeX project files, starts the PDF build, and creates a topic-specific PDF copy when the build succeeds.

The script supports two usage modes. In interactive mode, it asks the user for a topic in the terminal, which makes the project easy to demonstrate during review. In direct mode, the topic is passed as command-line text, for example `python scripts/generate_online.py "AI Agents in Healthcare"`. This makes the project reproducible and scriptable.

A Python version guard is included at startup. If the user accidentally runs from the old `(.venv)` Python 3.9 environment, the script prints a clear instruction to activate `.venv-crewai` instead of failing with an obscure type-hint or CrewAI import error.

### CrewAI Module Design

The live agent system is split into dedicated files so the architecture is easy to inspect:

- `crewai_agents.py` defines the specialized agents: assignment planner, research agent, article writer, LaTeX publication engineer, and PDF QA reviewer.
- `crewai_tasks.py` defines the task chain and expected outputs, so each agent knows what artifact it must produce.
- `crewai_llm.py` builds the CrewAI `LLM` object for Gemini or OpenAI and validates that the required API key exists.
- `crewai_pipeline.py` creates the `Crew`, runs `Process.sequential`, and retries through configured Gemini fallback models when a model is overloaded.

This separation matters because generated-document failures can come from different layers. If the topic is weak, the planning task can be improved. If the prose is sparse, the writer task can be changed. If the PDF fails, the sanitizer or LaTeX template can be adjusted without rewriting the whole crew.

### Agent Responsibilities

The crew is designed like a miniature production team:

| Agent | Main responsibility | Why it matters |
|---|---|---|
| Planner | Converts the assignment into structure and acceptance criteria | Prevents the article from becoming a loose prompt response |
| Researcher | Frames claims, references, risks, and evaluation concepts | Makes the output more research-like |
| Writer | Produces dense, section-specific prose | Avoids sparse pages and repeated filler |
| LaTeX Engineer | Requests valid LaTeX sections, figures, tables, formulas, and BiDi text | Keeps the PDF buildable |
| QA Reviewer | Checks repetition, layout expectations, references, and submission requirements | Adds a final critique pass before compilation |

The use of separate agents is not decorative. It makes the assignment's main point visible: agent design is about role boundaries, task contracts, and reviewable outputs.

### LaTeX as a Stable Publication Layer

The model is not allowed to control the entire LaTeX document. Instead, the project keeps a stable publication shell in `latex/main_template.tex`. That shell owns the title page, abstract page, page geometry, headers, fonts, spacing, Hebrew language configuration, figures, and numeric bibliography.

The CrewAI output is treated as article body content and stored in `latex/chapters/online_article.tex`. This design keeps the generated content flexible while protecting the parts of the document that must remain stable for professional layout.

When a new topic is generated, `generate_online.py` replaces the title placeholder in the template, writes a fresh `latex/main.tex`, and then runs the build. The result is a real LaTeX project, not a PDF-only artifact.

### Sanitizer for Real LLM Output

The sanitizer is one of the most important implementation pieces. Real online LLMs often return text that looks reasonable but breaks LaTeX. The project therefore runs generated content through `latex_sanitizer.py` before compilation.

It handles:

- accidental `\documentclass` and `\usepackage` preambles,
- generated `\begin{document}` and `\end{document}` wrappers,
- generated `\bibliography`, `\bibliographystyle`, and nested `thebibliography` blocks,
- markdown code fences and markdown links,
- inline backtick code conversion to `\texttt{...}`,
- unbalanced `itemize` and `enumerate` environments,
- unsafe ampersands outside tables,
- mojibake/corrupted generated Hebrew lines,
- known generated LaTeX phrases that commonly break compilation.

This is the part that turns the project from a fragile demo into a repeatable generation pipeline. It accepts that LLMs are imperfect and adds a repair layer before the PDF compiler sees the content.

### MiKTeX-Friendly Build Strategy

`scripts/build.py` avoids relying on `latexmk` because on Windows/MiKTeX it can fail when Perl is missing. The script searches for `lualatex` or `xelatex`, runs multiple passes, and copies `latex/main.pdf` into `output/agentic_ai_production_2026.pdf`.

The script also avoids a misleading `biber` failure. It only runs `biber` when `main.bcf` exists, which means the current non-`biblatex` article template does not produce a false `Cannot find main.bcf` error.

### Output Management

The canonical PDF path is always `output/agentic_ai_production_2026.pdf`. When the build succeeds from an online topic run, the project also creates a topic-specific copy, such as `output/AI_Agents_for_Early_Detection_of_Mental_Health_Crises_Using_Multimodal_Data.pdf`.

This gives reviewers one stable file to grade while still preserving evidence of custom-topic generation.

### Validation and Evidence

Validation is intentionally lightweight but meaningful. `pytest` checks the package import and deterministic support pipeline. The README records the latest PDF page count, terminal screenshot, output paths, and TODO completion status. The final PDF is also visually supported by generated assets under `latex/assets/` and `output/imgs/`.

Every submitted Python file is kept under 150 lines. That constraint shaped the implementation: instead of one large script, the project uses small modules with clear ownership.
## How To Run

Create the environment:

```powershell
cd C:\Users\Aisha\Desktop\AI\uoh-ay26-book-generator
.\scripts\setup_env.ps1
.\.venv-crewai\Scripts\Activate.ps1
```

If your prompt says `(.venv)`, leave it first:

```powershell
deactivate
.\.venv-crewai\Scripts\Activate.ps1
```

Create local API configuration:

```powershell
Copy-Item .env.example .env
```

For Gemini:

```text
LLM_PROVIDER=gemini
GEMINI_API_KEY=your_key_here
GEMINI_MODEL=gemini-2.5-flash-lite
GEMINI_FALLBACK_MODELS=gemini-2.0-flash,gemini-1.5-flash
```

Generate a new article interactively:

```powershell
python scripts/generate_online.py
```

Or pass the topic directly:

```powershell
python scripts/generate_online.py "AI Agents for Early Detection of Mental Health Crises Using Multimodal Data"
```

Save terminal output while still seeing it:

```powershell
python scripts/generate_online.py "Your Topic" 2>&1 | Tee-Object run-log.txt
```

Rebuild the current LaTeX project without calling the online model:

```powershell
python scripts/build.py
```

## Documentation Package

The `docs/` folder is part of the submission, not decoration.

- `PRD.md` explains goals, non-goals, functional requirements, acceptance criteria, risks, and delivered results.
- `PLAN.md` explains architecture, module boundaries, CrewAI role discipline, workflow, LaTeX strategy, quality gates, and implementation evidence.
- `TODO.md` contains a 900-task backlog. Completed implemented areas are checked; future or optional work remains open.

## Quality Gates

| Gate | Status | Evidence |
|---|---:|---|
| Real online CrewAI workflow | Passed | `Agent`, `Task`, `Crew`, `Process.sequential`, `LLM` modules |
| Terminal topic prompt | Passed | `scripts/generate_online.py` |
| LaTeX PDF build | Passed | `Output written on main.pdf (15 pages, 261859 bytes)` |
| Python file size limit | Passed | Largest submitted `.py` file is below 150 lines |
| Tests | Passed | `pytest: 1 passed` |
| Hebrew/BiDi support | Passed | `polyglossia`, `hebrew` environment, live text fallback |
| Required docs | Passed | README, PRD, PLAN, TODO present |
| TODO size | Passed | 900 tasks |
| Terminal evidence | Passed | `output/imgs/terminal-output.png` |

## Self-Scoring Grade

Our estimated grade for this assignment is:

**87 / 100**

| Category | Score | Reasoning |
|---|---:|---|
| Assignment compliance | 19 / 20 | Includes README, PRD, PLAN, TODO, LaTeX project, generated PDFs, a 900-task backlog, and modular code. |
| Real CrewAI implementation | 17 / 20 | Uses actual CrewAI agents, tasks, crew execution, online LLM configuration, and fallback models. Some behavior still depends on provider availability. |
| PDF quality and research style | 16 / 20 | Produces a 15-page research-style PDF with figures, table, formula, references, and BiDi text, but final article quality still depends on the generated model response. |
| Modularity and code quality | 14 / 15 | Source files are small, separated by responsibility, and stay below 150 lines. A few legacy/reference modules remain for compatibility. |
| Documentation depth | 13 / 15 | README, PRD, PLAN, and TODO are detailed, include evidence, and describe implementation/results clearly. More formal source evaluation could improve it further. |
| Robustness and validation | 8 / 10 | Sanitizer, fallback models, version guard, and tests improve robustness. Online 503/quota errors and LLM variability remain real risks. |

Why not 100? The project is strong and complete, but it is still an online generative workflow. Gemini availability can affect generation, model output can vary between runs, and a final human review is still needed before academic submission. The safest self-score is therefore high but not perfect.
