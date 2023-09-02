import requests
import json

with open('exchangerate/page_id.json', 'r') as file:
    PAGES = json.load(file)

# 配置信息
config = {
    "API_KEY": "secret_ORwyPwlsnaxoqLxrJRKA36ckCRVtq3rZBL6kQISRPoS",
    "EXCHANGE_API_URL": "https://v6.exchangerate-api.com/v6/{api_version}/latest/{base_currency}",
    "NOTION_API_URL": "https://api.notion.com/v1/pages/{page_id}",
    "NOTION_VERSION": "2022-06-28",
    "PAGE_IDS": PAGES
}

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


# 获取指定基础货币的汇率
def fetch_exchange_rate(base_currency: str) -> dict:
    exchange_url = config["EXCHANGE_API_URL"].format(api_version="8c647a751dcfa69079eade22", base_currency=base_currency)
    response = requests.get(exchange_url)
    response.raise_for_status()
    return response.json()

# 将数据保存为 JSON 文件
def save_to_file(data: dict, filename: str) -> None:
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

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
    save_to_file(exchange_data, 'ExchangeRate.json')
    rates_to_update = {
        currency: custom_round(1 / exchange_data['conversion_rates'].get(currency))
        for currency in config["PAGE_IDS"].keys()
        if exchange_data['conversion_rates'].get(currency) is not None
    }
    for currency, rate in rates_to_update.items():
        print(f"{currency} 对 CNY 的汇率是 {rate}")
        update_notion_page(currency, rate)
    print("Notion 页面已更新")

# 当脚本作为主程序运行时执行主函数
if __name__ == "__main__":
    main_optimized()
