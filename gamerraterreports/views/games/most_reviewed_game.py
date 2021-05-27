"""Module for generating the most reviewed game"""
import sqlite3
from django.shortcuts import render
from gamerraterapi.models import Game
from gamerraterreports.views import Connection


def most_reviewed_game(request):
    if request.method == "GET":
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            # Query for all games, with related user info.
            db_cursor.execute("""
                SELECT
                    title,
                    MAX(ratings)
                FROM (
                    SELECT
                        g.id,
                        g.title,
                        COUNT(r.id) ratings
                    FROM
                        gamerraterapi_game g
                    JOIN
                        gamerraterapi_rating r
                    ON
                        r.game_id = g.id
                    GROUP BY
                        g.id
                )
            """)

            data = db_cursor.fetchone()

            game = Game()
            game.title = data["title"]

        most_reviewed_game = game

        template = "games/most_reviewed_game.html"
        context = {
            'most_reviewed_game': most_reviewed_game
        }

        return render(request, template, context)
