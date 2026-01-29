import schedule
import time
from datetime import datetime

from app.config.settings import DIGEST_GENERATION_TIME
from app.config.logging import logger
from app.database.db import SessionLocal

from app.ingestion.blog_scraper import BlogScraper
from app.ingestion.youtube_scraper import YouTubeScraper
from app.ingestion.newsletter_scraper import NewsletterScraper
from app.ingestion.persist import save_articles

from app.ai.processor import Processor
from app.digest.generator import Generator
from app.email.sender import EmailSender
from app.digest.templates import Templates


class Cron:
    """Daily job orchestration"""

    def __init__(self):
        self.db = SessionLocal()
        self.processor = Processor()
        self.generator = Generator(self.db, self.processor)
        self.email_sender = EmailSender()

    # --------------------------------------------------
    # Scheduling
    # --------------------------------------------------
    def schedule_jobs(self):
        hour, minute = map(int, DIGEST_GENERATION_TIME.split(":"))
        time_str = f"{hour:02d}:{minute:02d}"

        schedule.every().day.at(time_str).do(self.daily_job)
        logger.info(f"Jobs scheduled for {time_str} daily")

    # --------------------------------------------------
    # Main Daily Job
    # --------------------------------------------------
    def daily_job(self):
        try:
            logger.info("Starting daily digest generation job...")

            # Step 1: Scrape + persist
            logger.info("Step 1: Scraping content from sources...")
            self._scrape_and_store_sources()

            # Step 2: Generate digests
            logger.info("Step 2: Generating digests...")
            digest_count = self.generator.generate_for_all_users(self.db)
            logger.info(f"Generated {digest_count} digests")

            # Step 3: Send emails
            logger.info("Step 3: Sending digest emails...")
            email_count = self._send_digest_emails()
            logger.info(f"Sent {email_count} digest emails")

            logger.info("Daily job completed successfully")

        except Exception as e:
            logger.error(f"Error in daily job: {str(e)}")

    # --------------------------------------------------
    # Scrape + Persist
    # --------------------------------------------------
    def _scrape_and_store_sources(self):
        try:
            blog_articles = BlogScraper().scrape()
            saved = save_articles(self.db, blog_articles, "Blog")
            logger.info(f"Saved {saved} blog articles")
        except Exception as e:
            logger.error(f"Error scraping blogs: {str(e)}")

        try:
            yt_articles = YouTubeScraper().scrape()
            saved = save_articles(self.db, yt_articles, "YouTube")
            logger.info(f"Saved {saved} YouTube articles")
        except Exception as e:
            logger.error(f"Error scraping YouTube: {str(e)}")

        try:
            nl_articles = NewsletterScraper().scrape()
            saved = save_articles(self.db, nl_articles, "Newsletter")
            logger.info(f"Saved {saved} newsletter articles")
        except Exception as e:
            logger.error(f"Error scraping newsletters: {str(e)}")

    # --------------------------------------------------
    # Email Sending  ✅ FIXED
    # --------------------------------------------------
    def _send_digest_emails(self) -> int:
        from app.database.models import Digest, Article

        today = datetime.utcnow().date()

        digests = (
            self.db.query(Digest)
            .filter(
                Digest.generated_date == today,
                Digest.email_sent == False
            )
            .all()
        )

        sent_count = 0

        for digest in digests:
            try:
                articles = (
                    self.db.query(Article)
                    .filter(Article.id.in_(digest.article_ids))
                    .all()
                )

                articles_data = [
                    {
                        "title": a.title,
                        "url": a.url,
                        "summary": a.summary or "",
                        "topic": a.topic or "General",
                        "takeaways": a.takeaways or [],
                    }
                    for a in articles
                ]

                html_body = Templates.get_email_template(
                    digest.overview,
                    articles_data,
                )

                # 🔥 SEND EMAIL (no if-condition bullshit)
                self.email_sender.send_email(
                    recipient=digest.user.email,
                    subject="Your Daily AI Digest 🚀",
                    body=html_body,
                )

                digest.email_sent = True
                self.db.commit()
                sent_count += 1

            except Exception as e:
                logger.error(f"Error sending digest email: {str(e)}")

        return sent_count

    # --------------------------------------------------
    # Scheduler Runner
    # --------------------------------------------------
    def run_scheduler(self):
        self.schedule_jobs()

        logger.info("DEV MODE: Running daily job immediately")
        self.daily_job()

        logger.info("Scheduler is running. Press Ctrl+C to stop.")

        try:
            while True:
                schedule.run_pending()
                time.sleep(60)
        except KeyboardInterrupt:
            logger.info("Scheduler stopped by user")
        finally:
            self.db.close()