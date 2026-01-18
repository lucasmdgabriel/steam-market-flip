import json
import time

import pyautogui
import pyperclip

with open('new_items.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
new_items = data["new_items"]

with open('data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
old_items = data["items"]

old_urls = []
for item in old_items:
    old_urls.append(item["url"])

new = ""
while new != "s":
    new = input("Novo item: ")

    if new in new_items:
        print("Item já inserido na lista de novos itens.")
    elif new in old_urls:
        print("Item já inserido na lista de itens.")
    elif new != "s":
        new_items.append(new)

with open("new_items.json", "w", encoding="utf-8") as f:
    json.dump({"new_items": new_items}, f, ensure_ascii=False, indent=4)

# Minimizar VS Code
pyautogui.moveTo(1805, 15)
pyautogui.click()
time.sleep(0.1)

for new_item in new_items:
    # Clicar na url
    pyautogui.moveTo(1410, 70)
    pyautogui.click()

    # Cola link do item
    pyperclip.copy(new_item)
    pyautogui.hotkey("ctrl", "v")
    time.sleep(0.1)

    pyautogui.press("enter")
    time.sleep(2.5)

    pyautogui.moveTo(980, 424)
    for _ in range(3):
        pyautogui.click()

    pyautogui.hotkey("ctrl", "c")
    time.sleep(0.1)

    old_items.append({
        "name": pyperclip.paste().replace("\r\n", ""),
        "url": new_item,
        "buy_value": 0.0,
        "sale_value": 0.0,
        "buyed_value": 0.0,
        "status": "waiting_buy_oportunity",
        "buying_countdown": {},
        "sale_tries": 0
    })

with open("data.json", "w", encoding="utf-8") as f:
    json.dump({"items": old_items, "buy_and_sell": data["buy_and_sell"]}, f, ensure_ascii=False, indent=4)