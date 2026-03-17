import requests

import os
from dotenv import load_dotenv
import json
from datetime import datetime
load_dotenv()
API_KEY = os.getenv("API_KEY")
CHANNEL_HANDLE = "MrBeast"

max_results = 50


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
    


def get_video_ids(playlist_id):

    video_ids = []


    base_url = f"https://youtube.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults={max_results}&playlistId={playlist_id}&key={API_KEY}"
    pageToken = None
    try:

        while True:

            url = base_url
            if pageToken:
                url += f"&pageToken={pageToken}"
            
            response = requests.get(url)
            response.raise_for_status()  # Check if the request was successful

            data = response.json()

            for item in data.get('items', []):
                video_id = item['contentDetails']['videoId']
                video_ids.append(video_id)

            pageToken = data.get('nextPageToken')
            if not pageToken:
                break

        return video_ids

    except Exception as e:
        raise Exception(f"An error occurred while fetching video IDs: {str(e)}")



def extract_video_data(video_ids):

    extracted_data = []

    def batch_list(video_ids_list, batch_size):
        for i in range(0, len(video_ids_list), batch_size):
            yield video_ids_list[i:i + batch_size]
    
    try:
        
        for batch in batch_list(video_ids, max_results):
            video_ids_str = ",".join(batch)
            url = f"https://youtube.googleapis.com/youtube/v3/videos?part=contentDetails&part=snippet&part=statistics&id={video_ids_str}&key={API_KEY}"

            response = requests.get(url)
            response.raise_for_status()  # Check if the request was successful
            data = response.json()

            for item in data.get('items', []):
                video_id = item['id']
                snippet = item['snippet']
                contentDetails = item['contentDetails']
                statistics = item['statistics']


                video_data = {
                    "video_id": video_id,
                    "title": snippet.get('title'),
                    "publishedAt": snippet.get('publishedAt'),
                    "duration": contentDetails.get('duration'),
                    "viewCount": statistics.get('viewCount', None),
                    "likeCount": statistics.get('likeCount', None),
                    "commentCount": statistics.get('commentCount', None)
                }

                extracted_data.append(video_data)
        return extracted_data
    except requests.exceptions.RequestException as e:
        raise Exception(f"An error occurred while fetching video data: {str(e)}")


def save_to_json(extracted_data):
    file_path = f"./data/YT_data_{datetime.today().strftime('%d-%m-%Y')}.json"

    with open(file_path, 'w', encoding='utf-8') as json_file:
        json.dump(extracted_data, json_file, indent=4, ensure_ascii=False)



if __name__ == "__main__":
  playlistId = get_playlist_id()

  video_ids = get_video_ids(playlistId)
  video_data = extract_video_data(video_ids)
  save_to_json(video_data)