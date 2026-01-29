import feedparser
from datetime import datetime
from app.config.logging import logger


class NewsletterScraper:
    """
    Scrapes RSS-based newsletters.
    Each item is converted into a raw article.
    AI summarization happens later.
    """

    SOURCE_NAME = "Newsletter"  

    FEEDS = [
        {
            "publisher": "The Pragmatic Engineer",
            "url": "https://newsletter.pragmaticengineer.com/feed",
            "topic_hint": "product",
        },
        {
            "publisher": "The Batch (Andrew Ng)",
            "url": "https://www.deeplearning.ai/the-batch/feed/",
            "topic_hint": "ai",
        },
        {
            "publisher": "TLDR AI",
            "url": "https://tldr.tech/ai/rss",
            "topic_hint": "ai",
        },
        {
            "publisher": "Import AI",
            "url": "https://jack-clark.net/feed/",
            "topic_hint": "ai",
        },
    ]

    def scrape(self):
        articles = []

        for feed in self.FEEDS:
            try:
                parsed = feedparser.parse(feed["url"])

                for entry in parsed.entries[:5]:
                    content = ""

                    if hasattr(entry, "content") and entry.content:
                        content = entry.content[0].value
                    else:
                        content = entry.get("summary", "")

                    articles.append(
                        {
                            "title": entry.get("title", "No title"),
                            "url": entry.get("link"),
                            "content": content,
                            "published_at": datetime.utcnow(), 
                            "source": self.SOURCE_NAME,         
                            "publisher": feed["publisher"],    
                            "topic_hint": feed["topic_hint"],
                        }
                    )

            except Exception as e:
                logger.warning(
                    f"Newsletter error ({feed['publisher']}): {e}"
                )

        logger.info(f"Scraped {len(articles)} articles from newsletters")
        return articles