import requests
from dotenv import load_dotenv
import os

# 从环境变量提取需要用到的 API KEY，ExchangeRate 的用于获取最新汇率，Notion 的用于查询要更新的页面 page_id 并进行更新
load_dotenv()
ExchangeRate_API_KEY = os.environ.get('Exchange_API_KEY')
Notion_API_KEY       = os.environ.get('Notion_API_KEY')

# Notion 的请求头
Notion_Headers = {
    'Authorization' : f'Bearer {Notion_API_KEY}',
    'Notion-Version': '2022-06-28',
    'Content-Type'  : 'application/json'
}


# 配置要查询的数据库 ID：database_id，区别于查询后得到的页面 ID：page_id
# Notion 查询数据库 URL，使用 POST 方法，过滤器作为请求体（可选）
# 默认请求大小限制在100条，需要作分页请求处理，前一次响应体中的 next_cursor 直接作为后一次请求体中的 start_cursor，以此循环
# 参见文档：https://developers.notion.com/reference/post-database-query
database_id = os.environ.get('Currency_database_id')
query_database_url = f'https://api.notion.com/v1/databases/{database_id}/query'

# payload = {
#     "filter": {
#         "property": "Exchange Rate to CNY",
#         "number": {
#             "is_not_empty": True
#         }
#     }
# }




#
def get_all_pages_from_notion(query_database_url, Notion_Headers, payload):
    all_results = []
    start_cursor = None

    while True:
        if start_cursor:
            payload['start_cursor'] = start_cursor

        response = requests.post(query_database_url, headers=Notion_Headers).json()

        all_results.extend(response['results'])

        if response.get('has_more'):
            start_cursor = response['next_cursor']
        else:
            break

    return all_results

get_all_pages_from_notion(query_database_url, Notion_Headers)

