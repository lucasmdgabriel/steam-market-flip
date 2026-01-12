
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
    item_str = get_item_data(item)

    heh = check_item_market_data(item_str)

    print(heh)

    exit()