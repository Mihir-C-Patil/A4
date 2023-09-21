from flask import Blueprint, render_template, redirect, url_for, session, request, flash
from better_profanity import Profanity
from flask_wtf import FlaskForm
from wtforms import TextAreaField, HiddenField, SubmitField, SelectField
from wtforms.validators import DataRequired, length, ValidationError
from games.authentication.authentication import login_required
import games.adapters.repository as repo
import games.gamesDescription.services as services
from games.authentication import services as authservice

from games.gameLibrary.gameLibrary import get_genres_and_urls
from games.gameLibrary.services import get_genres

class ReviewForm(FlaskForm):
    options = [(1, '1 star'), (2, '2 stars'), (3, '3 stars'), (4, '4 stars'), (5, '5 stars')]
    rating = SelectField('Rating', choices=options, coerce=int)
    comment = TextAreaField('Review')
    #game_id = HiddenField('game_id')
    submit = SubmitField('Submit Review')
    # game_id = HiddenField("Game id")

games_description_blueprint = Blueprint('games_description_bp', __name__)


@games_description_blueprint.route('/games-description/<int:game_id>',
                                   methods=['GET'])
def games_description(game_id):
    get_game = services.get_game(repo.repo_instance, game_id)
    # get_similar_games = None
    if len(get_game.genres) > 0:
        get_similar_games = services.similar_game(repo.repo_instance,
                                                  get_game.genres)

    genres = get_genres(repo.repo_instance)
    form = ReviewForm()
    get_average = services.get_average(get_game)
    get_number_of_reviews = len(get_game.reviews)
    return render_template('gameDesc.html', game=get_game,
                           similar_games=[game for game in get_similar_games
                                          if game != get_game][0:4],
                           all_genres=genres,
                           genre_urls=get_genres_and_urls(), form=form, average=get_average, review_number=get_number_of_reviews)

@games_description_blueprint.route('/review/<int:game_id>', methods=['POST'])
@login_required
def post_review(game_id):
    game = services.get_game(repo.repo_instance, game_id)
    form = ReviewForm()
    if 'username' in session:
        print('yes')
        user = authservice.get_user(session['username'], repo.repo_instance)
        if form.validate_on_submit():
            if services.add_review(form.rating.data, form.comment.data, user, game):
                flash('Review successfully added', 'success')
                return redirect(url_for('games_description_bp.games_description', game_id=game_id))
            else:
                flash('You have already added a review for this game!', 'error')
    print('hello5')
    return render_template('gameDesc.html', game_id=game_id, form=form, game=game)

