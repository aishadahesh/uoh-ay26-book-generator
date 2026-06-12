HEBREW_COVER = {
    "authors": "שמות הכותבים: עאישה אבו דאהש, יוסף אסדי",
    "course": "שם הקורס: אורקסטריצה של סוכני AI",
    "assignment": "מטלה 03",
    "lecturer": 'שם המרצה: ד"ר יורם ראובן סגל',
    "university": "אוניברסיטת חיפה",
    "date": "יוני 2026",
}

ENGLISH_COVER = {
    "authors": "Authors: Aisha Abu Dahesh and Yousef Asadi",
    "course": "Course: Orchestration of AI Agents",
    "assignment": "Assignment 03",
    "lecturer": "Lecturer: Dr. Yoram Reuven Segal",
    "university": "University of Haifa",
    "date": "June 2026",
}


def cover_value(language: str, key: str) -> str:
    values = HEBREW_COVER if language == "hebrew" else ENGLISH_COVER
    return values[key]
