from book_generator.localized_titles import localized_title


def template_values(options):
    title = localized_title(options.topic, options.output_language)
    return {
        "<<DOCUMENT_CLASS_LINE>>": options.class_line,
        "<<ARTICLE_TITLE>>": title,
        "<<ARTICLE_SUBTITLE>>": options.subtitle,
        "<<COVER_AUTHORS>>": options.cover_authors,
        "<<COVER_COURSE>>": options.cover_course,
        "<<COVER_ASSIGNMENT>>": options.cover_assignment,
        "<<COVER_LECTURER>>": options.cover_lecturer,
        "<<COVER_UNIVERSITY>>": options.cover_university,
        "<<COVER_DATE>>": options.cover_date,
        "<<MAIN_LANGUAGE>>": options.main_language,
        "<<OTHER_LANGUAGE>>": options.other_language,
        "<<CONTENTS_NAME>>": options.contents_name,
        "<<ABSTRACT_TITLE>>": options.abstract_title,
        "<<ABSTRACT_TEXT>>": options.abstract_text,
        "<<KEYWORDS_LABEL>>": options.keywords_label,
        "<<KEYWORDS>>": options.keywords,
        "<<TOC_LEVEL>>": options.toc_level,
        "<<HEADER_LEFT>>": title[:46],
        "<<HEADER_RIGHT>>": options.header_right,
        "<<TOC_BLOCK>>": options.toc_block,
    }


def write_latex_project(chapter_path, main_path, template_path, options, article):
    chapter_path.write_text(article + "\n", encoding="utf-8")
    template = template_path.read_text(encoding="utf-8")
    for key, value in template_values(options).items():
        template = template.replace(key, value)
    main_path.write_text(template, encoding="utf-8")
