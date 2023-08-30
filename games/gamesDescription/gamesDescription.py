from flask import Blueprint, render_template
import games.adapters.repository as repo
import games.gamesDescription.services as services
from markupsafe import escape

from games.gameLibrary.gameLibrary import get_genres_and_urls
from games.gameLibrary.services import get_genres

games_description_blueprint = Blueprint('games_description_bp', __name__)


@games_description_blueprint.route('/games-description/<int:game_id>', methods=['GET'])
def games_description(game_id):
    get_game = services.get_game(repo.repo_instance, game_id)
    #get_similar_games = None
    if len(get_game.genres) > 0:
        get_similar_games = services.similar_game(repo.repo_instance, get_game.genres)

    genres = get_genres(repo.repo_instance)
    return render_template('gameDesc.html', game=get_game, similar_games=[game for game in get_similar_games if game != get_game][0:4], all_genres=genres,
                           genre_urls=get_genres_and_urls())

