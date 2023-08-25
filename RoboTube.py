from pytube import Playlist, YouTube

def load_paths_from_file():
    paths = []
    try:
        with open("download_paths.txt", "r") as file:
            paths = [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        # Create the file with a default path
        default_path = "default_download_path"
        with open("download_paths.txt", "w") as file:
            file.write(default_path + "\n")
        paths = [default_path]
    return paths


def save_paths_to_file(paths):
    with open("download_paths.txt", "w") as file:
        for path in paths:
            file.write(path + "\n")


def select_path(paths):
    print("Available paths:")
    for i, path in enumerate(paths):
        print(f"{i + 1}. {path}")
    choice = input("Select a path by entering its number (or enter 'new' to add a new path): ")
    if choice.isdigit() and 1 <= int(choice) <= len(paths):
        return paths[int(choice) - 1]
    elif choice.lower() == 'new':
        new_path = input("Enter the new folder path: ")
        paths.append(new_path)
        save_paths_to_file(paths)
        return new_path
    else:
        print("Invalid choice. Using the default path.")
        return paths[0]


def download_video(video_link, sp):
    vid = YouTube(video_link)
    st = vid.streams.get_by_itag(22)
    if st is not None:
        print("Downloading:", vid.title)
        st.download(sp)
        print(f"Downloaded {vid.title}")
    else:
        print(f"No stream available for {vid.title}")

def download_playlist(playlist_link, quality, sp):
    p = Playlist(playlist_link)
    print(f'Downloading: {p.title}')

    for video in p.videos:
        st = video.streams.filter(res=quality).first()
        if st is not None:
            print("Downloading:", video.title)
            st.download(sp)
            print(f"Downloaded {video.title} in {quality}.")
        else:
            print(f"No {quality} stream available for {video.title}.")

def download_audio(audio_link, sp):
    audio = YouTube(audio_link)
    st = audio.streams.get_by_itag(251)
    if st is not None:
        print("Downloading:", audio.title)
        st.download(sp)
        print(f"Downloaded {audio.title}")
    else:
        print(f"No stream available for {audio.title}")

def main():
    paths = load_paths_from_file()
    if not paths:
        print("No paths found. Please add at least one path.")
        exit()

    sp = select_path(paths)

    while True:
        user_input = input("Enter 'video' or 'playlist' or 'audio' to continue, or 'exit' to quit: ").lower()

        if user_input == 'exit':
            print("Exiting the program.")
            break

        elif user_input == 'video':
            print("Video Mode:")
            video_link = input("Paste Your Video Link: ")
            download_video(video_link, sp)

        elif user_input == 'playlist':
            print("Playlist Mode:")
            playlist_link = input("Paste Your Playlist Link: ")
            quality = input("What's Your Preferable Quality? ")
            download_playlist(playlist_link, quality, sp)

        elif user_input == 'audio':
            print("Audio Mode:")
            audio_link = input("Paste Your Audio Link: ")
            download_audio(audio_link, sp)

        else:
            print("Invalid input. Please enter 'video' or 'playlist' or 'audio' or 'exit'.")

if __name__ == "__main__":
    main()




