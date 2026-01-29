from datetime import datetime, timedelta
import uuid

from app.database.models import Digest, User, Article
from app.config.logging import logger
from app.ranking.ranker import ArticleRanker


# --------------------------------------------------
# CANONICAL TOPICS (SINGLE SOURCE OF TRUTH)
# --------------------------------------------------
CANONICAL_TOPICS = {
    "ai": ["ai", "artificial intelligence", "llm", "llms", "chatgpt"],
    "mlops": ["mlops", "devops", "cloud", "infrastructure"],
    "startup": ["startup", "startups", "business", "founder", "saas"],
    "product": ["product", "pm", "ux", "design"],
    "vc": ["vc", "investment", "funding"],
    "general": [],
}


# --------------------------------------------------
# NORMALIZE AI TOPIC → CANONICAL
# --------------------------------------------------
def normalize_topic(raw_topic: str) -> str:
    if not raw_topic:
        return "general"

    raw = raw_topic.lower()

    for canonical, variants in CANONICAL_TOPICS.items():
        if raw == canonical or raw in variants:
            return canonical

    return "general"


# --------------------------------------------------
# EXPAND USER INTERESTS
# --------------------------------------------------
def expand_interests(interests: list[str]) -> set[str]:
    expanded = set()

    for interest in interests or []:
        key = interest.lower()
        expanded.add(key)

        for canonical, variants in CANONICAL_TOPICS.items():
            if key == canonical or key in variants:
                expanded.add(canonical)
                expanded.update(variants)

    return expanded


# --------------------------------------------------
# DIGEST GENERATOR
# --------------------------------------------------
class Generator:
    def __init__(self, db, processor):
        self.db = db
        self.processor = processor
        self.ranker = ArticleRanker()

    # --------------------------------------------------
    # MAIN ENTRY
    # --------------------------------------------------
    def generate_for_all_users(self, db) -> int:
        users = db.query(User).all()

        if not users:
            logger.warning("No users found. Skipping digest generation.")
            return 0

        today = datetime.utcnow().date()
        since = datetime.utcnow() - timedelta(days=7)

        digest_count = 0

        for user in users:
            logger.info(f"Generating digest for {user.email}")

            # --------------------------------------------------
            # 1️⃣ IDEMPOTENCY CHECK
            # --------------------------------------------------
            exists = (
                db.query(Digest)
                .filter(
                    Digest.user_id == user.id,
                    Digest.generated_date == today,
                )
                .first()
            )

            if exists:
                logger.info(f"Digest already exists for {user.email}, skipping")
                continue

            # --------------------------------------------------
            # 2️⃣ USER INTERESTS
            # --------------------------------------------------
            allowed_topics = expand_interests(user.interests or [])

            # --------------------------------------------------
            # 3️⃣ FETCH ARTICLES
            # --------------------------------------------------
            all_articles = (
                db.query(Article)
                .filter(Article.published_at >= since)
                .all()
            )

            if not all_articles:
                logger.warning("No articles found for digest generation")
                continue

            # --------------------------------------------------
            # 4️⃣ AI SUMMARIZE + TOPIC TAG (SAFE)
            # --------------------------------------------------
            for article in all_articles:
                if article.summary and article.topic:
                    continue

                try:
                    ai = self.processor.summarize_article(
                        article.content_md or ""
                    )

                    article.summary = ai.get("summary", "")
                    article.takeaways = ai.get("takeaways", [])
                    article.topic = normalize_topic(ai.get("topic"))

                    db.add(article)

                except Exception as e:
                    logger.error(
                        f"AI processing failed for article {article.id}: {e}"
                    )

            db.commit()

            # --------------------------------------------------
            # 5️⃣ SOFT INTEREST FILTER (NO HARD STOP)
            # --------------------------------------------------
            filtered_articles = [
                a for a in all_articles
                if a.topic in allowed_topics
            ]

            if not filtered_articles:
                logger.warning(
                    f"No interest-matched articles for {user.email}. Using fallback."
                )
                filtered_articles = all_articles[:10]

            # --------------------------------------------------
            # 6️⃣ RANK ARTICLES
            # --------------------------------------------------
            ranked = self.ranker.rank(filtered_articles, user)
            top_articles = ranked[:5]

            if not top_articles:
                logger.warning(
                    f"No ranked articles for {user.email}, skipping digest"
                )
                continue

            # --------------------------------------------------
            # 7️⃣ GENERATE OVERVIEW
            # --------------------------------------------------
            try:
                overview = self.processor.generate_overview(
                    top_articles,
                    user.interests or [],
                )
            except Exception as e:
                logger.error(
                    f"Overview generation failed for {user.email}: {e}"
                )
                overview = "Your AI knowledge digest for today."

            # --------------------------------------------------
            # 8️⃣ SAVE DIGEST
            # --------------------------------------------------
            digest = Digest(
                id=uuid.uuid4(),
                user_id=user.id,
                generated_date=today,
                overview=overview,
                article_ids=[a.id for a in top_articles],
            )

            db.add(digest)
            db.commit()

            logger.info(
                f"Generated digest for {user.email} with {len(top_articles)} articles"
            )

            digest_count += 1

        return digest_count