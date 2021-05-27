"""Module for generating games in which more than 5 people can play"""
import sqlite3
from django.shortcuts import render
from gamerraterapi.models import Game
from gamerraterreports.views import Connection

def games_with_6_plus_players(request):
    if request.method == "GET":
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            # Query for all games, with related user info.
            db_cursor.execute("""
                SELECT
                    id,
                    title
                FROM
                    gamerraterapi_game
                WHERE
                    player_max > 5
            """)

            dataset = db_cursor.fetchall()

            query_games = {}

            for row in dataset:
                game = Game()
                game.title = row["title"]
                game.id = row["id"]

                query_games[game.id] = game

        games_with_6_plus_players_list = query_games.values()

        template = "games/games_with_6_plus_players.html"
        context = {
            'games_list': games_with_6_plus_players_list
        }

        return render(request, template, context)
