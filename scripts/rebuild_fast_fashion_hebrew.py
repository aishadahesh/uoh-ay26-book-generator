from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from book_generator.document_options import DocumentOptions, bidi_section
from book_generator.latex_project import write_latex_project
from book_generator.latex_sanitizer import sanitize_latex_body
from book_generator.page_count import read_pdf_pages
from book_generator.page_expander import expansion_count, expansion_pages
from book_generator.pdf_outputs import copy_named_outputs

TOPIC = "The Algorithmic Closet: Can AI Agents Make Fast Fashion Slower, Smarter, and More Ethical?"
CHAPTER = ROOT / "latex" / "chapters" / "online_article.tex"
MAIN = ROOT / "latex" / "main.tex"
TEMPLATE = ROOT / "latex" / "main_template.tex"
PDF = ROOT / "output" / "agentic_ai_production_2026.pdf"


def base_body() -> str:
    sections = [
        ("מבוא: אופנה מהירה כבעיה מערכתית", "אופנה מהירה מבוססת על מחזורי עיצוב קצרים, ייצור זול, שיווק אגרסיבי ותחושת דחיפות מתמדת. סוכני בינה מלאכותית יכולים להאט את המנגנון הזה רק אם הם מתוכננים להפחית עודפים, להאריך חיי בגד ולחשוף את המחיר הסביבתי והחברתי של כל החלטת רכישה."),
        ("חיזוי ביקוש בלי ייצור יתר", "מודלי חיזוי יכולים לנתח מכירות, מזג אוויר, חיפושים, החזרות ומגמות רשת, אך המטרה אינה לייצר מהר יותר אלא לייצר פחות טעויות. כאשר התחזית מחוברת למגבלות מלאי, ייצור מקומי ומדדי פסולת, היא יכולה להפחית בגדים שלא יימכרו."),
        ("שרשרת אספקה שקופה", "סוכן אחראי צריך לקשר כל פריט לחומר הגלם, למפעל, לשכר העבודה, לטביעת הפחמן ולתנאי ההובלה. שקיפות כזו מאפשרת לצרכן להבין אם מחיר נמוך נובע מיעילות אמיתית או מהעברת עלויות לעובדים ולסביבה."),
        ("הארון הקיים לפני קנייה", "המלצה אתית מתחילה בפריטים שכבר נמצאים בארון. במקום להציע רכישה מיידית, המערכת יכולה להציע שילוב מחדש, תיקון, השאלה, מכירה מחדש או התאמה עונתית של בגד קיים."),
        ("טבלת הערכה", r"\begin{table}[!h]\centering\small\caption{מסגרת RTL להערכת אופנה מהירה}\begin{tabular}{|p{0.25\textwidth}|p{0.33\textwidth}|p{0.28\textwidth}|}\hline מדד & מה נבדק & משמעות \\ \hline קיימות & מים, פליטות, פסולת טקסטיל & האם הבגד מפחית נזק סביבתי \\ \hline אתיקה & שכר, בטיחות, שקיפות מפעלים & האם הייצור מכבד עובדים \\ \hline שימושיות & מספר לבישות, תיקון, התאמה לארון & האם הפריט ישרוד מעבר לטרנד \\ \hline\end{tabular}\end{table}"),
        ("מדד מתמטי פשוט", r"ניתן להגדיר ציון אחריות כך: \[R=0.30S+0.25E+0.25U+0.20T\] כאשר \(S\) מייצג קיימות, \(E\) אתיקה, \(U\) שימושיות לאורך זמן, ו-\(T\) שקיפות."),
        ("הטיות וירוק מדומה", "מערכות המלצה עלולות להציג מוצר כירוק גם כאשר הנתונים חלקיים. לכן נדרש מנגנון ביקורת שמבדיל בין טענה שיווקית לבין ראיה ניתנת לבדיקה, ומסמן אי-ודאות במקום להסתיר אותה."),
        ("תפקיד הצרכן", "הצרכן אינו רק נקודת מכירה אלא שותף במעגל החיים של הבגד. כאשר המערכת מציגה עלות ללבישה, אפשרויות תיקון ומידע על מקור החומר, היא משנה את השאלה ממה לקנות עכשיו לכמה זמן הבגד ישרת אותי."),
        ("סיכום", "סוכני בינה מלאכותית לא יפתרו לבדם את משבר האופנה המהירה, אך הם יכולים להפוך את המערכת למדידה, שקופה ואיטית יותר. הערך האמיתי שלהם אינו במהירות ההמלצה אלא ביכולת לעצור רכישה לא נחוצה ולתמוך בבחירה אחראית."),
    ]
    body = "\n\n".join(f"\\section{{{title}}}\n{text}" for title, text in sections)
    body += "\n\n\\begin{figure}[!h]\\centering\\includegraphics[width=0.72\\textwidth]{assets/agent_runtime_architecture.png}\\caption{זרימת סוכנים להערכת אופנה מהירה}\\end{figure}"
    return sanitize_latex_body(body) + "\n\n" + bidi_section("hebrew")


def main() -> int:
    options = DocumentOptions(TOPIC, "book", "hebrew")
    article = base_body()
    added = 0
    for _ in range(8):
        write_latex_project(CHAPTER, MAIN, TEMPLATE, options, article)
        code = subprocess.call([sys.executable, str(ROOT / "scripts" / "build.py")], cwd=ROOT)
        pages = read_pdf_pages(ROOT / "latex" / "main.log")
        print(f"pages={pages}")
        if code != 0 or pages > 15:
            return code or 7
        if pages == 15:
            for target in copy_named_outputs(PDF, TOPIC, "book", "hebrew"):
                print(f"saved {target}")
            return 0
        missing = 15 - pages
        article += "\n\n" + expansion_pages(options, missing, added)
        added += expansion_count(missing)
    return 5


if __name__ == "__main__":
    raise SystemExit(main())
