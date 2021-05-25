### View module for handling requests about reviews
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from django.contrib.auth.models import User
from gamerraterapi.models import Game, Rating


class RatingViewSet(ViewSet):

    def create(self, request):
        req = request.data
        rating = Rating()

        rating.user = User.objects.get(pk=request.auth.user.id)
        rating.game = Game.objects.get(pk=req['game_id'])
        rating.score = req['score']

        try:
            rating.save()
            serializer = RatingSerializer(rating, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({'reason': ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        req = request.data
        rating = Rating.objects.get(pk=pk)
        rating.score = req['score']


        try:
            rating.save()
            serializer = RatingSerializer(rating, context={'request': request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)


################################  SERIALIZERS  ################################

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ('id', 'user', 'game', 'score')
        depth = 1




