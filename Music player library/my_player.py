from song import Song
from binary_search_tree import BinarySearchTree
from stack import Stack


class MyPlayer:
    def __init__(self):
        """
        initializing attributes required for this file
        """
        self.songList = []
        self.is_sorted = False
        self.yearMemory = {}
        self.playHistory = Stack()
        # TODO: Modify the above attribute for Task 6

    def loadLibrary(self, filename):
        '''using this function to load songs from the given text files into songList attribute'''
        lines = open(filename,'r')# opening the text file
        for line in lines:
            songs = line.strip().split('|') #splitting the song attributes
            '''assigning song attributes'''
            self.artist_name=songs[0]
            self.song_title=songs[1]
            self.song_id=songs[2]
            self.duration=float(songs[3])
            self.year=int(songs[4])
            song = Song(self.artist_name, self.song_title,self.song_id,self.duration,self.year )
            self.songList.append(song) #appending the song attributes to songList



    def quickSort(self):
            ''' Sorting using Quicksort based on song release year'''
            def quick_sort(x, first, last):
                if first < last:
                    # finding the splitpoint
                    splitpoint = partition(x, first, last)
                    #splitting for recursive sorting for left and right sublist
                    quick_sort(x, first, splitpoint - 1)
                    quick_sort(x, splitpoint + 1, last)

            def partition(x, first, last):
                pivot = x[first]#choosing pivot element
                left = first + 1
                right = last
                done = False

                while not done:
                    # Move the left index to the right until a value greater than pivot is found
                    while left <= right and x[left] <= pivot:
                        left = left + 1
                    # Move the right index to the left until a value smaller than pivot is found
                    while x[right] >= pivot and right >= left:
                        right = right - 1
                    # If right index is less than left index, swap the elements
                    if right < left:
                        done = True
                    else:
                        temp = x[left]
                        x[left] = x[right]
                        x[right] = temp
                # Swap the pivot element with the element at the right index
                temp = x[first]
                x[first] = x[right]
                x[right] = temp
                return right

            # Create an empty list to store years from the songList
            year_list = []
            for line in self.songList:
                year_list.append(line.year)
            quick_sort(year_list, 0, len(year_list) - 1)
            sorted_song_list = []
            for year in year_list:
                for song in self.songList:
                    # If a song's year matches the current year, add it to the sorted_song_lis
                    if song.year == year:
                        sorted_song_list.append(song)
            y = []
            seen = set()  # Create a set to keep track of seen songs and avoiding duplication

            for i in sorted_song_list:
                if i not in seen:
                    y.append(i)
                    seen.add(i)



            # TODO: Sort your songList here...
            self.songList = y  # Assuming you want to update the original songList
            self.is_sorted = True  # Assuming you want to track the sorting state






    def playSong(self, title):
        '''Play a song with the given title and add it to the play history.'''
        for x in self.songList:
             if x.song_title == title:
                 Song.play(x)
                 self.playHistory.push(x) # Search for the song in songList, play it, and add it to the play history


    def getLastPlayed(self):
        '''Get the last played song from the play history.'''
        if not self.playHistory.isEmpty():
            return self.playHistory.peek()
        else:
            return None


    def hashfunction(self,song):
        '''  Hash function to determine the key for a song based on its year.'''
        return song.year

    def buildYearMemory(self):
        '''Build a dictionary where keys are years and values are entered via Binary Search Tree .'''
        for song in self.songList:
            #find year using hashfunction
            year = self.hashfunction(song)

            if year not in self.yearMemory:
                #create a new Binary Search Tree for this year if year not in yearMemory

                self.yearMemory[year] = BinarySearchTree()

            # Add the song to the Binary Search Tree for the corresponding year
            self.yearMemory[year].put(song.song_title,song)


    def getYearMemory(self, year, title):
        ''' Retrieve a song based on the given year and title from the yearMemory dictionary.'''
        steps = 0  # Number of steps used to search for the song
        the_song = None  # The song

        # # Set the current dictionary to yearMemory
        # Check if the given year is present in the yearMemory dictionary
        current = self.yearMemory
        if year in current.keys():
            # If the year is present, search for the song in the corresponding Binary Search Tree (BST)
            the_song=current[year].get(title)
            # Get the number of steps taken during the search operation

            steps=self.yearMemory[year].steps
        else:
            # If the given year is not found in the dictionary, return None for both steps and the song
            return {'steps': None, 'song': None}
        # Return the number of steps taken during the search and the found song
        return {"steps": steps, "song": the_song}


    def getSong(self, year, title):
        '''Retrives a song using specified year and title from sonList using linear search'''
        steps = 0  # Number of steps used to search for the song
        the_song = None  # The song
        for x in self.songList:
            if x.year==year and x.song_title==title:
                # If a match is found, set the_song to the current song
                the_song = x
                # Increment the step count for each iteration
                steps=steps+1
                break

            else:
                steps=steps+1
        # Return the number of steps taken during the search and the found song
        return {"steps": steps, "song": the_song}


