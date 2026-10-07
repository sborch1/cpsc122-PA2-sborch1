from song_library import Song, SongLibrary

def display_menu() -> None:
    """Display the music manager menu"""
    
    print("\nMusic Library Manager")
    print()
    print("1. Display songs")
    print("2. Load songs from file")
    print("3. Save songs to file")
    print("4. Sort songs")
    print("5. Search for a song")
    print("6. Play a song")
    print("7. Add a song")
    print("8. Remove a song")
    print("9. Edit a song")
    print("10. Quit")


def get_integer(prompt: str) -> int:
    """
    Get an integer from the user

    Args:
        prompt: Message displayed to the user

    Returns:
        The integer entered by the user
    """
    
    while True:
        try:
            return int(input(prompt))
        
        except ValueError:
            
            print("Enter a valid integer")


def display_songs(library: SongLibrary) -> None:
    """
    Display all songs in the library

    Args:
        library: The music library to display
    """
    
    if not library._songs:
        print("The music library is empty")
    else:
        print("\n" + str(library))


def load_songs(library: SongLibrary) -> None:
    """
    Load songs from a file

    Args:
        library: The music library to update
    """
    filename = input("Enter filename to load: ")
    library.perform_load(filename)
    print("File loaded")


def save_songs(library: SongLibrary) -> None:
    """
    Save songs to a file

    Args:
        library: The music library to save
    """
    filename = input("Enter filename to save to: ")
    library.perform_save(filename)
    print("File saved")


def sort_songs(library: SongLibrary) -> None:
    """
    Sort songs by a selected attribute

    Args:
        library: The music library to sort
    """
    print("\nSort by:")
    print("1. Title")
    print("2. Artist")
    print("3. Genre")
    print("4. Rating")

    choice = get_integer("Choose a sorting option: ")

    attributes = {1: "title", 2: "artist", 3: "genre", 4: "rating"}

    if choice in attributes:
        library.perform_sort(attributes[choice])
        print(f"Songs sorted by {attributes[choice]}")
        display_songs(library)
    else:
        print("Invalid sorting option")


def search_song(library: SongLibrary) -> Song | None:
    """
    Search for a song using one of its attributes

    Args:
        library: The music library to search

    Returns:
        The matching Song, or None if no match is found
    """
    print("\nSearch by:")
    print("1. Title")
    print("2. Artist")
    print("3. Genre")
    print("4. Rating")

    choice = get_integer("Choose a search option: ")

    attributes = {1: "title", 2: "artist", 3: "genre", 4: "rating"}

    if choice not in attributes:
        print("Invalid search option")
        return None

    attribute = attributes[choice]
    value = input(f"Enter the {attribute} to search for: ")

    song = library.perform_search(attribute, value.lower())

    if song is None:
        print("No matching song was found")
    else:
        print("Song found:")
        print(song)

    return song


def play_song(library: SongLibrary) -> None:
    """
    Find a song by title and attempt to play its clip

    Args:
        library: The music library to search
    """
    title = input("Enter the song title to play: ")
    song = library.perform_search("title", title.lower())

    if song is None:
        print("No matching song was found.")
    else:
        song.play_clip()


def add_song(library: SongLibrary) -> None:
    """
    Ask the user for song information and add the song.

    Args:
        library: The music library to update.
    """
    print("Enter the song information.")
    title = input("Title: ").strip()
    artist = input("Artist: ").strip()
    genre = input("Genre: ").strip()
    clip = input("Path to audio clip: ").strip()

    while True:
        rating = get_integer("Rating (1-5): ")
        if Song.MIN_RATING <= rating <= Song.MAX_RATING:
            break
        print("Rating must be between 1 and 5.")

    new_song = Song(title, artist, genre, clip, rating)
    library.perform_add_song(new_song)

    print("Song added")


def remove_song(library: SongLibrary) -> None:
    """
    Remove a song using its displayed position

    Args:
        library: The music library to update
    """
    if not library._songs:
        print("The music library is empty")
        return

    display_songs(library)
    position = get_integer("Enter the song number to remove: ")

    if 1 <= position <= len(library._songs):
        library.perform_remove_song(position - 1)
        print("Song removed")
    else:
        print("Invalid song number")


def edit_song(library: SongLibrary) -> None:
    """
    Edit an attribute of a selected song

    Args:
        library: The music library to update
    """
    if not library._songs:
        print("The music library is empty")
        return

    display_songs(library)
    position = get_integer("Enter the song number to edit: ")

    if not 1 <= position <= len(library._songs):
        print("Invalid song number")
        return

    print("\nAttribute to edit:")
    print("1. Title")
    print("2. Artist")
    print("3. Genre")
    print("4. Clip path")
    print("5. Rating")

    choice = get_integer("Choose an attribute: ")

    attributes = {1: "title", 2: "artist", 3: "genre", 4: "clip", 5: "rating"}

    if choice not in attributes:
        print("Invalid attribute option")
        return

    attribute = attributes[choice]
    new_value = input(f"Enter the new {attribute}: ")

    if attribute == "rating":
        try:
            rating = int(new_value)
        except ValueError:
            print("Rating must be an integer from 1 to 5")
            return

        if not Song.MIN_RATING <= rating <= Song.MAX_RATING:
            print("Rating must be between 1 and 5")
            return

    library.perform_edit_song(position - 1, attribute, new_value)
    print("Song updated")


def main() -> None:
    """Run the music library manager"""
    library = SongLibrary()

    while True:
        display_menu()
        choice = get_integer("Enter your choice: ")

        if choice == 1:
            display_songs(library)
        elif choice == 2:
            load_songs(library)
        elif choice == 3:
            save_songs(library)
        elif choice == 4:
            sort_songs(library)
        elif choice == 5:
            search_song(library)
        elif choice == 6:
            play_song(library)
        elif choice == 7:
            add_song(library)
        elif choice == 8:
            remove_song(library)
        elif choice == 9:
            edit_song(library)
        elif choice == 10:
            print("Exiting...")
            break
        else:
            print("Invalid choice, choose 1-10")


if __name__ == "__main__":
    main()