from django.db import models

class Image(models.Model):
    photo = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=100)
    user = models.ForeignKey("User", on_delete=models.DO_NOTHING)
    timestamp = models.DateTimeField()