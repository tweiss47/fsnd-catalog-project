

class Song:
    def __init__(self, id, title, genre):
        self.id = id
        self.title = title
        self.genre = genre


genres = [
    'Blues', 'Classical', 'Jazz', 'Reggae', 'Country',
    'Electronic', 'Folk', 'Rock', 'Soul/R&B'
]
songs = [
    Song(1, 'Across the Tappan Zee', 'Folk'),
    Song(2, 'All Day Sucker', 'Soul/R&B'),
    Song(3, 'La Grange', 'Blues'),
    Song(4, 'Little Maggie', 'Folk')
]


def songs_for(genre):
    return [s for s in songs if s.genre == genre]

