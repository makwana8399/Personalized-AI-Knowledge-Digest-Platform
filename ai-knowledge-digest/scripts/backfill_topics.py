from app.database.db import SessionLocal
from app.database.models import Article
from app.config.logging import logger


def normalize_topic(raw_topic: str) -> str:
    if not raw_topic:
        return "general"

    raw = raw_topic.lower()

    if raw in ["llm", "ai", "artificial intelligence", "chatgpt"]:
        return "llms"
    if raw in ["mlops", "devops", "cloud", "infrastructure"]:
        return "mlops"
    if raw in ["startup", "business", "founder", "saas"]:
        return "startups"
    if raw in ["vc", "investment", "funding"]:
        return "vc"
    if raw in ["product", "pm", "ux", "design"]:
        return "product"

    return "general"


def main():
    db = SessionLocal()

    articles = db.query(Article).all()
    updated = 0

    for article in articles:
        old = article.topic
        new = normalize_topic(article.topic)

        if old != new:
            article.topic = new
            db.add(article)
            updated += 1

    db.commit()
    db.close()

    logger.info(f"Backfilled topics for {updated} articles")


if __name__ == "__main__":
    main()