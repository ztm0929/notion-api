import requests
import json
import datetime
from dotenv import load_dotenv
import os

# 从环境变量提取需要用到的API KEY，ExchangeRate的用于获取最新汇率，Notion的用于查询要更新的页面page_id以及更新
load_dotenv()
ExchangeRate_API_KEY = os.environ.get('Exchange_API_KEY')
NOtion_API_KEY       = os.environ.get('Notion_API_KEY')

base_currency = ''

# 基本配置信息：ExchangeRate请求URL（GET方法）、Notion查询URL（POST方法）和更新URL（PATCH方法）
config = {
    "exchangerate_standard_endpoint_url": f'https://v6.exchangerate-api.com/v6/{ExchangeRate_API_KEY}/latest/{base_currency}',
    "NOTION_API_URL": "https://api.notion.com/v1/pages/{page_id}",
    "NOTION_VERSION": "2022-06-28",
    "PAGE_IDS": PAGES
}

# 定义获取获取指定基础货币汇率的函数
def fetch_exchange_rate(base_currency: str) -> dict:
    # 定义基础 URL
    exchangerate_standard_endpoint_url = f'https://v6.exchangerate-api.com/v6/{ExchangeRate_API_KEY}/latest/{base_currency}'
    response = requests.get(exchangerate_standard_endpoint_url)
    response.raise_for_status()
    return response.json()

# 将数据保存为 JSON 文件
def save_to_file(data: dict, filename: str) -> None:
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)



#
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



with open('exchangerate/page_id.json', 'r') as file:
    PAGES = json.load(file)


def custom_round(number):
    # 将数字转为字符串
    num_str = str(number)
    
    # 如果数字小于1
    if number < 1:
        # 查找小数点后第一个非零数字的位置
        decimal_position = num_str.index('.')
        for i in range(decimal_position + 1, len(num_str)):
            if num_str[i] != '0':
                # 将数字四舍五入到第一个非零数字之后的1位
                return round(number, i - decimal_position + 1)
    
    # 如果数字大于或等于1，将其四舍五入到2位小数
    return round(number, 2)




# 更新 Notion 页面的汇率
def update_notion_page(currency: str, rate: float) -> None:
    notion_page_url = config["NOTION_API_URL"].format(page_id=config["PAGE_IDS"][currency])
    headers = {
        "Authorization": "Bearer " + config['API_KEY'],
        "Notion-Version": config["NOTION_VERSION"],
        "Content-Type": "application/json"
    }
    payload = {
        "properties": {
            "Exchange Rate to CNY": rate
        }
    }
    response_notion = requests.patch(notion_page_url, headers=headers, json=payload)
    response_notion.raise_for_status()

# 主函数
def main_optimized():
    exchange_data = fetch_exchange_rate("CNY")
    save_to_file(exchange_data, 'exchangerate/ExchangeRate.json')
    rates_to_update = {
        currency: custom_round(1 / exchange_data['conversion_rates'].get(currency))
        for currency in config["PAGE_IDS"].keys()
        if exchange_data['conversion_rates'].get(currency) is not None
    }
    for currency, rate in rates_to_update.items():
        print(f"{currency} 对 CNY 的汇率是 {rate}")
        update_notion_page(currency, rate)
    with open('exchangerate/execution.log', 'a') as log_file:
        log_file.write(f"Execution time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Notion 页面已更新\n")
    os.system("osascript -e 'display notification \"Notion 页面已更新\" with title \"任务完成\"'")
    print("Notion 页面已更新")
    

# 当脚本作为主程序运行时执行主函数
if __name__ == "__main__":
    main_optimized()
