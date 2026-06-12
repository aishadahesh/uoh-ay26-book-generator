FAST_FASHION_TITLE = "הארון האלגוריתמי: האם סוכני AI יכולים להפוך אופנה מהירה לאיטית, חכמה ואתית יותר?"


def localized_title(topic: str, language: str) -> str:
    if language != "hebrew":
        return topic
    lower = topic.lower()
    if "fast fashion" in lower or "algorithmic closet" in lower:
        return FAST_FASHION_TITLE
    if "algorithmic hair" in lower or "hairstyle" in lower:
        return "שיער אלגוריתמי: סוכני AI, זהות תסרוקת, סטנדרטים של יופי וביטוי אישי"
    return topic
