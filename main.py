from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import random
import datetime

# VALORES INICIAIS
wallet_value = 100

date_time = datetime.datetime.now()

driver = webdriver.Chrome()
# URL de login da Steam
login_url = "https://store.steampowered.com/login/?redir=&redir_ssl=1"
driver.get(login_url)

wait = WebDriverWait(driver, 300)




def aguardar_pagina(driver): # CORRIGIR: ATUALIZAR NOME
    WebDriverWait(driver, 10).until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )

def check_is_in_countdown(): # CORRIGIR: IMPLEMENTAR LÓGICA DA FUNÇÃO
    return random.randrange(2) == 0

def cancel_item_buy(): # CORRIGIR: IMPLEMENTAR LÓGICA DA FUNÇÃO
    return

def item_buy(value, quant): # CORRIGIR: IMPLEMENTAR LÓGICA DA FUNÇÃO
    print(value, quant)

    buy_button = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[.//span[contains(text(), 'Comprar...')]]")
        )
    )

    buy_button.click()

    exit()
    return

def check_is_profitable(offer_value, order_value):
    offer_value -= 0.01
    order_value += 0.01

    offer_value = round(offer_value, 2)
    order_value = round(order_value, 2)

    tax = offer_value * 0.15
    if tax < 0.1:
        tax = 0.1

    billing = round(offer_value - tax, 2)

    print(f"-- Valor de compra: R${order_value}")
    print(f"-- Valor de venda: R${offer_value} (recebe R${billing})")

    profit = round(billing - order_value, 2)
    profit_relative = round(profit/order_value, 2)

    print(f"-- Lucro: {profit} ({round(profit_relative*100, 2)}%)")

    is_profitable = profit > 0.1 and profit_relative >= 0.1

    return is_profitable, offer_value, order_value



try:
    # Espera a URL mudar
    wait.until(EC.url_changes(login_url))
    
    print("Sucesso! Você está logado.")
    print(f"Página atual: {driver.current_url}")

except Exception as e:
    print(f"Tempo de login esgotado: {e}")
    exit()

items = [
    {
        "name": "Splat",
        "url": "https://steamcommunity.com/market/listings/753/282010-Splat",
        "max_items": 3,
        "buy_status": "buying",
        "buying_data": {
            "quant": 5,
            "price": 1.87
        },
        "sell_data": []
    },
    {
        "name": "Broken Shell (Brilhante)",
        "url": "https://steamcommunity.com/market/listings/753/367520-Broken%20Shell%20%28Foil%29",
        "max_items": 3,
        "buy_status": "waiting_to_buy",
        "buying_data": {},
        "sell_data": []
    }
]

index = 0
last_index = -1
iteration = 0
while index < len(items):
    item_name = items[index]["name"]
    item_url = items[index]["url"]
    buy_status = items[index]["buy_status"]

    if index != last_index:
        iteration = 0
    
        print("")
        print(f"=== {item_name} [{index}] ===")

        driver.get(item_url)
        aguardar_pagina(driver)

        # ENCONTRAR VALORES DE ENCOMENDA E OFERTAS
        sell_price_data = wait.until(
            lambda d: d.find_elements(By.CLASS_NAME, "market_commodity_orders_header_promote")
        )
        collected_offer_value = float(sell_price_data[1].text.replace("R$ ", "").replace(",", "."))
        collected_order_value = float(sell_price_data[3].text.replace("R$ ", "").replace(",", "."))

        # ENCONTRAR VALORES DE COMPRA DO USUÁRIO
        buy_user_price_data = wait.until(
            lambda d: d.find_elements(By.CLASS_NAME, "market_listing_price")
        )
        collected_price_buying = float(buy_user_price_data[0].text.strip().replace("R$ ", "").replace(",", "."))
        collected_quant_buying = int(buy_user_price_data[1].text.strip())

    else:
        iteration += 1
    last_index = index

    if iteration > 0: # apenas separa
        print("=")

    if buy_status == "buying":
        print(f"{iteration}. Comprando *")
        buying_data = items[index]["buying_data"]
        is_profitable, offer_value, order_value = check_is_profitable(collected_offer_value, collected_order_value)

        if buying_data["quant"] > collected_quant_buying:
            diff = buying_data["quant"] - collected_quant_buying

            # ADICIONA ITENS A LISTA DE VENDA
            for _ in range(diff):
                new_sell_data_item = {
                    "buy_price": buying_data["price"],
                    "sell_price": 0.0,
                    "status": "countdown",
                    "countdown": {
                        "day": date_time.day,
                        "month": date_time.month,
                        "year": date_time.year,
                        "hour": 5,
                        "minute": 0
                    }
                }

                items[index]["sell_data"].append(new_sell_data_item)

        # CANCELA COMPRA DE ITEM PARA RECOMPRAR
        if buying_data["price"] != collected_order_value:
            print("- Cancelando compra. Valor mudou.")
            cancel_item_buy()
            
            items[index]["buy_status"] = "waiting_to_buy"
            items[index]["buying_data"] = {}

            index -= 1

    if buy_status == "waiting_to_buy":
        print(f"{iteration}. Checando itens disponíveis para compra *")

        max_items = items[index]["max_items"]
        num_items_to_sell = len(items[index]["sell_data"])

        quant_to_buy = max_items - num_items_to_sell

        if quant_to_buy < 0: quant_to_buy = 0

        print(f"-- Limite de itens: {max_items}")
        print(f"-- Itens sendo vendidos: {num_items_to_sell}")
        print(f"- Desejando comprar {quant_to_buy} item(ns).")

        is_profitable, offer_value, order_value = check_is_profitable(collected_offer_value, collected_order_value)

        if is_profitable == False:
            print(f"-- Lucro não é suficiente. Ignorando compra.")
        elif wallet_value < order_value:
            print(f"-- Dinheiro disponível na carteira (R${wallet_value}) menor do que o valor do item (R${order_value}). Ignorando.")
        else:
            print(f"-- Comprando item por R${order_value}")
            item_buy(order_value, quant_to_buy)
            
    index += 1



exit()
# ENCONTRAR VALORES DE COMPRA
buy_price_quant = driver.find_elements(By.CLASS_NAME, "market_listing_price")

buy_price = buy_price_quant[0].text.strip().replace("R$ ", "")
buy_quant = buy_price_quant[1].text.strip()

print(f"Preço: {buy_price}")
print(f"Quantidade: {buy_quant}")


input("Pressione Enter para fechar...")
driver.quit()