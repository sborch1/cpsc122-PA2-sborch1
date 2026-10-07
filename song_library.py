"""
Programmer: Stephen Borch
Class: CPSC 122, Fall 2026
Programming Assignment #2
Date: 10/06/26
I attempted the bonus

Description:
This module defines Song and SongLibrary for managing a music library of songs
"""
from pathlib import Path

class Song:
    """Represents a song and its attributes"""
    
    MIN_RATING = 1
    MAX_RATING = 5
    SORT_ATTRIBUTE = "title"
    
    def __init__(self, title: str, artist: str, genre: str, clip: str, rating: int):
        """
        Initialize a song with its attributes

        Args:
            title (str): Song title
            artist (str): Song artist
            genre (str): Song genre
            clip (str): Path to audio clip
            rating (int): Song rating from 1 to 5
        """
        
        self.title = title.lower()
        self.artist = artist.lower()
        self.genre = genre.lower()
        self.clip = clip
        self.rating = 0
        self.set_rating(rating)
        
    def __str__(self) -> str:
        """
        Return a labeled string containing the song attributes

        Returns:
            A representation of the song
        """
        
        return  (
            f"Title: {self.title}\n"
            f"Artist: {self.artist}\n"
            f"Genre: {self.genre}\n"
            f"Path to Clip: {self.clip}\n"
            f"Rating: {self.rating}"
        )
        
    def __lt__(self, other_song: "Song") -> bool:
        """
        Compare songs using the class sort attribute

        Args:
            other_song: The song to compare against

        Returns:
            True if this song sorts before the other song
        """
        
        self_val = getattr(self, Song.SORT_ATTRIBUTE)
        other_song_val = getattr(other_song, Song.SORT_ATTRIBUTE)
        
        return self_val < other_song_val
    
    def set_rating(self, rating: int) -> None:
        """
        Set the rating within the permitted range

        Args:
            rating: Rating to assign

        Notes:
            Clamp the value to the range 1 through 5
        """
        if rating < Song.MIN_RATING:
            self.rating = Song.MIN_RATING
        elif rating > Song.MAX_RATING:
            self.rating = Song.MAX_RATING
        else:
            self.rating = rating
        

    def get_attribute_string_value(self, attribute: str) -> str:
        """
        Return an attribute as a string

        Args:
            attribute: Name of the requested attribute

        Returns:
            Attribute value as a string, or an empty string
            if the attribute is unsupported
        """
        
        if attribute == "title":
            return self.title
        if attribute == "artist":
            return self.artist
        if attribute == "genre":
            return self.genre
        if attribute == "rating":
            return str(self.rating)

        return ""
        
        

    def set_attribute_value(self, attribute: str, new_attribute_value: str) -> None:
        """
        Update a supported song attribute

        Args:
            attribute: Name of the attribute to update
            new_attribute_value: New value for the attribute

        Notes:
            Convert text attributes to lowercase and validate ratings
        """
        
        if attribute == "title":
            self.title = new_attribute_value.lower()
        elif attribute == "artist":
            self.artist = new_attribute_value.lower()
        elif attribute == "genre":
            self.genre = new_attribute_value.lower()
        elif attribute == "clip":
            self.clip = new_attribute_value
        elif attribute == "rating":
            self.set_rating(int(new_attribute_value))
        

    def play_clip(self) -> None:
        """Attempt to play the audio clip without crashing on failure"""
        
        try: 
            import playsound3
            
            clip_path = Path(self.clip)
            
            if clip_path.is_file():
                playsound3.playsound(str(clip_path), block=False)
            else:
                print(f"The clip was not found: {self.clip}")
                
        except Exception as error:
            print(f"Unable to play clip: {error}")


class SongLibrary:
    """Manage a collection of Song objects"""

    def __init__(self, sort_attribute: str = "title") -> None:
        """
        Initialize an empty song library

        Args:
            sort_attribute: Attribute used by the bonus sorting feature
        """
        self._songs: list[Song] = []
        self._sort_attribute = sort_attribute

    def __str__(self) -> str:
        """
        Return an enumerated representation of the library

        Returns:
            All songs with their list positions
        """
        
        if not self._songs:
            return "The song library is empty"
        
        library_string = ""
        
        for index, song in enumerate(self._songs, start=1):
            library_string += f"Song {index}\n{song}\n\n"
        return library_string

    def perform_load(self, filename: str) -> None:
        """
        Load song records from a text file

        Args:
            filename: Path to the library file

        Notes:
            Each record contains five fields and a blank separator line
        """
        with open(filename, "r", encoding="utf-8-sig") as input_file:
            lines = input_file.readlines()
            
        record: list[str] = []
            
        for line in lines + [""]:
            if line.strip():
                record.append(line.strip())
            elif record:
                if len(record) == 5:
                    title, artist, genre, clip, rating_text = record
                        
                    try:
                        rating = int(rating_text)
                        song = Song(title, artist, genre, clip, rating)
                        self.perform_add_song(song)
                    except ValueError:
                        print(f"Skipping record with invalid rating: {rating_text}")
                else:
                    print("Skipping an invalid song record")
                record = []

    def perform_save(self, filename: str) -> None:
        """
        Save all song records to a text file

        Args:
            filename: Destination file path
        """
        with open(filename, "w", encoding="utf-8-sig") as output_file:
            for index, song in enumerate(self._songs):
                output_file.write(
                    f"{song.title}\n"
                    f"{song.artist}\n"
                    f"{song.genre}\n"
                    f"{song.clip}\n"
                    f"{song.rating}\n"
                )
                
                if index < len(self._songs) - 1:
                    output_file.write("\n")

    def perform_sort(self, attribute: str) -> None:
        """
        Sort songs using selection sort

        Args:
            attribute: title, artist, genre, or rating

        Notes:
            The bonus requires manual selection sort
        """
        
        valid_attributes = {"title", "artist", "genre", "rating"}
        
        if attribute not in valid_attributes:
            print("Invalid sort attribute")
            return
        
        self._sort_attribute = attribute
        Song.SORT_ATTRIBUTE = attribute
        
        for start_index in range(len(self._songs) - 1):
            smallest_index = start_index
            
            for current_index in range(start_index + 1, len(self._songs)):
                current_value = (self._songs[current_index].get_attribute_string_value(attribute))
                smallest_value = (self._songs[smallest_index].get_attribute_string_value(attribute))
                
                if attribute == "rating":
                    is_smaller = int(current_value) < int(smallest_value)
                else:
                    is_smaller = current_value < smallest_value
                    
                if is_smaller:
                    smallest_index = current_index
                    
            self._songs[start_index], self._songs[smallest_index] = (
                self._songs[smallest_index],
                self._songs[start_index]
            )


    def perform_search(
        self, search_attribute: str, search_attribute_value: str
    ) -> Song | None:
        """
        Return the first song matching the requested value

        Args:
            search_attribute: Attribute to search
            search_attribute_value: Value to find

        Returns:
            The first matching Song, or None
        """
        
        search_attribute = search_attribute.lower().strip()
        search_attribute_value = search_attribute_value.lower().strip()
        
        if search_attribute == "index":
            try:
                index = int(search_attribute_value) - 1
                
                if 0 <= index < len(self._songs):
                    return self._songs[index]
                
            except ValueError:
                return None
            
            return None
        
        for song in self._songs:
            attribute_value = song.get_attribute_string_value(search_attribute)
            
            if attribute_value.lower() == search_attribute_value.lower():
                return song
        
        return None

    def perform_add_song(self, new_song: Song) -> None:
        """
        Append a song to the library

        Args:
            new_song: Song object to add
        """
        self._songs.append(new_song)

    def perform_remove_song(self, index_to_remove: int) -> None:
        """
        Remove the song at a specified index

        Args:
            index_to_remove: Position of the song to remove
        """
        
        if 0 <= index_to_remove < len(self._songs):
            self._songs.pop(index_to_remove)
        else:
            print("Invalid song index")
            

    def perform_edit_song(
        self, index_to_edit: int, attribute: str, new_attribute_value: str) -> None:
        """
        Update an attribute of a song at a specified index

        Args:
            index_to_edit: Position of the song to edit
            attribute: Attribute to update
            new_attribute_value: Replacement value
        """
        
        if 0 <= index_to_edit < len(self._songs):
            self._songs[index_to_edit].set_attribute_value(attribute, new_attribute_value)
        else:
            print("Invalid song index")

    def get_song_index(self, song: Song) -> int:
        """
        Find a song by object identity

        Args:
            song: Song object to locate

        Returns:
            Its index, or -1 if the same object is not present
        """
        
        for index, library_song in enumerate(self._songs):
            if library_song is song:
                return index
            
        return -1