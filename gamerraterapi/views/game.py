### View module for handling requests about games
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from gamerraterapi.models import Game, Category

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
        r = request.data
        game = Game()
        game.title = r['title']
        game.released = r['released']
        game.description = r['description']
        game.player_min = r['player_min']
        game.player_max = r['player_max']
        game.age_min = r['age_min']
        game.designer = r['designer']

        try:
            game.save()
            categories = Category.objects.in_bulk(r['categories'])
            game.categories.set(categories)
            serializer = GameSerializer(game, context={'request': request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)


################################  SERIALIZERS  ################################

class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ('id', 'title', 'released', 'description', 'player_min', 'player_max',
            'age_min', 'designer', 'categories', 'average_rating')
        depth = 1
