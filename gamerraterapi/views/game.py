### View module for handling requests about games
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from gamerraterapi.models import Game, Category
from django.contrib.auth.models import User

class GameViewSet(ViewSet):

    def retrieve(self, request, pk=None):
        try:
            game = Game.objects.get(pk=pk)
            serializer = GameSerializer(game, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        games = Game.objects.all()

        serializer = GameSerializer(
            games, many=True, context={'request': request}
        )
        return Response(serializer.data)

    def create(self, request):
        req = request.data
        game = Game()
        game.user = User.objects.get(pk=request.auth.user.id)
        game.title = req['title']
        game.released = req['released']
        game.description = req['description']
        game.player_min = req['player_min']
        game.player_max = req['player_max']
        game.age_min = req['age_min']
        game.designer = req['designer']

        try:
            game.save()
            categories = Category.objects.in_bulk(req['categories'])
            game.categories.set(categories)
            serializer = GameSerializer(game, context={'request': request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        req = request.data
        game = Game.objects.get(pk=pk)
        game.title = req['title']
        game.released = req['released']
        game.description = req['description']
        game.player_min = req['player_min']
        game.player_max = req['player_max']
        game.age_min = req['age_min']
        game.designer = req['designer']

        try:
            game.save()
            categories = Category.objects.in_bulk(req['categories'])
            game.categories.set(categories)
            serializer = GameSerializer(game, context={'request': request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)



################################  SERIALIZERS  ################################

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name')

class GameSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)

    class Meta:
        model = Game
        fields = ('id', 'title', 'released', 'description', 'player_min', 'player_max',
            'age_min', 'designer', 'categories', 'average_rating', 'user')
        depth = 1
