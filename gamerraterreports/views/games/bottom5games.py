import sqlite3
from django.shortcuts import render
from gamerraterapi.models import Game
from gamerraterreports.views import Connection

def bottom_5_games_list(request):
    """ Function to build a list of games, limit top 5"""
    if request.method == 'GET':
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            db_cursor.execute("""
                SELECT
                    g.id,
                    g.title,
                    g.description,
                    AVG(r.score) avg_score
                FROM
                    gamerraterapi_game g
                JOIN
                    gamerraterapi_rating r ON r.game_id = g.id
                GROUP BY
                    g.title
                ORDER BY
                    avg_score ASC
                LIMIT 5
            """)

            dataset = db_cursor.fetchall()

            bottom_5_games = {}

            for row in dataset:
                game = Game()
                game.id = row["id"]
                game.title = row["title"]
                game.description = row["description"]
                game.score = row["avg_score"]

                bottom_5_games[game.id] = game

        list_of_bottom_5_games = bottom_5_games.values()

        template = 'games/bottom_5_games.html'
        context = {
            'bottom_5_games_list': list_of_bottom_5_games
        }

        return render(request, template, context)


