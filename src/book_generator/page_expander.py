def expansion_pages(options, missing_pages: int, start: int = 0) -> str:
    domain = _domain(options.topic)
    if getattr(options, "output_language", "") == "hebrew" and domain not in ("food", "fashion"): domain = "fashion"
    count = expansion_count(missing_pages)
    return expansion_pages_for_count(domain, count, start)


def expansion_pages_for_count(domain, count: int, start: int = 0) -> str:
    return "\n\n".join(_render(domain, start + index) for index in range(count))


def expansion_count(missing_pages: int) -> int:
    return 0 if missing_pages <= 0 else 8 if missing_pages == 1 else missing_pages * 2 + 4


def _render(domain, index):
    title, angle, evidence, risk, action = _section(domain, index)
    return f"\\section{{{title}}}\n{_paragraphs(angle, evidence, risk, action)}"


def _section(domain, index):
    bank = SECTION_BANKS[domain]
    if index < len(bank):
        return bank[index]
    return _generated_section(domain, index)


def _paragraphs(angle, evidence, risk, action):
    return "\n\n".join([angle, evidence, risk, action])


def _domain(topic):
    if "מתכונים" in topic or "מטבח" in topic:
        return "food"
    if "Hair" in topic or "hair" in topic or "hairstyle" in topic:
        return "hair"
    if "הבגדים" in topic or "אופנה" in topic or "fashion" in topic.lower() or "closet" in topic.lower():
        return "fashion"
    if "Software" in topic or "Repositories" in topic:
        return "code"
    return "sport"


def _generated_section(domain, index):
    aspects = DOMAIN_ASPECTS[domain]
    aspect, evidence_item, risk_item, action_item = aspects[index % len(aspects)]
    lens = LENSES[domain][index % len(LENSES[domain])]
    context = CONTEXTS[domain][index % len(CONTEXTS[domain])]
    case = CASES[domain][index % len(CASES[domain])]
    if domain in ("food", "fashion"):
        title = f"{aspect}, {lens} ו{context}"
        angle = f"הדיון ב{aspect} מקבל משמעות מעשית כאשר בוחנים אותו דרך {lens}, {context} ו{case}, משום שהחיבור ביניהם חושף החלטות קטנות שמעצבות דפוס תרבותי רחב."
        evidence = f"הראיות המרכזיות הן {evidence_item}; דרך {lens}, {context} ו{case} הן מחברות בין פעולה יומיומית, זיכרון אישי, הקשר חברתי והשלכה תרבותית."
        risk = f"הסיכון הוא {risk_item}, ולכן הניתוח של {lens} בתוך {context} ו{case} חייב להבחין בין סיפור מושך לבין מסקנה שאפשר להצדיק באמצעות מקורות ועדויות."
        action = f"השלב המעשי הוא {action_item}. כך ההמלצה נשארת מחוברת ל{context}, ל{case} ולנושא עצמו, ולא הופכת לתיאור כללי."
        return title, angle, evidence, risk, action
    title = f"{aspect} Through {lens} and {context}"
    angle = f"{aspect} becomes concrete when read through {lens}, {context}, and {case}, because the discussion moves from broad possibility to a specific domain pressure."
    evidence = f"The relevant evidence is {evidence_item}; through {lens}, {context}, and {case}, it anchors the claim in observable material rather than generic enthusiasm."
    risk = f"The main risk is {risk_item}, so the argument about {lens} inside {context} and {case} must remain tied to consequences inside the topic."
    action = f"The practical response is to {action_item}. This keeps the recommendation useful for {context} and {case} instead of drifting into process commentary."
    return title, angle, evidence, risk, action


FOOD = [
    ("איסוף ידע בעל פה", "ראיון קולינרי איכותי שואל מי בישל, מי לימד, באיזה חג הופיעה המנה, ומה השתנה כאשר המשפחה עברה מקום.", "הראיה החשובה היא לא רק רשימת רכיבים אלא גם קול, היסוס, תנועה, וסיפור שמסביר מדוע המתכון שרד.", "הסיכון הוא להפוך ידע גופני לטבלה יבשה שמוחקת את מי שהעביר את המתכון.", "המערכת צריכה לשמור אודיו, תמלול, גרסה מבושלת, והערות משפחתיות כיחידות מידע נפרדות."),
    ("מחברת מוכתמת כמקור", "כתמי שמן, מחיקות, קיפולים והערות שוליים מספרים אילו מתכונים באמת חיו במטבח.", "צילום המקור לצד OCR מאפשר לבדוק מה נקרא בוודאות ומה נותר מסופק.", "ניקוי יתר של הטקסט עלול למחוק סימנים חומריים שהם חלק מן הזיכרון.", "הסוכן מסמן אי-ודאות, מציע קריאה אפשרית, ומשאיר את צילום המקור זמין לבדיקה."),
    ("גרסאות בין דורות", "אותו מתכון משתנה כאשר דור חדש מפחית סוכר, מחליף קמח, או מתאים את המנה לטבעונות.", "השוואת גרסאות מראה כיצד מסורת ממשיכה לחיות ולא רק נשמרת בארכיון.", "גרסה יחידה עלולה להציג מסורת כאמת קפואה ולמחוק התאמות משפחתיות.", "המאגר צריך לשמור עץ גרסאות עם תאריך, מבשל, סיבה לשינוי ותוצאה בפועל."),
    ("בעלות והסכמה", "מתכון משפחתי עשוי להיות ידע אישי, משפחתי או קהילתי, ולכן פרסום דורש הרשאה ברורה.", "תיעוד הסכמה מציין מי אישר, מה מותר לשתף, ומה נשאר פרטי.", "הסיכון הוא מסחור ידע ביתי ללא קרדיט או ללא הבנת ההקשר הקהילתי.", "הסוכן מוסיף שכבת הרשאות לפני יצירת PDF ציבורי או שיתוף ברשת."),
    ("תרגום תרבותי", "תרגום מתכון אינו החלפת מילים בלבד; שמות רכיבים וכלים נושאים זיכרון מקומי.", "מונחים מסומנים עם הסבר, מקור, אפשרות החלפה והערת משמעות.", "תרגום גלובלי מדי עלול למחוק טעם, מקום ושפה.", "המערכת מציגה מונח מקורי לצד פירוש במקום להעלים אותו."),
    ("מדדי הצלחה", "הצלחה נמדדת בכמות הסיפורים שנשמרו, במספר הגרסאות המקושרות, וביכולת לבשל מתוך המאגר.", "בדיקת משתמשים מראה האם קוראים מבינים גם את הפעולה וגם את ההקשר המשפחתי.", "מדד של מספר מתכונים בלבד מעודד ארכיון שטוח ולא איכותי.", "המערכת מדרגת תוצר לפי דיוק, הקשר, מקוריות, נגישות ושקיפות."),
    ("חינוך דרך אוכל", "מתכון אחד יכול ללמד היסטוריה, הגירה, אקלים, דת, מסחר ושפה.", "שימוש בכיתה מחבר בין רכיבים לבין מפות, תאריכים וסיפורי משפחה.", "הסיכון הוא להפוך שיעור תרבותי לפעילות בישול בלבד.", "הסוכן מוסיף שאלות מחקר קצרות לצד כל מתכון."),
    ("ביקורת טעם", "AI אינו טועם, אך הוא יכול לזהות זמן אפייה חסר או יחס רכיבים חריג.", "ההתראה מתבססת על השוואה למתכונים דומים ולכללי טכניקה.", "חריגה עשויה להיות סוד משפחתי ולכן אסור למחוק אותה אוטומטית.", "המערכת מציעה בדיקה ומבקשת אישור אנושי לפני תיקון."),
]

FASHION = [
    ("הארון כמאגר זהות", "בגד מייצג זיכרון, גוף, תקציב, מעמד, עונה ורצון להשתייך או להתבדל.", "תדירות לבישה וצירופי פריטים מגלים מה באמת שימושי ולא רק מה נראה טוב.", "הסיכון הוא לצמצם זהות אנושית להמלצה מסחרית.", "הסוכן מסביר מדוע הצעה מתאימה לאירוע, לגוף, למזג האוויר ולערכי המשתמש."),
    ("שימוש חוזר לפני קנייה", "המלצה טובה מתחילה בפריטים קיימים בארון ולא בדחיפת רכישה חדשה.", "מדדי שימוש חוזר והפחתת החזרות בודקים אם המערכת באמת מקיימת.", "אופטימיזציה למכירות בלבד מגבירה צריכה ומחלישה קיימות.", "המערכת מציעה שילוב מחדש, תיקון, השאלה או יד שנייה לפני מוצר חדש."),
    ("פרטיות הגוף", "מידות גוף, תמונות והעדפות צניעות הן מידע רגיש.", "הראיה כוללת מדיניות שמירת נתונים, מחיקה וחישוב מקומי.", "איסוף יתר עלול להפוך התאמה אישית לפולשנות.", "הסוכן שומר מינימום נתונים ומציג למשתמש מה הוסק עליו."),
    ("גיוון תרבותי", "אופנה דתית, מקומית או מסורתית אינה צריכה להפוך לטרנד גלובלי אחיד.", "המערכת מזהה גבולות של צניעות, סמלים וטקסים.", "מחיקת הקשר תרבותי מייצרת המלצות לא רגישות.", "המשתמש יכול להגדיר כללים אישיים וקהילתיים לפני ההמלצה."),
    ("תיקון ותחזוקה", "כפתור חסר או מכפלת ארוכה אינם סיבה אוטומטית לקנייה.", "יומן תיקונים מודד אילו פעולות האריכו חיי בגד.", "הזנחת תחזוקה מחזקת אופנה מהירה.", "הסוכן מציע תיקון, תפירה או צביעה מחדש כחלק מהמלצה."),
    ("מעמד ומחיר", "יוקרה אינה חייבת להיות מותג יקר; היא יכולה להיות התאמה, איכות ושימוש מתמשך.", "השוואת עלות ללבישה חושפת ערך אמיתי של פריט.", "הטיה למותגים יקרים משכפלת פערים חברתיים.", "המערכת מציגה חלופות בתקציבים שונים בלי להוריד איכות המלצה."),
    ("יומן לבישה", "יומן לבישה מלמד מתי בגד נוח, מתי הוא נשאר תלוי, ומתי הוא חוזר לשימוש.", "נתונים לאורך זמן עדיפים על צילום חד-פעמי.", "תמונה יפה לא מבטיחה שימושיות.", "הסוכן לומד ממשוב חוזר ולא רק ממראה חיצוני."),
    ("הסבר המלצה", "המשתמש צריך להבין את סיבת ההמלצה ולא לקבל פלט אטום.", "הסבר כולל צבע, גזרה, אירוע, נוחות, קיימות ותקציב.", "חוסר הסבר מחליש אמון ומגביר תחושת מניפולציה.", "כל המלצה כוללת נימוק קצר ואפשרות לדחות את ההנחה."),
]

CODE = [
    ("Repository Evidence", "A self-healing repository starts from evidence: failing tests, flaky builds, duplicated logic, high churn, and unclear ownership.", "The agent links every claim to files, tests, logs, dependency versions, or issue history.", "Without evidence, the article becomes generic advice rather than engineering analysis.", "The workflow stores observations before proposing patches."),
    ("Risk Ranking", "Not every code smell deserves the same attention; debt near authentication or deployment can be more urgent than cosmetic duplication.", "Risk is estimated from coupling, failure history, ownership, and release impact.", "Equal treatment of all findings wastes review time.", "The agent sorts repairs by operational risk before writing recommendations."),
    ("Characterization Tests", "Before changing legacy behavior, the system should capture what the code currently does.", "Characterization tests document existing outputs and edge cases.", "Refactoring without tests can silently change user-facing behavior.", "The patch agent adds tests before structural cleanup."),
    ("Patch Size Discipline", "Small patches are easier to review, revert, and explain.", "Diff size, touched modules, and changed public APIs become review signals.", "Large generated rewrites often hide mistakes.", "The system prefers narrow refactors and separate pull requests."),
    ("Prompt Injection in Repos", "Issues, comments, docs, and fixtures can contain instructions that should not control the agent.", "The system classifies repository text as data unless policy marks it trusted.", "A malicious comment could redirect tool use or leak assumptions.", "The agent separates developer policy from untrusted project content."),
    ("Dependency Drift", "Libraries change APIs, licenses, security posture, and transitive dependencies.", "Version diffs and advisory feeds show when maintenance is needed.", "Delayed upgrades become emergency migrations.", "The agent proposes staged upgrades with rollback notes."),
    ("Documentation Repair", "Documentation debt misleads developers even when code works.", "README commands, examples, and API docs are compared against tests and actual behavior.", "Stale docs cause failed onboarding and incorrect usage.", "The system patches docs with evidence from runnable commands."),
    ("Human Approval", "Self-healing should not mean self-merging.", "Approval records identify who accepted a change and why.", "Full autonomy removes accountability from risky edits.", "Agents prepare evidence while humans approve merge decisions."),
]

SPORT = [
    ("Live Match Data", "The algorithmic stadium collects tracking, fatigue, crowd movement, ticket scans, and broadcast attention.", "Each signal belongs to performance, safety, business, or fan-experience layers.", "Mixing layers can turn emotion into pure pricing data.", "The system separates analytical goals before making recommendations."),
    ("Fan Emotion", "Fans experience sport through hope, rivalry, memory, suspense and belonging.", "Sentiment, chants and viewing behavior are interpreted as cultural signals, not only engagement metrics.", "Personalization can fragment the shared match story.", "AI should support accessibility while preserving collective moments."),
    ("Coaching Judgment", "Agents can detect fatigue, pressing traps, and tactical imbalance.", "Model outputs are compared with match context, player confidence and tournament pressure.", "Statistics alone can misread human momentum.", "The coach receives evidence, not automatic authority."),
    ("Broadcast Storytelling", "A highlight is not always the statistically largest event.", "Crowd reaction, defensive recovery and symbolic substitutions can matter.", "Automated clips may flatten narrative drama.", "The system combines event data with story context."),
    ("Player Data Rights", "Tracking data affects contracts, selection and public reputation.", "Athletes need visibility into conclusions drawn from their bodies.", "Opaque analytics can create unfair career consequences.", "Governance must include challenge, correction and consent mechanisms."),
    ("Small Federation Access", "Wealthy teams can buy stronger analytics than small teams.", "Shared tools and standards can reduce unfair data gaps.", "Technology may widen competitive inequality.", "Leagues should define fair access rules for core analytics."),
    ("Stadium Operations", "AI can reduce queues, improve transport and support safety planning.", "Operational data must be judged by fan welfare, not only revenue.", "Optimization can become extraction if every delay becomes a sales opportunity.", "The system reports service quality alongside commercial outcomes."),
    ("Authenticity", "Sport depends on uncertainty and shared drama.", "Prediction should explain possibilities without pretending the match is solved.", "Overconfident analytics can drain suspense.", "AI should enrich interpretation while leaving room for surprise."),
]

DOMAIN_ASPECTS = {
    "food": [
        ("טקסי בישול משפחתיים", "סדר פעולות, חלוקת תפקידים וזמני חג", "מחיקת ההקשר החברתי של המנה", "לתעד מי משתתף בבישול ומה משמעות התפקיד שלו"),
        ("חומרי גלם מקומיים", "מקור רכיבים, עונתיות ושמות מקומיים", "החלפת רכיבים שמוחקת מקום וזיכרון", "לשמור שם מקורי לצד הסבר קולינרי"),
        ("זיכרון של טעם", "תיאורי מרקם, ריח וצבע בזמן הבישול", "הפיכת טעם לחישוב טכני בלבד", "לחבר בין מדידה לבין עדות חושית"),
        ("הגירה ושינוי מתכון", "תחליפים שנוצרו בעקבות מעבר מקום", "הצגת שינוי כטעות ולא כהסתגלות", "להציג גרסאות לפי מקום ותקופה"),
    ],
    "fashion": [
        ("כלכלת לבישה", "עלות ללבישה ותדירות שימוש", "הפיכת סטייל לצריכה מהירה", "להעדיף פריטים שחוזרים לשימוש"),
        ("גוף ונוחות", "מידה, תנועה, בד ואקלים", "המלצה יפה שאינה נוחה", "לשלב משוב לבישה ולא רק תמונה"),
        ("סמלים וזהות", "צבעים, צניעות, קהילה ואירוע", "מחיקת משמעות תרבותית", "לתת למשתמש להגדיר גבולות סגנון"),
        ("חיי הבגד", "תיקון, אחסון, כביסה ושימוש חוזר", "החלפת בגד במקום תחזוקה", "להציע תיקון לפני רכישה"),
    ],
    "code": [
        ("Legacy Knowledge", "old modules, ownership gaps, and undocumented behavior", "repairing code without understanding why it exists", "preserve historical intent before changing structure"),
        ("Reviewable Repair", "small diffs, tests, and clear risk notes", "large generated patches that reviewers cannot trust", "keep repairs narrow and evidence-driven"),
        ("Dependency Health", "version drift, advisories, and migration notes", "upgrades that break production behavior", "stage upgrades with tests and rollback paths"),
        ("Developer Trust", "explanations, reproducible failures, and approval records", "automation that feels opaque", "make every repair understandable to maintainers"),
    ],
    "sport": [
        ("Tournament Emotion", "rivalry, pressure, memory, and national identity", "reducing a match to prediction charts", "read analytics through the emotional stakes of the game"),
        ("Player Welfare", "fatigue, injury risk, and schedule load", "using tracking data only for performance extraction", "balance competitive insight with athlete protection"),
        ("Fan Experience", "chants, travel, queues, broadcast access, and shared attention", "turning supporters into pricing signals", "measure service quality alongside revenue"),
        ("Competitive Fairness", "analytics budgets, data access, and federation resources", "widening gaps between rich and small teams", "define shared standards for core sport data"),
    ],
    "hair": [
        ("Hair Texture Recognition", "curl pattern, density, porosity, and scalp sensitivity", "flattening diverse hair types into narrow beauty categories", "validate recommendations across textured, straight, dyed, and protective styles"),
        ("Virtual Try-On Trust", "face shape, lighting, hairline mapping, and color simulation", "promising a salon result that the user cannot realistically achieve", "label simulations as previews and include stylist review"),
        ("Beauty Standard Bias", "training data diversity, cultural styles, and age representation", "recommending only dominant or commercial looks", "audit hairstyle outputs by culture, texture, gender, and accessibility"),
        ("Salon Collaboration", "client preference, maintenance time, budget, and professional judgment", "replacing consultation with opaque automation", "use AI as a conversation aid rather than an authority"),
    ],
}
LENSES = {
    "food": ["הבית", "החג", "ההגירה", "הדור הצעיר", "שוק מקומי", "בית הספר", "ארכיון משפחתי", "מטבח משותף"],
    "fashion": ["היומיום", "הגוף", "הקהילה", "העונה", "תיקון", "תקציב", "אירוע חברתי", "קיימות"],
    "code": ["Maintainer Experience", "Release Practice", "Security Review", "Test Design", "Onboarding", "Incident Learning", "Architecture Drift", "Documentation"],
    "sport": ["Match Day", "Broadcast Narrative", "Training Load", "Supporter Culture", "Tournament Travel", "Youth Development", "Data Governance", "Stadium Safety"],
    "hair": ["Salon Consultation", "AR Mirror", "Curl Care", "Color Planning", "Identity Expression", "Trend Forecasting", "Scalp Health", "Digital Avatar"],
}
CONTEXTS = {"food": ["אובדן ידע", "שפה מקומית", "הסכמה", "טעם", "תיעוד", "חינוך", "עונתיות", "קהילה", "מורשת"], "fashion": ["זהות", "פרטיות", "מחיר", "נוחות", "מחזור חיים", "מלאכה", "ייצוג", "שימוש חוזר", "אקלים"], "code": ["Ownership", "Regression Safety", "API Stability", "Threat Modeling", "Release Notes", "Incident Recovery", "Review Load", "Knowledge Transfer", "Maintainability"], "sport": ["Public Trust", "Player Rights", "Crowd Memory", "Competitive Balance", "Media Pressure", "Travel Equity", "Youth Pathways", "Safety Planning", "Shared Drama"], "hair": ["Texture Justice", "Self-Image", "Cultural Meaning", "Salon Safety", "Maintenance Cost", "Representation", "Color Risk", "Consent", "Accessibility"]}
CASES = {"food": ["מחברת מוכתמת", "שולחן רמדאן", "מתכון חתונה", "מטבח מהגרים", "שוק שבת", "סדנת תלמידים", "ארוחת זיכרון", "צנצנת תבלינים", "בישול שכונתי", "שיחת סבתא", "מנה שנשכחה"], "fashion": ["מעיל שעבר בירושה", "שמלת חג", "ארון קפסולה", "חנות יד שנייה", "תיקון מכפלת", "מדידת אונליין", "בגד עבודה", "צעיף מסורתי", "יומן לבישה", "חלון ראווה", "בד ממוחזר"], "code": ["legacy payment module", "flaky test suite", "security hotfix", "dependency migration", "API deprecation", "onboarding sprint", "incident review", "documentation drift", "release freeze", "monorepo boundary", "ownership handoff"], "sport": ["World Cup qualifier", "late penalty", "fan zone queue", "youth academy", "injury return", "broadcast replay", "small federation", "derby atmosphere", "stadium evacuation", "travel schedule", "underdog campaign"], "hair": ["protective braids", "curly cut consult", "silver hair transition", "virtual bangs preview", "hijab-friendly salon", "teen identity shift", "color allergy check", "avatar hairstyle", "wedding updo", "barbershop fade", "postpartum hair loss"]}
SECTION_BANKS = {"food": FOOD, "fashion": FASHION, "code": CODE, "sport": SPORT, "hair": []}
