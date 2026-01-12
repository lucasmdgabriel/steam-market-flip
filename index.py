import pyautogui
import pyperclip
import json
import time
from scripts.items import get_item_data, check_item_market_data
from scripts.buy import buy_action
from datetime import datetime
from decimal import Decimal, ROUND_DOWN

now = datetime.now()
year   = now.year
month  = now.month
day    = now.day
hour   = now.hour
minute = now.minute



account_name = "nash"
steam_wallet = 20.06

# Abrir itens
with open('data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
items = data["items"]

# Minimizar VS Code
pyautogui.moveTo(1780, 20) # NOTEBOOK
pyautogui.moveTo(1805, 15) # PC
pyautogui.click()
time.sleep(0.1)

# # Clicar na url
# pyautogui.moveTo(1410, 70) # NOTEBOOK
# pyautogui.moveTo(1570, 50) # PC
# pyautogui.click()

# # Cola link da steam
# pyperclip.copy("https://steamcommunity.com/")
# pyautogui.hotkey("ctrl", "v")
# time.sleep(0.1)

# pyautogui.press("enter")
# time.sleep(2)

# for i in range(7):
#     pyautogui.hotkey("ctrl", "-")
#     time.sleep(0.1)

new_items = []


def cancel_buy(item_status):
    if "buying" in item_status and "selling" in item_status:
        print("cancelando compra em baixo...")
    elif "buying" in item_status:
        print("cancelando compra em cima...")
    else:
        print("ignorando cancelamento de compra")


for item in items:
    item_status = item["status"]

    item_str = get_item_data(item)

    item_market_data = check_item_market_data(item_str)

    print(f"item_market_data: {item_market_data}")
    print(f"item: {item}")

    # buy_price = item_market_data["buy"][0]["price"]
    # sell_price = item_market_data["sell"][0]["price"]

    buy_price = Decimal(str(item_market_data["buy"][0]["price"]))
    sell_price = Decimal(str(item_market_data["sell"][0]["price"]))

    new_buy_price = buy_price - Decimal("0.01")
    new_sell_price = sell_price + Decimal("0.01")

    print(f"buy_price: {buy_price}")
    print(f"sell_price: {sell_price}")
    print(f"new_buy_price: {new_buy_price}")
    print(f"new_sell_price: {new_sell_price}")
    print("")
    

    tax = new_buy_price * Decimal("0.15")
    if tax < 0.1:
        tax -= 0.1

    print(f"tax: {tax}")


    if "buying" in item_status or "buying_countdown" not in item_status:
        profit = (new_buy_price - tax) - sell_price
        profit_rate = profit/sell_price

        if item_market_data["buy_count"] < 1 and "buying" in item_status:
            item_status.remove("buying")
            item_status.append("buying_countdown")
            item["buying_countdown"] = {
                "day": (day + 7, month, year),
                "hour": (hour, minute)
            }

        elif profit < 0.1 or profit_rate < 0.15:
            if "buying" in item_status:
                item_status.remove("buying")

            cancel_buy(item_status)
            item["buy_value"] = 0.0

        elif sell_price != item["buy_value"]:
            if "buying" not in item_status:
                item_status.append("buying")

            cancel_buy(item_status)
            buy_action(sell_price)
            item["buy_value"] = sell_price

        print(f"profit: {profit}")
        print(f"profit_rate: {profit_rate}")

        worth_it = False

    print(item_status)
    item["status"] = item_status
    print(item)



    exit()