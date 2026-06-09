from book_generator import BookConfig, BookPipeline


def test_pipeline_generates_required_chapters():
    manuscript = BookPipeline(BookConfig()).run()
    assert manuscript.title
    assert len(manuscript.chapters) >= 3
    assert any("CrewAI" in chapter.body for chapter in manuscript.chapters)
    assert manuscript.qa_notes
