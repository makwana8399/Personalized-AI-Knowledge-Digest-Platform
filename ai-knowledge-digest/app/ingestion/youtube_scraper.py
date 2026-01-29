from datetime import datetime
import feedparser
from youtube_transcript_api import YouTubeTranscriptApi
from app.config.logging import logger


class YouTubeScraper:
    """
    Scrapes recent YouTube videos by channel ID.
    Pulls transcripts when available.
    """

    SOURCE_NAME = "YouTube"  

    CHANNELS = [
        {
            "channel_name": "Fireship",
            "channel_id": "UCsBjURrPoezykLs9EqgamOA",
            "topic_hint": "dev",
        },
        {
            "channel_name": "Two Minute Papers",
            "channel_id": "UCbfYPyITQ-7l4upoX8nvctg",
            "topic_hint": "ai",
        },
        {
            "channel_name": "AI Explained",
            "channel_id": "UCNJ1Ymd5yFuUPfJ3i6rA5Qw",
            "topic_hint": "ai",
        },
        {
            "channel_name": "Lex Clips",
            "channel_id": "UCs1bZ6n6Rz9YxN4rU8nJZ5Q",
            "topic_hint": "ai",
        },
    ]

    MAX_VIDEOS = 3

    def scrape(self):
        articles = []

        for channel in self.CHANNELS:
            try:
                feed_url = (
                    "https://www.youtube.com/feeds/videos.xml"
                    f"?channel_id={channel['channel_id']}"
                )

                feed = feedparser.parse(feed_url)

                for entry in feed.entries[: self.MAX_VIDEOS]:
                    video_id = entry.get("yt_videoid")

                    text = ""
                    try:
                        if video_id:
                            transcript = YouTubeTranscriptApi.get_transcript(video_id)
                            text = " ".join(chunk["text"] for chunk in transcript)
                    except Exception:
                        text = entry.get("summary", "")

                    articles.append(
                        {
                            "title": entry.get("title", "No title"),
                            "url": entry.get("link"),
                            "content": text,
                            "published_at": datetime.utcnow(), 
                            "source": self.SOURCE_NAME,      
                            "channel_name": channel["channel_name"],
                            "topic_hint": channel["topic_hint"],
                        }
                    )

            except Exception as e:
                logger.warning(
                    f"YouTube channel error ({channel['channel_name']}): {e}"
                )

        logger.info(f"Scraped {len(articles)} articles from YouTube")
        return articles