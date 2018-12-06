

class Song:
    def __init__(self, id, title, genre, artist, description):
        self.id = id
        self.title = title
        self.genre = genre
        self.artist = artist
        self.description = description


genres = [
    'Blues', 'Classical', 'Jazz', 'Reggae', 'Country',
    'Electronic', 'Folk', 'Rock', 'Soul/R&B'
]
songs = [
    Song(
        1,
        'Across the Tappan Zee',
        'Folk',
        'Glenn Jones',
        '''
        Instrumental for two banjos from the album My Garden State.
        '''
    ),
    Song(
        2,
        'All Day Sucker',
        'Soul/R&B',
        'Stevie Wonder',
        '''
        Masterful funkiness from Stevie Wonder's album Songs in the Key of Life.
        '''
    ),
    Song(
        3,
        'La Grange',
        'Blues',
        'ZZ Top',
        '''
        From the 1973 album Tres Hombres.
        '''
    ),
    Song(
        4,
        'Little Maggie',
        'Folk',
        'Robert Plant',
        '''
        A reworking of an an Appalacian folk song. From Robert Plant's 2014
        album Lullaby and the Ceasless Roar
        '''
    )
]


def songs_for(genre):
    return [s for s in songs if s.genre == genre]


def get_song(id):
    for s in songs:
        if s.id == id:
            return s
    return None

