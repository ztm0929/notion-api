import requests
import json
import datetime
from dotenv import load_dotenv
import os

# 从环境变量提取需要用到的 API KEY，ExchangeRate 的用于获取最新汇率，Notion 的用于查询要更新的页面 page_id 并进行更新
load_dotenv()
ExchangeRate_API_KEY = os.environ.get('Exchange_API_KEY')
Notion_API_KEY       = os.environ.get('Notion_API_KEY')

print(ExchangeRate_API_KEY)

# def fetch_exchange_rate(base_currency: str) -> dict:
#     # ExchangeRate 标准端点 URL，使用 GET 方法，参见官方文档：https://www.exchangerate-api.com/docs/standard-requests
#     exchangerate_standard_endpoint_url = f'https://v6.exchangerate-api.com/v6/{ExchangeRate_API_KEY}/latest/{base_currency}'
#     response = requests.get(exchangerate_standard_endpoint_url)
#     response.raise_for_status()
#     return response.json()

# exchange_data = fetch_exchange_rate("CNY")