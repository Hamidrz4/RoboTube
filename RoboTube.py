from pytube import Playlist, YouTube,exceptions

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
    try:
        st = vid.streams.get_by_itag(22)  # Update the itag based on the desired stream
        if st is not None:
            print("Video:", vid.title)
            print("File size:", st.filesize / (1024 * 1024), "MB")
            download_choice = input("Do you want to download this video? (yes/no): ")
            if download_choice.lower() == "yes":
                print("Downloading...")
                st.download(output_path=sp)
                print(f"Downloaded {vid.title}")
            else:
                print("Download canceled.")
        else:
            print(f"No stream available for {vid.title}")
    except exceptions.AgeRestrictedError:
        print("The video is age restricted and can't be downloaded without logging in.")


def download_playlist(playlist_link, quality, sp):
    p = Playlist(playlist_link)
    print(f'Downloading: {p.title}')

    for video in p.videos:
        st = video.streams.filter(res=quality).first()
        if st is not None:
            print("Downloading:", video.title)
            st.download(sp)
            print(f"Downloaded {video.title} in {quality}.")

            if video.captions:
                download_caption(video, sp)
        else:
            print(f"No {quality} stream available for {video.title}.")
            n += 1

def download_audio(audio_link, sp):
    audio = YouTube(audio_link)
    st = audio.streams.get_by_itag(251)
    if st is not None:
        print("Audio:", audio.title)
        print("File size:", st.filesize / (1024 * 1024), "MB")  # Convert bytes to MB
        download_choice = input("Do you want to download this audio? (yes/no): ")
        if download_choice.lower() == "yes":
            print("Downloading...")
            st.download(output_path=sp)
            print(f"Downloaded {audio.title}")
        else:
            print("Download canceled.")
    else:
        print(f"No stream available for {audio.title}")

def download_caption(video, sp):
    print("Available caption tracks:")
    for caption in video.captions:
        print(f"{caption.code}: {caption.name}")

    caption_code = input("Enter the caption track code to download: ")
    selected_caption = None

    for caption in video.captions:
        if caption_code in caption.code:
            selected_caption = caption
            break

    if selected_caption:
        print(f"Downloading caption track '{selected_caption.name}'...")
        caption_text = selected_caption.xml_captions
        with open(f"{sp}/{video.title}_{selected_caption.code}.xml", "w", encoding="utf-8") as caption_file:
            caption_file.write(caption_text)
        print(f"Caption track '{selected_caption.name}' downloaded in XML format.")
    else:
        print("Invalid caption track code.")

def main():
    paths = load_paths_from_file()
    if not paths:
        print("No paths found. Please add at least one path.")
        exit()

    sp = select_path(paths)

    while True:
        user_input = input("Enter 'video', 'playlist', 'audio', 'caption' to continue, or 'exit' to quit: ").lower()

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

        elif user_input == 'caption':
            print("Caption Mode:")
            video_link = input("Paste Your Video Link: ")
            vid = YouTube(video_link)
            if vid.captions:
                download_caption(vid, sp)
            else:
                print("No captions available for this video.")

        else:
            print("Invalid input. Please enter 'video', 'playlist', 'audio', 'caption', or 'exit'.")

if __name__ == "__main__":
    main()





