import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from app.config.settings import (
    SMTP_HOST,
    SMTP_PORT,
    SMTP_USER,
    SMTP_PASSWORD,
    FROM_EMAIL,
)
from app.config.logging import logger


class EmailSender:
    def send_email(
        self,
        to_email: str = None,
        recipient: str = None,
        subject: str = "",
        html_content: str = None,
        body: str = None,
        html: str = None,
        **kwargs,
    ):
        """
        Ultra-flexible email sender.
        Supports:
        - to_email / recipient
        - html / body / html_content
        """

        # ✅ resolve recipient
        email = to_email or recipient
        if not email:
            raise ValueError("Recipient email not provided")

        # ✅ resolve body (any name)
        content = html_content or body or html
        if not content:
            raise ValueError("Email content not provided")

        msg = MIMEMultipart("alternative")
        msg["From"] = FROM_EMAIL
        msg["To"] = email
        msg["Subject"] = subject

        msg.attach(MIMEText(content, "html"))

        try:
            with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
                server.starttls()
                server.login(SMTP_USER, SMTP_PASSWORD)
                server.sendmail(FROM_EMAIL, email, msg.as_string())

            logger.info(f"Email sent to {email}")

        except Exception as e:
            logger.error(f"Failed to send email to {email}: {e}")
            raise