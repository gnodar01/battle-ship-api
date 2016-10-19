"""File for retrieving enteties and properties from datastore."""

from google.appengine.ext import ndb
import endpoints

from models.ndbModels import User
from validators import check_player_registered


def get_by_urlsafe(urlsafe, model):
    """Returns an ndb.Model entity that the urlsafe key points to. Checks
        that the type of entity returned is of the correct kind. Raises an
        error if the key String is malformed or the entity is of the incorrect
        kind
    Args:
        urlsafe: A urlsafe key string
        model: The expected entity kind
    Returns:
        The entity that the urlsafe Key string points to or None if no entity
        exists.
    Raises:
        ValueError:"""
    try:
        key = ndb.Key(urlsafe=urlsafe)
    except TypeError:
        raise endpoints.BadRequestException('Invalid Key')
    except Exception, e:
        if e.__class__.__name__ == 'ProtocolBufferDecodeError':
            raise endpoints.BadRequestException('Invalid Key')
        else:
            raise

    entity = key.get()
    if not entity:
        return None
    if not isinstance(entity, model):
        raise ValueError('Incorrect Kind')
    return entity


def get_user(username):
    """Takes in the name of a player/user,
    and returns a user query object"""
    user = User.query(User.name == username).get()
    if not user:
        raise endpoints.ConflictException(
            '{} does not exist.'.format(username))
    return user


def get_registered_player(game, username):
    player = get_user(username)
    check_player_registered(game, player)
    return player
