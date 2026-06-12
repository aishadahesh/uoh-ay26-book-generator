from book_generator.document_options import bidi_section

TOPICS = [
    ("מטבחי זיכרון: כיצד AI יכול לשמר מתכונים משפחתיים לפני שהם נעלמים", "article", "hebrew", "food"),
    ("Self-Healing Software Repositories: Can AI Agents Detect, Explain, and Repair Technical Debt?", "article", "english", "code"),
    ("ארון הבגדים האלגוריתמי: אופנה, זהות וקיימות בעידן סוכני AI", "book", "hebrew", "fashion"),
    ("The Algorithmic Stadium: AI Agents, Fan Emotion, and the Future of Global Sport", "book", "english", "sport"),
]


def base_body(options, domain):
    return HEBREW_BASE[domain](options.topic) if options.output_language == "hebrew" else ENGLISH_BASE[domain](options.topic)


def food_base(topic):
    return rf"""\section{{מבוא: מתכון כזיכרון משפחתי}}
המאמר {topic} בוחן מתכונים כיחידות ידע תרבותיות: הם שומרים טעם, הגירה, שפה, יחסי משפחה, מחסור, חגיגות וטכניקות שאינן תמיד כתובות. כאשר סבתא אומרת "עד שהבצק מרגיש נכון", היא מעבירה ידע גופני ולא רק הוראה. לכן סוכן AI לשימור מתכונים צריך להקשיב לסיפור, לא רק לחלץ רשימת רכיבים.
\section{{מה AI צריך לשמר}}
המערכת צריכה לתעד גרסאות, הערות שוליים, תחליפים, זמני חג, כלי מטבח, ומי לימד את מי. מאגר קולינרי איכותי יכלול אודיו, תמונה, תמלול, OCR של מחברות, תיוג רכיבים, וקישור בין מתכון לסיפור משפחתי.
\begin{{figure}}[h]\centering\includegraphics[width=0.72\textwidth]{{assets/agent_runtime_architecture.png}}\caption{{צוות סוכנים לשימור ידע קולינרי}}\end{{figure}}
\section{{טבלת שימור}}
\begin{{table}}[h]\centering\small\begin{{tabular}}{{>{{\raggedleft\arraybackslash}}p{{0.38\textwidth}}>{{\raggedleft\arraybackslash}}p{{0.36\textwidth}}>{{\raggedleft\arraybackslash}}p{{0.18\textwidth}}}}\toprule\textbf{{ערך תרבותי}}&\textbf{{נתון לשימור}}&\textbf{{שכבה}}\\\midrule זיכרון בין-דורי&סיפור, קול, תמונה, אירוע משפחתי&משפחה\\ דיוק בישול&כמויות, מרקם, טמפרטורה, זמן&טכניקה\\ הקשר קהילתי&חג, מקום, שפה, שינויי הגירה&תרבות\\\bottomrule\end{{tabular}}\caption{{שכבות ידע במתכון משפחתי}}\end{{table}}
\section{{נוסחת איכות}}
\[Q_{{recipe}}=0.30M+0.25T+0.25C+0.20A\]
כאשר \(M\) הוא זיכרון, \(T\) הוא דיוק טכני, \(C\) הוא הקשר תרבותי, ו-\(A\) הוא נגישות. {bidi_section("hebrew")}"""


def fashion_base(topic):
    return rf"""\section{{מבוא: הארון כמאגר זהות}}
הספר {topic} מציג את ארון הבגדים כמערכת נתונים חיה. כל פריט נושא זיכרון, גוף, עונה, מעמד, מגדר, תקציב ורצון להשתייך או להתבדל. סוכן AI בתחום האופנה אינו רק ממליץ מה ללבוש; הוא משפיע על דימוי עצמי ועל דפוסי צריכה.
\section{{בין סטייל לקיימות}}
אופנה אלגוריתמית יכולה להפחית קניות שגויות, להציע שילובים מתוך בגדים קיימים, ולחשב עלות סביבתית. באותה עת היא עלולה להגביר רכישות דרך המלצות תכופות. לכן השאלה אינה האם AI "מבין אופנה", אלא האם הוא מתוכנן לעודד בחירה אחראית.
\begin{{figure}}[h]\centering\includegraphics[width=0.72\textwidth]{{assets/agent_runtime_architecture.png}}\caption{{מערכת סוכנים לארון בגדים אלגוריתמי}}\end{{figure}}
\section{{טבלת החלטות}}
\begin{{table}}[h]\centering\small\begin{{tabular}}{{>{{\raggedleft\arraybackslash}}p{{0.38\textwidth}}>{{\raggedleft\arraybackslash}}p{{0.36\textwidth}}>{{\raggedleft\arraybackslash}}p{{0.18\textwidth}}}}\toprule\textbf{{השפעה}}&\textbf{{מה נמדד}}&\textbf{{ממד}}\\\midrule פחות בזבוז&שימוש חוזר, תיקונים, התאמה לארון קיים&קיימות\\ ביטוי אישי&צבע, גזרה, הקשר חברתי, נוחות&זהות\\ סיכון מסחרי&דחיפת טרנדים, קנייה אימפולסיבית&צריכה\\\bottomrule\end{{tabular}}\caption{{מדדי אופנה אלגוריתמית}}\end{{table}}
\section{{מודל השפעה}}
\[S=0.30I+0.30U+0.25E-0.15B\]
כאשר \(I\) הוא זהות, \(U\) שימושיות, \(E\) קיימות, ו-\(B\) הטיית צריכה. {bidi_section("hebrew")}"""


def code_base(topic):
    return rf"""\section{{Introduction: Technical Debt as Repository Memory}}
{topic} treats a software repository as a living memory of design choices. Technical debt is not only ugly code; it is the accumulated cost of shortcuts, missing tests, unclear ownership, brittle architecture, and documentation that no longer matches behavior.
\section{{Agentic Maintenance Loop}}
A self-healing repository needs several agents: a scanner that detects risk, a reasoning agent that explains impact, a patch agent that proposes small changes, and a reviewer that runs tests before approval. The goal is not autonomous chaos, but a disciplined maintenance workflow.
\begin{{figure}}[h]\centering\includegraphics[width=0.72\textwidth]{{assets/agent_runtime_architecture.png}}\caption{{Agent workflow for repository repair}}\end{{figure}}
\section{{Debt Evaluation Table}}
\begin{{table}}[h]\centering\small\begin{{tabular}}{{p{{0.20\textwidth}}p{{0.34\textwidth}}p{{0.36\textwidth}}}}\toprule\textbf{{Layer}}&\textbf{{Evidence}}&\textbf{{Repair Action}}\\\midrule Code smell&duplication, long methods, fragile branches&refactor with tests\\ Architecture&cycles, hidden coupling, unclear modules&split boundaries\\ Process&missing CI, weak review, stale docs&add gates and ownership\\\bottomrule\end{{tabular}}\caption{{Technical debt layers and agent actions}}\end{{table}}
\section{{Risk Model}}
\[R=0.35D+0.25C+0.20F+0.20H\]
Here \(D\) is debt severity, \(C\) coupling, \(F\) failure history, and \(H\) human review cost. {bidi_section("english")}"""


def sport_base(topic):
    return rf"""\section{{Introduction: The Stadium as a Data Arena}}
{topic} studies the stadium as a social and computational system. AI agents now shape ticketing, scouting, broadcast highlights, tactical analysis, fan sentiment, safety operations, and live storytelling. Sport becomes a field where emotion and analytics meet.
\section{{Fan Emotion and Algorithmic Mediation}}
The key issue is not only whether AI predicts performance. It is whether AI changes how fans feel suspense, loyalty, disappointment, and belonging. Personalized feeds can deepen attachment, but they can also fragment the shared public experience of watching a match together.
\begin{{figure}}[h]\centering\includegraphics[width=0.72\textwidth]{{assets/agent_runtime_architecture.png}}\caption{{Agent system inside the algorithmic stadium}}\end{{figure}}
\section{{Stadium Evaluation Table}}
\begin{{table}}[h]\centering\small\begin{{tabular}}{{p{{0.20\textwidth}}p{{0.34\textwidth}}p{{0.36\textwidth}}}}\toprule\textbf{{Layer}}&\textbf{{Signals}}&\textbf{{AI Use}}\\\midrule Performance&tracking, fatigue, tactics&coaching insight\\ Fan emotion&chants, posts, attention, movement&experience design\\ Operations&queues, safety, transport, pricing&stadium management\\\bottomrule\end{{tabular}}\caption{{AI layers in global sport}}\end{{table}}
\section{{Engagement Model}}
\[F=0.30P+0.25E+0.25S+0.20T\]
Here \(P\) is performance quality, \(E\) emotional resonance, \(S\) shared identity, and \(T\) technological support. {bidi_section("english")}"""


HEBREW_BASE = {"food": food_base, "fashion": fashion_base}
ENGLISH_BASE = {"code": code_base, "sport": sport_base}
