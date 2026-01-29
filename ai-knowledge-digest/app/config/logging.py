import logging
import logging.handlers
from app.config.settings import LOG_LEVEL


# Configure logging settings
def setup_logging():
    logger = logging.getLogger("ai_digest")
    logger.setLevel(LOG_LEVEL)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(LOG_LEVEL)

    # File handler
    file_handler = logging.handlers.RotatingFileHandler(
        "logs/ai_digest.log",
        maxBytes=10485760,  # 10MB
        backupCount=5,
    )
    file_handler.setLevel(LOG_LEVEL)

    # Formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger


logger = setup_logging()