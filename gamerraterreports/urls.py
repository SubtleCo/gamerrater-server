from gamerraterreports.views.games.games_for_under_8s import games_for_under_8s
from gamerraterreports.views.games.gamer_with_most_games import gamer_with_most_games
from django.urls import path
from .views import top_5_games_list, bottom_5_games_list, games_per_category_list, games_with_6_plus_players, most_reviewed_game

urlpatterns = [
    path('reports/games/top5', top_5_games_list),
    path('reports/games/bottom5', bottom_5_games_list),
    path('reports/categories/count', games_per_category_list),
    path('reports/games/party', games_with_6_plus_players),
    path('reports/games/most_reviewed', most_reviewed_game),
    path('reports/users/mostgames', gamer_with_most_games),
    path('reports/games/under8s', games_for_under_8s)
]