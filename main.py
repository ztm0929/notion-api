import requests
import os

# Notion API 的设置
NOTION_API_KEY = os.environ.get('Notion_API_KEY')
NOTION_API_ENDPOINT = "https://api.notion.com/v1/pages"
NOTION_PARENT_PAGE_ID = '37c9da3125db4edfa7579415a521bffd'

# 下载图片
IMAGE_URL = 'https://2kdb.net/storage/players/23/r.j._barrett_63075.jpg'
image_response = requests.get(IMAGE_URL)
image_content = image_response.content

# 使用 Notion API 上传图片
headers = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"  # 可能需要根据Notion文档更新版本号
}

data = {
    "parent": {"type": "page_id", "page_id": NOTION_PARENT_PAGE_ID},
    "properties": {},
    "children": [{
        "object": "block",
        "type": "image",
        "image": {
            "type": "external",
            "external": {
                "url": IMAGE_URL
            }
        }
    }]
}

response = requests.post(NOTION_API_ENDPOINT, headers=headers, json=data)

if response.status_code == 200:
    print("Image uploaded successfully!")
else:
    print(f"Failed to upload image. Response: {response.text}")
