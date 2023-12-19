from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    username = models.CharField(max_length=255, blank=True, unique=True)
    photo_profile = models.ImageField(upload_to="media/", verbose_name="Фотография")

    def __str__(self):
        return self.username


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    publish_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField()
    desc_text = models.CharField(max_length=200, blank=True, unique=True)
    full_desc_text = models.CharField(max_length=200, blank=True, unique=True)
    photo_question = models.ImageField(upload_to="media/", verbose_name="Фотография")

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text


class Vote(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)





