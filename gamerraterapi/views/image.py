### View module for handling requests about images
from gamerraterapi.models.image import GamePicture
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from gamerraterapi.models import Game, Category
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
import uuid, base64


class ImageViewSet(ViewSet):

    def create(self, request):

        req = request.data
        image = GamePicture()
        image.user = User.objects.get(pk=request.auth.user.id)
        image.game = Game.objects.get(pk=req['game_id'])

        format, imgstr = req['game_image'].split(';base64,')
        ext = format.split('/')[-1]
        data = ContentFile(base64.b64decode(imgstr), name=f'{req["game_id"]}-{uuid.uuid4()}.{ext}')
        image.action_pic = data

        try:
            image.save()
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)