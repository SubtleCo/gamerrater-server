from gamerraterapi.models.rating import Rating
from django.db import models

class Game(models.Model):
    title = models.CharField(max_length=50)
    released = models.IntegerField()
    description = models.TextField()
    player_min = models.IntegerField()
    player_max = models.IntegerField()
    age_min = models.IntegerField()
    designer = models.CharField(max_length=50)
    categories = models.ManyToManyField("Category", related_name="games")

    @property
    def average_rating(self):
        """Averate rating calculated attribute for each game"""
        ratings = Rating.objects.filter(game=self)

        total_rating = 0
        for rating in ratings:
            total_rating += rating.score

        average = 0
        if (len(ratings)):
            average = total_rating / len(ratings)
        return average