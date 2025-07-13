
import os
import django
import argparse
import logging
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from apps.file.models import File
from service.upload import Upload


logger = logging.getLogger(__name__)


logger = logging.getLogger(__name__)


def main(file_id):
    try:    
        file=File.objects.get(id=file_id)
        signed_url=Upload.get_signed_url(file)['download']
        logger.info(f"Download Link: {signed_url}")  
    except File.DoesNotExist:
        logger.warn(f"File:{file_id} does not exist")



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file_id")
    args = parser.parse_args()
    main(args.file_id)


# To run -> python scripts/get_signed_url.py <file_id>