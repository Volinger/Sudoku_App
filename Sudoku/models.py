from django.db import models
from django.contrib.auth.models import User


class Results(models.Model):
	UserId = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True)
	Difficulty = models.ForeignKey('Difficulty', on_delete=models.CASCADE)
	Time = models.DateTimeField()
	Duration = models.FloatField()  # Duration in seconds


class Difficulty(models.Model):
	Option = models.CharField(max_length=256)
	FieldsToRemove = models.FloatField()  # Defines % of sudoku grid cells, which should be cleared, rounded down.
