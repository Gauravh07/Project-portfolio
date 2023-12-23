from my_player import MyPlayer
import random

player = MyPlayer()

if __name__ == "__main__":
    # Test1: read from file
    player.loadLibrary("subset_songs.txt")   # Change to the following line when you are confident with your code.
    # player.loadLibrary("all_songs.txt")
    print("Loaded %d songs from file" % len(player.songList))
    print("  the first one of which is:", str(player.songList[0]))

    # Test2: test sort
    player.quickSort()
    print("The release years are: ", end="")
    for s in player.songList:
        print(s.year, end="->")

    # Test3: test play
    random_song = random.choice(player.songList)
    print("\n\nTest playing song: ", str(random_song), "...")
    player.playSong(random_song.song_title)

    # another_random_song = random.choice(player.songList)
    # print("\nTest playing another song: ", str(another_random_song))
    # player.playSong(another_random_song.song_title)

    # Test4: test show last played
    print("\nTest showing last played song...")
    last_played = player.getLastPlayed()
    print("Last played song is: ", str(last_played))

    # Test5: test build year memory function
    print("\nTest building year memory...")
    player.buildYearMemory()
    print("There are %d years in the year memory" % len(player.yearMemory))

    # Test6: test get year memory function
    random_song = random.choice(player.songList)
    print("\nTest getting year memory for song: ", str(random_song))
    year = random_song.year
    title = random_song.song_title
    result = player.getYearMemory(year, title)
    song = result["song"]
    steps = result["steps"]
    print("The song found is: ", str(song))
    print("The number of steps used is: ", steps)

    # Test7: test get year memory function for the same song
    print("\nTest getting song for the same song: ", str(random_song))
    result = player.getSong(year, title)
    song = result["song"]
    steps = result["steps"]
    print("The song found is: ", str(song))
    print("The number of steps used is: ", steps)

















































