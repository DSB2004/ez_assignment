from celery import shared_task
import logging
logger = logging.getLogger(__name__)
class MailService:
    @shared_task
    def send_mail(email,content):
        logger.info(f"Mail sent to User {email} -> {content}")
        