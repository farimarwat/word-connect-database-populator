from django.db import models


# Create your models here.

class Chapter(models.Model):
    chapter_name = models.CharField(max_length=50, unique=True)
    chapter_completed = models.BooleanField(default=False)


class Level(models.Model):
    level_serial = models.IntegerField()
    level_letters = models.CharField(max_length=50, unique=True)
    level_completed = models.BooleanField(default=False)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)


class Solution(models.Model):
    solution_word = models.CharField(max_length=50)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
