from datetime import datetime
from app.database.models import Article, Source
from app.config.logging import logger
from app.ai.processor import Processor


def save_articles(db, articles: list, source_name: str) -> int:
    """Save articles to DB with deduplication and AI enrichment"""

    source = db.query(Source).filter(Source.name == source_name).first()
    if not source:
        logger.warning(f"Source not found: {source_name}")
        return 0

    processor = Processor()
    saved = 0

    for item in articles:
        if not item.get("url"):
            continue

        # Deduplication
        exists = db.query(Article).filter(Article.url == item["url"]).first()
        if exists:
            continue

        content = item.get("content", "")

        # -------------------------
        # AI PROCESSING (SAFE)
        # -------------------------
        try:
            ai_data = processor.process_article(content)
        except Exception as e:
            logger.error(f"AI processing failed: {e}")
            ai_data = {
                "summary": "",
                "takeaways": [],
                "topic": "General",
            }

        # -------------------------
        # Save article
        # -------------------------
        article = Article(
            title=item.get("title", "No title"),
            url=item["url"],
            content_md=content,
            summary=ai_data.get("summary"),
            takeaways=ai_data.get("takeaways", []),
            topic=ai_data.get("topic", "General"),
            published_at=item.get("published_at") or datetime.utcnow(),
            source_id=source.id,
            created_at=datetime.utcnow(),
        )

        db.add(article)
        saved += 1

    db.commit()
    return saved