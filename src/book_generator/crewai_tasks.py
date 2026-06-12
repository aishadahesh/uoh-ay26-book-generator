def create_tasks(options, agents):
    from crewai import Task

    topic = options.topic
    style = options.document_style
    language = options.output_language
    opposite = "English" if language == "hebrew" else "Hebrew"
    top_level = "one \\chapter followed by \\section" if style == "book" else "\\section"
    language_rule = (
        "Write the entire main body in Hebrew. Use English only in the required BiDi section."
        if language == "hebrew"
        else "Write the entire main body in English. Use Hebrew only in the required BiDi section."
    )
    rtl_table_rule = (
        "For Hebrew output, organize tables right-to-left: put the first logical column on the "
        "visual right, reverse the LaTeX column order, and right-align paragraph columns."
        if language == "hebrew"
        else "For English output, keep tables left-to-right with standard readable column order."
    )
    planner, researcher, writer, latex_engineer, qa = agents
    plan = Task(
        description=(
            f"Create a detailed plan for a 15-page {style} about {topic}. {language_rule} "
            "The plan must include cover, abstract, headers/footers, numeric references, one figure, "
            f"one table, one formula, and a real BiDi paragraph in {opposite}. "
            f"{rtl_table_rule} "
            "Book mode has a table of contents; article mode does not. Avoid sparse pages."
        ),
        expected_output="A concise publication architecture and acceptance checklist.",
        agent=planner,
    )
    research = Task(
        description=(
            f"Build the research frame for {topic}. Connect the topic to production AI agents, CrewAI "
            "role discipline, governed runtimes, observability, evaluation metrics, and document "
            f"generation as an auditable case study. {language_rule} Use numeric citation keys."
        ),
        expected_output="A structured research brief with section claims and citation keys.",
        agent=researcher,
        context=[plan],
    )
    draft = Task(
        description=(
            f"Write a dense 4200-5200 word research-level {style} body. {language_rule} "
            f"Use {top_level} commands; do not create many chapters. Do not include title, author, "
            "date, maketitle, abstract, table of contents, documentclass, packages, begin-document, "
            "or bibliography. Every paragraph must add new content, not repeated filler."
        ),
        expected_output="A complete LaTeX body with original research-level prose.",
        agent=writer,
        context=[plan, research],
    )
    latex = Task(
        description=(
            "Convert the draft into final valid LaTeX body content. Include two figures referencing "
            "assets/agent_runtime_architecture.png and assets/readiness_chart.png, one booktabs table, "
            f"one equation, and a real {opposite} BiDi section. {rtl_table_rule} "
            "Return body content only."
        ),
        expected_output="Final compilable LaTeX body content only, no Markdown fences.",
        agent=latex_engineer,
        context=[draft],
    )
    review = Task(
        description=(
            f"Repair the body for a polished 15-page result. {language_rule} Ensure no repeated "
            f"paragraphs, no generated front matter, numeric citations, real {opposite} BiDi text, "
            f"and compact book structure without blank pages. {rtl_table_rule} "
            "Return only corrected LaTeX body."
        ),
        expected_output="Corrected final LaTeX body only.",
        agent=qa,
        context=[latex],
    )
    return [plan, research, draft, latex, review]
