from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class GamePicture(models.Model):
    game = models.ForeignKey('Game', on_delete=models.DO_NOTHING, related_name='pictures')
    action_pic = models.ImageField(upload_to='actionimages', height_field=None, width_field=None, max_length=None, null=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    timestamp = models.DateTimeField(default=timezone.now, editable=False)