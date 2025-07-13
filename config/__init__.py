from .celery import app as celery_app

__all__ = ['celery_app']


# To run -> celery -A config worker --loglevel=info --concurrency=4