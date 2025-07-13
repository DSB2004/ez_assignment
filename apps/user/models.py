from django.db import models
import uuid

class Role(models.TextChoices):
    OPERATION='operation'
    CLIENT='client'
    

class User(models.Model):
    id=models.UUIDField(default=uuid.uuid4(),primary_key=True)
    email=models.EmailField(unique=True)
    password=models.TextField()
    is_verified=models.BooleanField(default=False)
    role= models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.CLIENT
    )
