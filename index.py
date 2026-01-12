
import pyautogui
import json
import time
from scripts.items import get_item_data, check_item_market_data

account_name = "nash"
steam_wallet = 20.06

# Abrir itens
with open('data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
items = data["items"]

# Minimizar VS Code
pyautogui.moveTo(1780, 20)
pyautogui.click()
time.sleep(0.1)

new_items = []

for item in items:
    item_status = item["status"]

    item_str = get_item_data(item)

    item_market_data = check_item_market_data(item_str)

    print(item_market_data)
    print(item)

    sell_price = item_market_data["buy"][0]["price"] - 0.01
    buy_price = item_market_data["sell"][0]["price"] - 0.01

    print(sell_price)
    print(buy_price)

    if "buying" in item_status or item_status == []:
        profit = (sell_price * 0.85) - buy_price

        print(profit)

        worth_it = False


    exit()