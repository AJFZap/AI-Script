from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    personal_token = models.CharField(max_length=255, blank=True, null=True)

class ScriptsList(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    videoTitle = models.CharField(max_length=300)
    videoLink = models.URLField(unique=True)
    generatedScript = models.TextField()
    generatedSummary = models.TextField()
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.videoLink
    
    class Meta:
        ordering = ['-createdAt']
