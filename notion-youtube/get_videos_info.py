import requests
from dotenv import load_dotenv
import os
import json

load_dotenv()

YouTube_API_KEY = os.environ.get('YouTube_API_KEY')
CHANNEL_ID = 'UC0d16AioQ0z-RzwAae3g08Q'
MAX_RESULTS = 50
next_page_token = None

search_url = f'https://www.googleapis.com/youtube/v3/search?key={YouTube_API_KEY}&channelId={CHANNEL_ID}&order=date&part=snippet&type=video&maxResults={MAX_RESULTS}'

all_videos = []

while True:
    url = search_url + (f'&pageToken={next_page_token}' if next_page_token else '')

    response = requests.get(url)
    videos = json.loads(response.text)

    all_videos.extend(videos.get('items', []))
    
    next_page_token = videos.get('nextPageToken')

    if not next_page_token:
        break

with open('notion-youtube/videos_info.json', 'w') as file:
        json.dump(videos, file, ensure_ascii=False, indent=4)

print('json file has been saved!')