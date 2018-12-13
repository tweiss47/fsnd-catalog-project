from flask import (
    Blueprint, request, make_response, jsonify
)
import json
from . import model


bp = Blueprint('api', __name__, url_prefix='/api')


@bp.route('/song')
def song_list():
    songs = model.get_songs(100)
    return jsonify(Songs=[s.serialize for s in songs])


@bp.route('/song/add', methods=('POST',))
def song_add():
    response = make_response(
        json.dumps('Authorization required'.format(id)), 403
    )
    return response


@bp.route('/song/<int:id>', methods=('GET', 'PUT', 'PATCH', 'DELETE'))
def song_action(id):
    if request.method == 'GET':
        song = model.get_song(id)
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
