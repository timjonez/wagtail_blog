from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.shortcuts import redirect

# Create your models here.

class Prayer(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField(max_length=500)
    date = models.DateTimeField(default=timezone.now)

    def get_absolute_url(self):
        return reverse('prayers:prayer_detail',kwargs={'pk':self.pk})


    def __str__(self):
        return self.title
