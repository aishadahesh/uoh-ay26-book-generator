def create_agents(llm):
    from crewai import Agent

    planner = Agent(
        role="Assignment Planner and Architecture Lead",
        goal="Turn the assignment into a rigorous modular plan for a 15-page article generator.",
        backstory="You design professional AI-agent software projects with clear deliverables.",
        llm=llm,
        verbose=True,
        allow_delegation=False,
    )
    researcher = Agent(
        role="Research Agent",
        goal="Develop a recent, research-level conceptual frame for production AI agents.",
        backstory="You connect agent frameworks, governance, observability, and security literature.",
        llm=llm,
        verbose=True,
        allow_delegation=False,
    )
    writer = Agent(
        role="Research Article Writer",
        goal="Write dense, original, non-repetitive article sections with numeric citations.",
        backstory="You write academic technical papers with clear arguments and full pages of content.",
        llm=llm,
        verbose=True,
        allow_delegation=False,
    )
    latex_engineer = Agent(
        role="LaTeX Publication Engineer and BiDi Specialist",
        goal="Produce valid LuaLaTeX article body content with figures, table, formula, and Hebrew RTL text.",
        backstory="You know professional LaTeX typography, Unicode, Hebrew BiDi, and PDF quality checks.",
        llm=llm,
        verbose=True,
        allow_delegation=False,
    )
    qa = Agent(
        role="PDF Quality Assurance Reviewer",
        goal="Reject repeated filler, sparse pages, broken references, and malformed Hebrew text.",
        backstory="You review final academic PDFs against strict course rubrics and engineering constraints.",
        llm=llm,
        verbose=True,
        allow_delegation=False,
    )
    return planner, researcher, writer, latex_engineer, qa
