# The current api only supports read operations, but has placeholder routes
# and verbs for a more complete implementation. Write operations will return
# 403.


from flask import (
    Blueprint, request, make_response, jsonify
)
import json
from songcat.model import get_all_songs, get_song


# use /api as the route for all API calls.
bp = Blueprint('api', __name__, url_prefix='/api')


@bp.route('/song')
def song_list():
    # Get all the songs.
    songs = get_all_songs()
    return jsonify(Songs=[s.serialize for s in songs])


@bp.route('/song/add', methods=('POST',))
def song_add():
    response = make_response(
        json.dumps('Authorization required'.format(id)), 403
    )
    return response


@bp.route('/song/<int:id>', methods=('GET', 'PUT', 'PATCH', 'DELETE'))
def song_action(id):
    # Peform an action on an individual song.
    if request.method == 'GET':
        song = get_song(id)
        if song is None:
            response = make_response(
                json.dumps('No song found with id {}'.format(id)), 404
            )
            return response
        return jsonify(song.serialize)
    else:
        response = make_response(
            json.dumps('Authorization required'.format(id)), 403
        )
        return response
