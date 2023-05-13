from django.db import models

# Create your models here.
from django.utils import timezone
from django.contrib.auth.models import User

class usermanage(models.Model):
    realname = models.CharField(max_length=256)
    userid=models.CharField(max_length=256)
    content = models.TextField()
    author = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    #created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.realname