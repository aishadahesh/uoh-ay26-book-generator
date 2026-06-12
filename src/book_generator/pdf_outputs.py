from datetime import datetime
from pathlib import Path
import re
import shutil


def topic_slug(topic: str) -> str:
    cleaned = re.sub(r"[^\w\u0590-\u05FF]+", "_", topic, flags=re.UNICODE)
    return cleaned.strip("_")[:72] or "generated_publication"


def copy_named_outputs(canonical_pdf: Path, topic: str, style: str, language: str) -> list[Path]:
    if not canonical_pdf.exists():
        return []
    base = f"{topic_slug(topic)}_{style}_{language}"
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    targets = [
        canonical_pdf.with_name(f"{base}.pdf"),
        canonical_pdf.with_name(f"{base}_{timestamp}.pdf"),
    ]
    for target in targets:
        if target != canonical_pdf:
            shutil.copyfile(canonical_pdf, target)
    return targets
