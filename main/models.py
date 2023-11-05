from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Topic(models.Model):
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    user_name = models.CharField()

    def __str__(self):
        return self.text


class Entry(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    user_name = models.CharField()

    class Meta:
        verbose_name_plural = 'Entries'

    def __str__(self):
        return f'{self.text[:50]}'

