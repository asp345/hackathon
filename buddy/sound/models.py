from django.db import models
from django.utils import timezone
import random
import usermanage
# Create your models here.

class sound(models.Model):
    def random_int():
        return random.randint(1, 65535)
    senderid = models.CharField(max_length=255)
    random_num=models.CharField(max_length=7)
    receiverid = models.CharField(max_length=255,default=0)
    #author = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)