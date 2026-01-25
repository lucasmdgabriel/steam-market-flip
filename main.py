from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import random
import datetime

date_time = datetime.datetime.now()

def aguardar_pagina(driver): # CORRIGIR: ATUALIZAR NOME
    WebDriverWait(driver, 10).until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )

def check_is_in_countdown(): # CORRIGIR: IMPLEMENTAR LÓGICA DA FUNÇÃO
    return random.randrange(2) == 0


def check_is_profitable(offer_value, order_value):
    offer_value -= 0.01
    order_value += 0.01

    offer_value = round(offer_value, 2)
    order_value = round(order_value, 2)

    tax = offer_value * 0.15
    if tax < 0.1:
        tax = 0.1

    billing = round(offer_value - tax, 2)

    print(f"Valor de compra: R${order_value}")
    print(f"Valor de venda: R${offer_value} (recebe R${billing})")

    profit = round(billing - order_value, 2)
    profit_relative = round(profit/order_value, 2)

    print(f"Lucro: {profit} ({profit_relative*100}%)")

    is_profitable = profit > 0.1 and profit_relative >= 0.1

    return is_profitable, offer_value, order_value

driver = webdriver.Chrome()
# # URL de login da Steam
# login_url = "https://store.steampowered.com/login/?redir=&redir_ssl=1"
# driver.get(login_url)

# wait = WebDriverWait(driver, 300)

# try:
#     # Espera a URL mudar
#     wait.until(EC.url_changes(login_url))
    
#     print("Sucesso! Você está logado.")
#     print(f"Página atual: {driver.current_url}")

# except Exception as e:
#     print(f"Tempo de login esgotado: {e}")
#     exit()

# driver.find_element("xpath", "//button[text()='Criar conta']").click()

items = [
    {
        "name": "Splat",
        "url": "https://steamcommunity.com/market/listings/753/282010-Splat",
        "max_items": 3,
        "buy_status": "buying",
        "buying_data": {
            "quant": 5,
            "price": 6.86
        },
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
    
        print("============================================================")
        print(f"= {item_name} [{index}] =")
        
    else:
        iteration += 1
    last_index = index

    collected_offer_value = 17.88 # CORRIGIR: COLETAR
    collected_order_value = 6.87 # CORRIGIR: COLETAR
    collected_quant_buying = 3 # CORRIGIR: COLETAR

    if buy_status == "buying":
        print(f"{iteration}. Comprando*")
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

        


    print(buying_data)
    index += 1



    # driver.get("https://steamcommunity.com/market/listings/753/282010-Splat")
    # aguardar_pagina(driver)

exit()


# ENCONTRAR VALORES DE COMPRA
buy_price_quant = driver.find_elements(By.CLASS_NAME, "market_listing_price")

buy_price = buy_price_quant[0].text.strip().replace("R$ ", "")
buy_quant = buy_price_quant[1].text.strip()

print(f"Preço: {buy_price}")
print(f"Quantidade: {buy_quant}")


input("Pressione Enter para fechar...")
driver.quit()