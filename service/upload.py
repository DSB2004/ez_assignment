from celery import shared_task
from imagekitio import ImageKit
from imagekitio.models.UploadFileRequestOptions import UploadFileRequestOptions
from config import settings
from base64 import b64decode
from apps.file.models import File
import os
import logging
logger = logging.getLogger(__name__)

class Upload:
    @shared_task
    def upload_file(temp_path, file_name, file_id):
        imagekit = ImageKit(
            private_key=settings.CLOUD_PRIVATE_KEY,
            public_key=settings.CLOUD_PUBLIC_KEY,
            url_endpoint=settings.CLOUD_URL
        )

        try:
            with open(temp_path, 'rb') as f:
                result = imagekit.upload_file(
                    file=f,
                    file_name=file_name,
                    options=UploadFileRequestOptions(
                        is_private_file=True,
                        
                    )
                )
            print(result.response_metadata.raw)
            image_url = result.response_metadata.raw.get('url')

            if image_url:
                uploaded_file = File.objects.get(id=file_id)
                uploaded_file.src = image_url
                uploaded_file.save()
                return image_url
            else:
                logger.error(f"Upload failed: {result.get("error")}")
                return None
            
        except Exception as e:
            logger.exception("Error during file upload")
            return None
        
        finally:
            try:
                if os.path.exists(temp_path):
                    os.remove(temp_path)
                    logger.info(f"Temporary file {temp_path} deleted.")
            except Exception as e:
                logger.warning(f"Failed to delete temp file {temp_path}")
    
    def get_signed_url(file):
        src_url = file.src
        url_endpoint = settings.CLOUD_URL

        if not src_url.startswith(url_endpoint):
            return {"message": "Invalid source URL","download":None}
        
        relative_path = src_url.replace(url_endpoint, '').lstrip('/')
        imagekit = ImageKit(
            private_key=settings.CLOUD_PRIVATE_KEY,
            public_key=settings.CLOUD_PUBLIC_KEY,
            url_endpoint = settings.CLOUD_URL
            )
        signed_url = imagekit.url({
            "path": relative_path,
            "signed": True,
            "expire_seconds": 300
        })
        return {"message": "Your download link will be accessible for next 5 minutes","download":signed_url}


        