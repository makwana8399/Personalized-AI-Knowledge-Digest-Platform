
import sys
import os
from app.config.logging import logger
from app.scheduler.cron import Cron
from app.database.db import engine
from app.database.models import Base


def init_database():
    """Initialize database tables"""
    try:
        logger.info("Initializing database...")
        Base.metadata.create_all(bind=engine)
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing database: {str(e)}")
        sys.exit(1)


def main():
    """Main entry point"""
    try:
        logger.info("Starting AI Knowledge Digest Platform...")

        # Initialize database
        init_database()

        # Start scheduler
        cron = Cron()
        cron.run_scheduler()

    except KeyboardInterrupt:
        logger.info("Application stopped by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()