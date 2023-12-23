class Song:
    def __init__(self, artist_name: str, song_title: str, song_id: str, duration: float, year: int):
        self.artist_name = artist_name
        self.song_title = song_title
        self.song_id = song_id
        self.duration = duration
        self.year = year

    def __str__(self):
        # Return a string containing song details
        return self.song_title + ' by ' + self.artist_name + ' (ID: ' + self.song_id + ') released in '+str(self.year)

    def play(self):
        # Print a message which indicates the song playing and its duration
        print(('%s is playing, with a duration of %s second(s)')%(self.song_title,self.duration))
