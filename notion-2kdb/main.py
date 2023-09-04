import requests
import json
import os

database_url = 'https://api.notion.com/v1/databases/7c0db327f09945aeb139a666ee0aac2e/query'

headers = {
    "Authorization": f"Bearer {os.environ.get('Notion_API_KEY')}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

# 获取database目前所有的内含页面page_id

response = requests.post(database_url, headers=headers).json()

with open('notion-2kdb/page.json', 'w') as file:
    json.dump(response, file)

page_ids = [id["id"] for id in response["results"]]

for page_id in page_ids:
    print(page_id)

    # 通过获取到的page_id批量更新页面的title属性
    update_page_props_url = f'https://api.notion.com/v1/pages/{page_id}'

    payload = {
        "properties": {
            "Collection": {
                "select": {
                    "name": "Invincible"
                }
            }
        }
    }

    response_update = requests.patch(update_page_props_url, headers=headers, json=payload)

    print(response_update.status_code)