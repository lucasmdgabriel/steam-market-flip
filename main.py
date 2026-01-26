import json
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import random
import datetime

# VALORES INICIAIS
wallet_value = 91.65
buy_limit = wallet_value * 100
user = "boanashi"

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

def check_is_in_countdown(it_countdown):
    finish_countdown_str = f"{it_countdown["day"]}/{it_countdown["month"]}/{it_countdown["year"]}, {it_countdown["hour"]}:{it_countdown["minute"]}"

    on_countdown = False
    if it_countdown["year"] > date_time.year:
        on_countdown = True
    elif it_countdown["year"] < date_time.year:
        on_countdown = False
    elif it_countdown["month"] > date_time.month:
        on_countdown = True
    elif it_countdown["month"] < date_time.month:
        on_countdown = False
    elif it_countdown["day"] > date_time.day:
        on_countdown = True
    elif it_countdown["day"] < date_time.day:
        on_countdown = False
    elif it_countdown["hour"] > date_time.hour:
        on_countdown = True
    elif it_countdown["hour"] < date_time.hour:
        on_countdown = False
    elif it_countdown["minute"] > date_time.minute:
        on_countdown = True
    elif it_countdown["minute"] < date_time.minute:
        on_countdown = False
    # Ultimo caso é quando o countdown acabou no minuto atual, mantém o valor falso lá de cima

    if on_countdown:
        print(f"-- Item ainda em countdown. Finaliza em: {finish_countdown_str}")
    else:
        print(f"-- Acabou o countdown do item. Finalizado em: {finish_countdown_str}")

    return on_countdown
    

def cancel_item_buy():
    # Clica em Cancelar
    cancel_button = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, ".item_market_action_button")
        )
    )
    cancel_button.click()

    time.sleep(1) # TO.DO SLEEP NO CÓDIGO SER VARIÁVEL

def cancel_item_sell():
    # Clica em Remover
    remove_button = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, ".item_market_action_button_contents")
        )
    )
    remove_button.click()

    time.sleep(0.8)

    # Usando o ID (mais rápido e garantido)
    confirm_remove_button = wait.until(
        EC.element_to_be_clickable((By.ID, "market_removelisting_dialog_accept"))
    )
    confirm_remove_button.click()

    time.sleep(5)

def item_buy(value, quant):
    value = str(value).replace(".", ",")

    # Clica em Comprar...
    buy_button = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, ".market_commodity_buy_button")
        )
    )
    buy_button.click()
    
    time.sleep(1.2)

    # Modifica valor de compra
    input_price = wait.until(
        EC.element_to_be_clickable(
            (By.ID, "market_buy_commodity_input_price")
        )
    )
    driver.execute_script("""
        arguments[0].value = arguments[1];
        arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
        arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
    """, input_price, value)

    # Modifica quantidade à comprar
    input_quant = wait.until(
        EC.element_to_be_clickable(
            (By.ID, "market_buy_commodity_input_quantity")
        )
    )
    input_quant.clear()
    input_quant.send_keys(str(quant))

    # CORRIGIR: AQUELE PROBLEMA DE QUE AS VEZES O ITEM BAIXA 1 OU 2 CENTAVOS

    # Aceita os termos
    accept_terms = wait.until(
        EC.presence_of_element_located(
            (By.ID, "market_buyorder_dialog_accept_ssa")
        )
    )

    driver.execute_script("""
        arguments[0].checked = true;
        arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
    """, accept_terms)

    time.sleep(1.2)

    # Encomenda itens
    finish_buy = wait.until(
        EC.element_to_be_clickable(
            (By.ID, "market_buyorder_dialog_purchase")
        )
    )
    finish_buy.click()

    time.sleep(2)

    # Esperando confirmação da compra
    wait.until(
        EC.invisibility_of_element_located(
            (By.CSS_SELECTOR, ".market_confirmation_container.market_dialog_content_darker")
        )
    )

    # Esperando finalização da compra
    wait.until(
        lambda d: d.find_element(
            By.ID, "market_buy_commodity_status"
        ).text.strip() != "Buscando anúncios do item no preço desejado..."
    )

def item_sell(item_name, item_url, value):
    value = str(value).replace(".", ",")

    driver.get(f"https://steamcommunity.com/id/{user}/inventory")
    aguardar_pagina(driver)

    # Busca apenas elementos que possuem a classe 'item' e um ID que começa com números

    wait = WebDriverWait(driver, 10)

    filter_box = wait.until(EC.element_to_be_clickable((By.ID, "filter_control")))
    filter_box.clear()
    filter_box.send_keys(item_name)

    time.sleep(0.5)
    
    # Pega todos os itens e filtra o que está visível de fato
    all_items = driver.find_elements(By.CSS_SELECTOR, ".itemHolder .item")
    target_item = next((item for item in all_items if item.is_displayed()), None)

    if target_item:
        # Clica no link interno que é o alvo real do evento da Steam
        link = target_item.find_element(By.CSS_SELECTOR, ".inventory_item_link")
        driver.execute_script("arguments[0].click();", link)
    else:
        print("Nenhum item visível após o filtro.")

    # Clicar em vender
    wait = WebDriverWait(driver, 10)
    botao_vender = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Vender')]")))
    botao_vender.click()

    time.sleep(1)

    # Modifica o valor de venda
    input_quant = wait.until(
        EC.element_to_be_clickable(
            (By.ID, "market_sell_buyercurrency_input")
        )
    )
    input_quant.clear()
    input_quant.send_keys(value)

    time.sleep(0.5)

    # Aceita os termos
    accept_terms = wait.until(
        EC.presence_of_element_located(
            (By.ID, "market_sell_dialog_accept_ssa")
        )
    )

    driver.execute_script("""
        arguments[0].checked = true;
        arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
    """, accept_terms)
    time.sleep(1.2)

    # Vende itens
    sell_button = wait.until(
        EC.element_to_be_clickable(
            (By.ID, "market_sell_dialog_accept")
        )
    )
    sell_button.click()
    time.sleep(0.8)

    # Confirma venda
    wait.until(EC.element_to_be_clickable((By.XPATH, "//a[span[text()='OK']]")))

    ok_button = driver.find_element(By.XPATH, "//a[span[text()='OK']]")
    driver.execute_script("arguments[0].click();", ok_button)

    time.sleep(5)

    driver.get(item_url)
    aguardar_pagina(driver)

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

def calculate_total_buying(items):
    total_buying = 0.0

    for item in items:
        buy_data = item["buying_data"]

        if buy_data != {}:
            total_buying += (buy_data["quant"] * buy_data["price"])

    return round(total_buying, 2)




try:
    # Espera a URL mudar
    wait.until(EC.url_changes(login_url))
    
    print("Sucesso! Você está logado.")
    print(f"Página atual: {driver.current_url}")

except Exception as e:
    print(f"Tempo de login esgotado: {e}")
    exit()

with open('data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
items = data["items"]
buy_and_sell = data["buy_and_sell"]

print(f"Total buying inicial: {calculate_total_buying(items)}")

index = 0
last_index = -1
iteration = 0
while index < len(items):
    item_name = items[index]["name"]
    item_url = items[index]["url"]
    buy_status = items[index]["buy_status"]
    sell_data = items[index]["sell_data"]

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
        collected_price_buying = 0.0
        collected_quant_buying = 0

        buy_user_price_data = driver.find_elements(
            By.CLASS_NAME, "market_listing_price"
        )

        if len(buy_user_price_data) >= 2:
            collected_price_buying = float(
                buy_user_price_data[0].text
                    .replace("R$", "")
                    .replace(".", "")
                    .replace(",", ".")
                    .strip()
            )

            collected_quant_buying = int(
                buy_user_price_data[1].text.strip()
            )

        print(collected_price_buying, collected_quant_buying)

        # ENCONTRAR VALORES DE VENDA DO USUÁRIO
        collected_price_selling = 0.0
        try:
            sale_price_element = driver.find_element(By.XPATH, "//span[@title='Este é o valor pago pelo comprador.']")
            
            collected_price_selling = float(
                sale_price_element.text
                .replace("R$", "")
                .replace(".", "")
                .replace(",", ".")
                .strip()
            )
            print(f"Preço de venda: {collected_price_selling}")
        except:
            ""

        print(collected_price_selling)


    else:
        iteration += 1
        
    last_index = index

    if iteration > 0: # apenas separa
        print("=")

    if buy_status == "buying":
        print(f"C{iteration}. Comprando *")
        buying_data = items[index]["buying_data"]
        is_profitable, offer_value, order_value = check_is_profitable(collected_offer_value, collected_order_value)

        print(buying_data["quant"])
        print(collected_quant_buying)

        if buying_data["quant"] > collected_quant_buying:
            diff = buying_data["quant"] - collected_quant_buying

            print("- Adicionando {diff} itens a lista de vendas.")

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
        if buying_data["price"] != collected_order_value and collected_quant_buying > 0:
            print("- Cancelando compra. Valor mudou.")
            cancel_item_buy()
            
            items[index]["buy_status"] = "waiting_to_buy"
            items[index]["buying_data"] = {}

            index -= 1

    if buy_status == "waiting_to_buy":
        print(f"C{iteration}. Checando itens disponíveis para compra *")

        max_items = items[index]["max_items"]
        num_items_to_sell = len(items[index]["sell_data"])

        quant_to_buy = max_items - num_items_to_sell

        if quant_to_buy < 0:
            quant_to_buy = 0

        print(f"-- Limite de itens: {max_items}")
        print(f"-- Itens sendo vendidos: {num_items_to_sell}")
        print(f"- Desejando comprar {quant_to_buy} item(ns).")

        is_profitable, offer_value, order_value = check_is_profitable(collected_offer_value, collected_order_value)

        if quant_to_buy <= 0:
            print(f"-- Nenhum item para comprar. Ignorando compra.")
        elif is_profitable == False:
            print(f"-- Lucro não é suficiente. Ignorando compra.")
        elif wallet_value < order_value:
            print(f"-- Dinheiro disponível na carteira (R${wallet_value}) menor do que o valor do item (R${order_value}). Ignorando.")
        elif (calculate_total_buying(items) + (order_value * quant_to_buy)) > buy_limit:
            print(f"-- Buy limit atingido. Ignorando.")
        else:
            print(f"-- Comprando item por R${order_value}")
            item_buy(order_value, quant_to_buy)

            items[index]["buy_status"] = "buying"
            items[index]["buying_data"] = {
                "quant": quant_to_buy,
                "price": order_value
            }

    if iteration == 0 and len(sell_data) > 0:
        first_sell_data = sell_data[0]

        {
            "buy_price": 6.15,
            "sell_price": 0.0,
            "status": "countdown",
            "countdown": {
                "day": 31,
                "month": 1,
                "year": 2026,
                "hour": 5,
                "minute": 0
            }
        }

        if first_sell_data["status"] == "countdown":
            print(f"V{iteration}: Chegando se item ainda está em countdown.")
            on_countdown = check_is_in_countdown(first_sell_data["countdown"])

            if on_countdown == False:
                sell_data[0]["countdown"] = {}
                sell_data[0]["status"] = "waiting_to_sell"

        if first_sell_data["status"] == "selling":
            print(f"V{iteration}: Checando item sendo vendido.")
            print(f"-- Valor que estou vendendo de acordo com os dados da página Steam: R${collected_price_selling}")

            if collected_price_selling == 0.0:
                print(f"*** Item vendido por {first_sell_data["sell_price"]}! ***")

                buy_price_value = first_sell_data["buy_price"]
                sell_price_value = first_sell_data["sell_price"]
                tax_value = round(sell_price_value * 0.15, 2)

                if tax_value <= 0.1:
                    tax_value = 0.1
                    
                profit_value = round(sell_price_value - buy_price_value - tax_value, 2)

                buy_and_sell.append({
                    "name": items[index]["name"],
                    "url": items[index]["url"],
                    "date": {
                        "day": date_time.day,
                        "month": date_time.month,
                        "year": date_time.year
                    },
                    "buy_price": buy_price_value,
                    "sell_price": sell_price_value,
                    "tax": tax_value,
                    "profit": profit_value
                    
                })

                items[index]["sell_data"].pop(0)
                sell_data = items[index]["sell_data"]

                if len(sell_data) > 0:
                    first_sell_data = sell_data[0]
                else:
                    first_sell_data = None

            elif collected_price_selling != collected_offer_value:
                print(f"- Estou vendendo à R${collected_price_selling}, mas o mercado à R${collected_offer_value}. Corrigindo...")

                sell_data[0]["status"] = "waiting_to_sell"
                sell_data[0]["sell_price"] = 0.0

                cancel_item_sell()

        if first_sell_data != None and first_sell_data["status"] == "waiting_to_sell":
            print(f"- V{iteration}: Iniciando venda de item.")

            item_sell(item_name, item_url, offer_value)

            items[index]["sell_data"][0]["status"] = "selling"
            items[index]["sell_data"][0]["sell_price"] = offer_value

    index += 1

    with open("data.json", "w", encoding="utf-8") as f:
        json.dump({"items": items, "buy_and_sell": buy_and_sell}, f, ensure_ascii=False, indent=4)

    time.sleep(5)


print("")
print("Finalizado.")