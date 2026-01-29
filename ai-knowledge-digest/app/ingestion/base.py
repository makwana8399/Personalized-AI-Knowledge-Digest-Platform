
from abc import ABC, abstractmethod
from typing import List, Dict, Optional
from datetime import datetime


class Article:
    def __init__(
        self,
        title: str,
        url: str,
        content: str,
        published_at: Optional[datetime] = None,
        source: Optional[str] = None,
    ):
        self.title = title
        self.url = url
        self.content = content
        self.published_at = published_at or datetime.utcnow()
        self.source = source


class BaseScraper(ABC):
    """Base class for all scrapers"""

    def __init__(self):
        self.articles: List[Article] = []

    @abstractmethod
    def scrape(self) -> List[Article]:
        """Scrape content and return list of articles"""
        raise NotImplementedError

    def deduplicate(self, existing_urls: set) -> List[Article]:
        """Filter out articles that already exist"""
        return [a for a in self.articles if a.url not in existing_urls]