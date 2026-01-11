
import pyautogui
import json
import time
from scripts.items import check_item

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
    check_item(item, account_name)

    exit()