import endpoints
from re import match

from models.ndbModels import User

COLUMNS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
ROWS = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
GRID = [(column + row) for column in COLUMNS for row in ROWS]


def check_email(email):
    email_format_match = match(
        r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)',
        email)
    if not email_format_match:
        raise endpoints.ConflictException('E-mail is not valid')


def check_username_len(username):
    if len(username) < 3:
        raise endpoints.ConflictException(
            'Username must be at least 3 characters')


def check_user_exists(username):
    if User.query(User.name == username).get():
        raise endpoints.ConflictException(
            'A User with that name already exists')


def check_email_exists(email):
    if User.query(User.email == email).get():
        raise endpoints.ConflictException(
            'A User with that E-Mail already exists')


def check_player_registered(game, player):
    if game.player_one != player.key and game.player_two != player.key:
        raise endpoints.ConflictException(
            '{} is not registered for this game'.format(player.name))


def check_players_unique(player_one_name, player_two_name):
    if player_one_name == player_two_name:
        raise endpoints.ConflictException(
            'Player one cannot be the same as player two.')


def check_game_open(game):
    if game.player_two:
        raise endpoints.ConflictException('This game is already full!')


def coords_validity_check(row_coord, col_coord):
    """Raise errors if the row or column coordinates are not valid"""
    if row_coord not in ROWS:
        raise endpoints.ConflictException(
            'Row coordinate must be between 1 - 10')

    if col_coord not in COLUMNS:
        raise endpoints.ConflictException(
            'Column coordinate must be between A - J')
