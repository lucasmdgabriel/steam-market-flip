import pyautogui
import pyperclip
import json
import time
from datetime import datetime
from decimal import Decimal
from scripts.items import get_item_data, check_item_market_data
from scripts.buy import buy_action, sell_action
from scripts.cancel import cancel_action_buy, cancel_action_sell
import random

now = datetime.now()
year   = now.year
month  = now.month
day    = now.day
hour   = now.hour
minute = now.minute


account_name = "nash"
steam_wallet = float(input("Digite o valor atual da carteira: "))
buy_limit = steam_wallet * 10
sales_tries_before_take_a_loss = 6

print(f"Limite de compra: {buy_limit}")

# Abrir itens
with open('data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
items = data["items"]
buy_and_sell = data["buy_and_sell"]

random.shuffle(items)

for i in range(len(items)):
    items[i]["index"] = i

total_buying = 0
for item in items:
    if item["status"] == "buying":
        total_buying += item["buy_value"]
print(f"Compras totais: {total_buying}")
print(f"Número de itens: {len(items)}")
input("")

# Minimizar VS Code
pyautogui.moveTo(1805, 15)
pyautogui.click()
time.sleep(0.1)

def cancel_buy(item_status, value, total_buying):
    if item_status == "buying":
        total_buying = cancel_action_buy(value, total_buying)

    return total_buying

def cancel_sell(item_status):
    if item_status == "selling":
        cancel_action_sell()

def check_countdown(buying_countdown):
    print(buying_countdown)
    if (buying_countdown["year"] < year):
        return False
    elif (buying_countdown["year"] > year):
        return True
    
    if (buying_countdown["month"] < month):
        return False
    elif (buying_countdown["month"] > month):
        return True
    
    if (buying_countdown["day"] < day):
        return False
    elif (buying_countdown["day"] > day):
        return True
    
    if (buying_countdown["hour"] < hour):
        return False
    elif (buying_countdown["hour"] > hour):
        return True
    
    if (buying_countdown["minute"] < minute):
        return False
    elif (buying_countdown["minute"] > minute):
        return True
    
    return True


    
new_items = []
index = -1
first_item = True
for item in items:
    index += 1

    item_str = get_item_data(item)

    item_market_data = check_item_market_data(item_str, first_item)
    first_item = False

    print("===================")
    print(f" = {item["name"]} = ")

    print(f"item_market_data: {item_market_data}")
    print(f"item: {item}")

    buy_price = Decimal(str(item_market_data["buy"][0]["price"]))
    sell_price = Decimal(str(item_market_data["sell"][0]["price"]))

    new_buy_price = buy_price - Decimal("0.01")
    new_sell_price = sell_price + Decimal("0.01")

    if new_sell_price < 0.15:
        new_sell_price = Decimal(0.15)

    print(f"buy_price: {buy_price}")
    print(f"sell_price: {sell_price}")
    print(f"new_buy_price: {new_buy_price}")
    print(f"new_sell_price: {new_sell_price}")
    print("")
    

    tax = new_buy_price * Decimal("0.15")
    if tax < 0.1:
        tax = Decimal("0.1")

    print(f"tax: {tax}")


    if item["status"] == "buying" or item["status"] == "waiting_buy_oportunity":
        profit = (new_buy_price - tax) - new_sell_price
        profit_rate = profit/new_sell_price

        print(f"profit: {profit}")
        print(f"profit_rate: {profit_rate}")

        item["buy_value"] = Decimal(str(item["buy_value"])).quantize(Decimal("0.00"))

        if item_market_data["buy_count"] < 1 and item["status"] == "buying":
            item["status"] = "buying_countdown"
            item["buyed_value"] = item["buy_value"]
            item["buy_value"] = 0.0
            
            item["buying_countdown"] = {
                "day": day + 7,
                "month": month,
                "year": year,
                "hour": 5,
                "minute": 0
            }

        elif (profit < 0.1 or profit_rate < 0.10):
            total_buying = cancel_buy(item["status"], item["buy_value"], total_buying)
            item["status"] = "waiting_buy_oportunity"
            item["buy_value"] = 0.0

        elif sell_price != item["buy_value"]:
            item["status"] = "buying"

            total_buying = cancel_buy(item["status"], item["buy_value"], total_buying)

            is_buy, total_buying, value = buy_action(new_sell_price, steam_wallet, buy_limit, total_buying)
            item["buy_value"] = new_sell_price

            if is_buy == False:
               item["status"] = "waiting_buy_oportunity"
               item["buy_value"] = 0.0

    elif item["status"] == "buying_countdown":
        in_countdown = check_countdown(item["buying_countdown"])

        if not in_countdown:
            item["status"] = "waiting_sale_oportunity"
            item["buying_countdown"] = {}
            item["sale_tries"] = 0

    if item["status"] in ["selling", "waiting_sale_oportunity"]:
        profit = new_buy_price - Decimal(item["buyed_value"])
        
        profit_rate = 0

        if item["buyed_value"] != 0:
            profit_rate = profit/Decimal(item["buyed_value"])

        print(f"buyed_value: {item["buyed_value"]}")
        print(f"profit: {profit}")
        print(f"profit_rate: {profit_rate}")

        if item_market_data["sales_count"] < 1 and item["status"] == "selling":
            sold_item = {
                "Name": item["name"],
                "url": item["url"],
                "buy_price": float(item["buyed_value"]),
                "sell_price": float(item["sale_value"]),
                "tax": float(item["sale_value"]) * 0.15,
                "profit": float(Decimal(item["sale_value"]) - Decimal(item["buyed_value"])) - float(item["sale_value"]) * 0.15,
            }

            buy_and_sell.append(sold_item)

            item["status"] = "waiting_buy_oportunity"
            item["buy_value"] = "0.0"
            item["buyed_value"] = "0.0"
            item["sale_value"] = "0.0"

        elif (profit < -0.03 or profit_rate < -0.05) and item["sale_tries"] < sales_tries_before_take_a_loss:
            cancel_sell(item["status"])
            item["status"] = "waiting_sale_oportunity"
            item["sale_value"] = 0.0
            item["sale_tries"] += 1

        elif Decimal(str(buy_price)) != Decimal(str(item["sale_value"])):
            item["status"] = "selling"
            item["sale_tries"] = 0

            cancel_sell(item["status"])
            item["sale_value"] = new_buy_price

            sell_action(new_buy_price, item["name"])

    item["buy_value"] = float(item["buy_value"])
    item["sale_value"] = float(item["sale_value"])
    item["buyed_value"] = float(item["buyed_value"])
    new_items.append(item)
    print("=====================")

    combined = new_items + items[index+1:]
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump({"items": combined, "buy_and_sell": buy_and_sell}, f, ensure_ascii=False, indent=4)

end = datetime.now()
tempo_execucao = end - now

print(f"Tempo de execução: {tempo_execucao}")
print(f"Compras totais: {total_buying}")
print(f"Número de itens: {len(items)}")