from django.db import models

class Rating(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    game = models.ForeignKey("Game", on_delete=models.CASCADE)
    score = models.IntegerField(min=0, max=10)