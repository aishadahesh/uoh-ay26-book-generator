import os

from book_generator.crewai_agents import create_agents
from book_generator.crewai_llm import build_llm, provider_models
from book_generator.crewai_tasks import create_tasks


def run_article_crew(topic: str) -> str:
    os.environ.setdefault("CREWAI_TRACING_ENABLED", "false")
    try:
        from crewai import Crew, Process
    except ImportError as exc:
        raise RuntimeError("CrewAI is required for this assignment path.") from exc
    provider = os.getenv("LLM_PROVIDER", "gemini").lower()
    last_error = None
    for model in provider_models(provider):
        try:
            print(f"Running CrewAI with {provider} model: {model or 'default'}")
            llm = build_llm(provider, model)
            agents = create_agents(llm)
            tasks = create_tasks(topic, agents)
            crew = Crew(
                agents=list(agents),
                tasks=tasks,
                process=Process.sequential,
                verbose=True,
                memory=False,
            )
            return _result_text(crew.kickoff(inputs={"topic": topic}))
        except Exception as exc:
            last_error = exc
            print(f"CrewAI model {model or 'default'} failed: {exc}")
    raise RuntimeError(f"All CrewAI models failed: {last_error}")


def _result_text(result) -> str:
    for name in ("raw", "output", "final_output"):
        value = getattr(result, name, None)
        if value:
            return str(value)
    return str(result)
