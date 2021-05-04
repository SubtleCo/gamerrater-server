from django.db import models

class GameCategory(models.Model):
    game = models.ForeignKey("Game", on_delete=models.DO_NOTHING)
    category = models.ForeignKey("Category", on_delete=models.DO_NOTHING)