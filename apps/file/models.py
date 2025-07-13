from django.db import models
import uuid


class File(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = models.TextField()
    description=models.TextField()
    extension=models.TextField()
    size=models.TextField()
    src =models.URLField(default=None,null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    