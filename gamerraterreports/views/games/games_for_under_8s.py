import sqlite3
from django.shortcuts import render
from gamerraterapi.models import Game
from gamerraterreports.views import Connection

def games_for_under_8s(request):
    """ Function to build a list of games, limit top 5"""
    if request.method == 'GET':
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            db_cursor.execute("""
                SELECT
                    id,
                    title,
                    age_min
                FROM
                    gamerraterapi_game
                WHERE
                    age_min < 8
            """)

            dataset = db_cursor.fetchall()

            games_for_under_8s = {}

            for row in dataset:
                game = Game()
                game.id = row["id"]
                game.title = row["title"]

                games_for_under_8s[game.id] = game

        list_of_games_for_under_8s = games_for_under_8s.values()

        template = 'games/games_for_under_8s.html'
        context = {
            'games_for_under_8s': list_of_games_for_under_8s
        }

        return render(request, template, context)


