from django.db import models
from django.contrib.auth.models import User


class Results(models.Model):
	UserId = models.ForeignKey('User', on_delete=models.CASCADE)
	Difficulty = models.ForeignKey('Difficulty', on_delete=models.CASCADE)
	Time = models.DateTimeField()
	Duration = models.TimeField()


class Difficulty(models.Model):
	Difficulty = models.CharField()
