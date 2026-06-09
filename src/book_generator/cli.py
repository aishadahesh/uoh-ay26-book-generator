import argparse

from .config import BookConfig
from .pipeline import BookPipeline
from .rendering import render_markdown


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate the assignment manuscript.")
    parser.add_argument("--topic", default=BookConfig.topic)
    parser.add_argument("--author", default=BookConfig.author)
    args = parser.parse_args()

    config = BookConfig(topic=args.topic, author=args.author)
    manuscript = BookPipeline(config).run()
    render_markdown(manuscript, config.output_dir / "manuscript.md")
    print(f"Generated {config.output_dir / 'manuscript.md'}")


if __name__ == "__main__":
    main()
