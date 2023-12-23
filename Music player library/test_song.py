from song import Song

if __name__ == "__main__":
    # Test1: test constructor
    artist_name = "All Time Low"
    song_title = "Umbrella"
    song_id = "SOPOPLW12A8C13A905"
    duration = 227.70893
    year = 2008

    my_song = Song(artist_name, song_title, song_id, duration, year)

    print("Test1: test constructor")
    print("Artist name: ", my_song.artist_name, ", excepted: ", artist_name)
    print("Song title: ", my_song.song_title, ", excepted: ", song_title)
    print("Song id: ", my_song.song_id, ", excepted: ", song_id)
    print("Duration: ", my_song.duration, ", excepted: ", duration)
    print("Year: ", my_song.year, ", excepted: ", year)

    # test2: test __str__
    print("\nTest2: test __str__")
    print("Yours:", my_song, sep="\t\t")
    print("Excepted: ", "Umbrella by All Time Low (ID: SOPOPLW12A8C13A905) released in 2008", sep="\t")

    # test3: test play
    print("\nTest3: test play")
    my_song.play()
    print("Excepted: ", "Umbrella is playing, with a duration of 227.70893 second(s)", sep="\t")
