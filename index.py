
from scripts.player import show
import pyautogui
import json

show("34534", "543543")

steam_wallet = 20.06

# Abrir itens
with open('data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
items = data["items"]

# Minimizar VS Code
pyautogui.moveTo(1780, 20)
#pyautogui.click()

new_items = []

for item in items:
    print(item)