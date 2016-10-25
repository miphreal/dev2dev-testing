from datetime import timedelta

from django.db import models
from django.utils import timezone


class Question(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    def was_created_recently(self):
        now = timezone.now()
        return now - timedelta(days=1) <= self.created <= now

    def is_active_question(self):
        now = timezone.now()
        return now - timedelta(days=30) <= self.pub_date <= now


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
