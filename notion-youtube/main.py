import requests
from dotenv import load_dotenv
import os
import json

load_dotenv()

YouTube_API_KEY = os.environ.get('YouTube_API_KEY')

search_url = f'https://www.googleapis.com/youtube/v3/search?key={YouTube_API_KEY}&channelId=UC0d16AioQ0z-RzwAae3g08Q&order=date&part=snippet&type=video'

response = requests.get(search_url)
videos = json.loads(response.text)

with open('notion-youtube/videos_info.json', 'w') as file:
    json.dump(videos, file, ensure_ascii=False, indent=4)

print('json file has been saved!')