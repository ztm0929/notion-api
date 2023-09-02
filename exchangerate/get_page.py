import requests
import json

def get_all_pages_from_notion(base_url, headers, payload):
    all_results = []
    start_cursor = None

    while True:
        if start_cursor:
            payload['start_cursor'] = start_cursor

        response = requests.post(base_url, headers=headers, json=payload).json()

        all_results.extend(response['results'])

        if response.get('has_more'):
            start_cursor = response['next_cursor']
        else:
            break

    return all_results

def extract_mappings_from_urls(urls):
    """从给定的 URL 列表中提取所需的键值对格式。"""
    url_mappings = {}
    for url in urls:
        parts = url.split('/')
        if len(parts) >= 1:
            last_part = parts[-1]
            key, value = last_part.split('-')
            url_mappings[key] = value

    return url_mappings

# Existing configuration and payload
base_url = 'https://api.notion.com/v1/databases/dcd97c6fd1c7490ab5893b653c3907c5/query'
headers = {
    "Authorization": "Bearer secret_ORwyPwlsnaxoqLxrJRKA36ckCRVtq3rZBL6kQISRPoS",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}
payload = {
    "filter": {
        "property": "Exchange Rate to CNY",
        "number": {
            "is_not_empty": True
        }
    }
}

# Call the new function to fetch all results
all_pages = get_all_pages_from_notion(base_url, headers, payload)

# Extract URLs from all pages
notion_urls = [page["url"] for page in all_pages if "url" in page and page["url"] is not None]

# Extract mappings from URLs
mappings = extract_mappings_from_urls(notion_urls)

# Save the mappings to a JSON file
with open('exchangerate/page_id.json', 'w') as file:
    json.dump(mappings, file)

print("json file has been saved!")
