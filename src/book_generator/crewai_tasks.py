def create_tasks(topic: str, agents):
    from crewai import Task

    planner, researcher, writer, latex_engineer, qa = agents
    plan = Task(
        description=(
            f"Create a detailed plan for a 15-page research article about {topic}. "
            "The plan must satisfy a CrewAI + LaTeX assignment, include real code-driven PDF generation, "
            "avoid repetition, and require Hebrew/English BiDi text as real text."
        ),
        expected_output="A concise but complete article architecture and acceptance checklist.",
        agent=planner,
    )
    research = Task(
        description=(
            "Build the research frame for production AI agents in 2026. Cover CrewAI role discipline, "
            "LangGraph/LangChain comparison, governed runtimes, observability, security, human approval, "
            "evaluation metrics, and document generation as a case study. Use numeric citation keys."
        ),
        expected_output="A structured research brief with section claims and citation keys.",
        agent=researcher,
        context=[plan],
    )
    draft = Task(
        description=(
            "Write a dense 6500-7500 word research article body in LaTeX. Use only \\section and "
            "\\subsection. Do not use \\chapter, \\documentclass, or the begin-document command. "
            "Every section must contain new argumentation, not repeated filler. Include numeric citations."
        ),
        expected_output="A complete LaTeX article body with long, original, research-level prose.",
        agent=writer,
        context=[plan, research],
    )
    latex = Task(
        description=(
            "Convert the draft into final valid LaTeX body content. Include two figures referencing "
            "assets/agent_runtime_architecture.png and assets/readiness_chart.png, one booktabs table, "
            "one readiness equation, and a real Hebrew section using the Hebrew and flushright environments."
        ),
        expected_output="Final compilable LaTeX body content only, no Markdown fences.",
        agent=latex_engineer,
        context=[draft],
    )
    review = Task(
        description=(
            "Review and repair the LaTeX body. Ensure no repeated paragraphs, no sparse placeholder text, "
            "numeric citation commands, real Hebrew text, and enough content for a 15-page PDF. "
            "Return only the corrected LaTeX body."
        ),
        expected_output="Corrected final LaTeX body only.",
        agent=qa,
        context=[latex],
    )
    return [plan, research, draft, latex, review]


