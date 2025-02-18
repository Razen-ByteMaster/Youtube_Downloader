import os
import yt_dlp
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Replace these with your own values
API_KEY = ""  # Put your own API-KEY
PLAYLIST_ID = ""  # Specify your playlist
DOWNLOAD_FOLDER = r""  # Specify your download folder here

# Ensure the download directory exists
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)


def get_playlist_items(youtube, playlist_id):
    playlist_items = []
    request = youtube.playlistItems().list(
        part="snippet", playlistId=playlist_id, maxResults=50  # Adjust if necessary
    )
    while request:
        try:
            response = request.execute()
            for item in response["items"]:
                video_id = item["snippet"]["resourceId"]["videoId"]
                video_title = item["snippet"]["title"]
                playlist_items.append((video_id, video_title))
            request = youtube.playlistItems().list_next(request, response)
        except HttpError as e:
            print(f"An error occurred: {e}")
            break
    return playlist_items


def download_video(video_id, download_folder):
    ydl_opts = {
        "format": "bestvideo+bestaudio",
        "postprocessors": [
            {
                "key": "FFmpegVideoConvertor",
                "preferedformat": "mp4",
            }
        ],
        "outtmpl": os.path.join(download_folder, "%(title)s.%(ext)s"),
    }
    url = f"https://www.youtube.com/watch?v={video_id}"
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except Exception as e:
        print(f"Failed to download video {video_id}: {e}")


def main():
    youtube = build("youtube", "v3", developerKey=API_KEY)

    # Get playlist videos
    items = get_playlist_items(youtube, PLAYLIST_ID)

    # Download each video
    for video_id, title in items:
        print(f"Downloading: {title}")
        download_video(video_id, DOWNLOAD_FOLDER)


if __name__ == "__main__":
    main()
