import requests

import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")
CHANNEL_HANDLE = "MrBeast"


def get_playlist_id():

    try:

        url = "https://youtube.googleapis.com/youtube/v3/channels"

        params = {
            "part": "contentDetails",
            "forHandle": CHANNEL_HANDLE,
            "key": API_KEY
        }

        response = requests.get(url, params=params)

        response.raise_for_status()  # Check if the request was successful

        data = response.json()

        channel_items = data['items'][0]  # Assuming the first item is the desired channel
        channel_playlistsId = channel_items['contentDetails']['relatedPlaylists']['uploads']

        #print(f"Channel Playlists ID: {channel_playlistsId}")
        return channel_playlistsId
    
    except Exception as e:

        raise Exception(f"An error occurred while fetching the playlist ID: {str(e)}")
    
    
if __name__ == "__main__":
   get_playlist_id()