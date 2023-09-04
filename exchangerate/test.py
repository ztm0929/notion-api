import requests
from dotenv import load_dotenv
import os

# 加载 .env 文件以设置环境变量
load_dotenv()

# 从环境变量中获取 API 密钥
ExchangeRate_API_KEY = os.environ.get('ExchangeRate_API_KEY')

def fetch_exchange_rate(base_currency: str) -> dict:
    # 定义基础 URL
    exchangerate_standard_endpoint_url = f'https://v6.exchangerate-api.com/v6/{ExchangeRate_API_KEY}/latest/{base_currency}'
    response = requests.get(exchangerate_standard_endpoint_url)
    response.raise_for_status()
    return response.json()

# 获取汇率并打印
exchange_rate_data = fetch_exchange_rate('CNY')
print(exchange_rate_data)
