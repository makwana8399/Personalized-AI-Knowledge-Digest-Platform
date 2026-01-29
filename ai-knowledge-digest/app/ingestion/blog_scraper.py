import feedparser
from datetime import datetime
from app.config.logging import logger


class BlogScraper:
    """Scrape blog articles from RSS feeds"""

    FEED_URLS = [
        "https://www.theverge.com/rss/index.xml",
        "https://news.ycombinator.com/rss",
        "https://feeds.arstechnica.com/arstechnica/index",
    ]

    SOURCE_NAME = "Blog"  

    def scrape(self) -> list:
        articles = []

        for feed_url in self.FEED_URLS:
            try:
                feed = feedparser.parse(feed_url)

                for entry in feed.entries[:10]:
                    articles.append(
                        {
                            "title": entry.get("title", "No title"),
                            "url": entry.get("link"),
                            "content": entry.get("summary", ""),
                            "published_at": datetime.utcnow(),
                            "source": self.SOURCE_NAME,  
                        }
                    )

                logger.info(
                    f"Scraped {len(feed.entries[:10])} articles from {feed_url}"
                )

            except Exception as e:
                logger.error(f"Error scraping {feed_url}: {str(e)}")

        return articles
