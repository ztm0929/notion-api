import requests
import json
import html
from dotenv import load_dotenv
import os

load_dotenv()

with open('notion-youtube/test_videos_info.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

NOTION_API_KEY = os.environ.get('Notion_API_KEY')

database_id = '510240d82a91474f92b6592a0509d969'

headers = {
    'Authorization': f'Bearer {NOTION_API_KEY}',
    'Content-Type': 'application/json',
    'Notion-Version': '2022-06-28'
}

for item in data.get('items', []):
    payload = {
        'parent': {
            'database_id': database_id
        },
        'properties': {
            "Video Title": {
                'title': [
                    {
                        'text': {
                            'content': html.unescape(item.get('snippet', {}).get('title', ''))
                        }
                    }
                ]
            },
            "Thumbnail": {
                'files': [
                    {
                        'name': "cover",
                        'external': {
                            'url': item.get('snippet').get('thumbnails').get('high', 'default').get('url')
                        }
                    }
                ]
            },
            "Video ID": {
                'rich_text':[
                    {
                        'type': 'text',
                        'text': {
                            'content': item.get('id').get('videoId', ''),
                            'link': None
                        },
                        'annotations': {
                            'bold': False,
                            'italic': False,
                            'strikethrough': False,
                            'underline': False,
                            'code': False,
                            'color': 'default'
                        },
                        'plain_text': item.get('id').get('videoId', ''),
                        'href': 'https://youtube.'
                    }
                ]
            },
            "Publish Time (UTC+0)": {
                'date': {
                    'start': item.get('snippet').get('publishTime'),
                    'end': None
                }
            }
        }
    }

    response = requests.post(f'https://api.notion.com/v1/pages', headers=headers, json=payload)
    if response.status_code == 200:
        print(f"Successfully added {item.get('name')} to the database.")
    else:
        print(f"Failed to add {item.get('name')} to the database. Error: {response.text}")
