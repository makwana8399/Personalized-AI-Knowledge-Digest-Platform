
from app.database.models import Article, User
from app.config.logging import logger


class ArticleRanker:
    def rank(self, articles: list[Article], user: User) -> list[Article]:
        ranked = []

        for article in articles:
            score = 0
            text = f"{article.title or ''} {article.content_md or ''}".lower()

            for interest in user.interests:
                if interest.lower() in text:
                    score += 1

            ranked.append((score, article))

        ranked.sort(key=lambda x: x[0], reverse=True)

        logger.info(f"Ranked {len(ranked)} articles for user {user.email}")

        return [article for _, article in ranked]