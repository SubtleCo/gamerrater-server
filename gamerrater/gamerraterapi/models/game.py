from django.db import models

class Game(models.Model):
    title = models.CharField(max_length=50)
    released = models.IntegerField()
    description = models.TextField()
    player_min = models.IntegerField()
    player_max = models.IntegerField()
    age_min = models.IntegerField()
    designer = models.CharField()
