import pyautogui
import pyperclip
import time
import re

def get_item_data(item, first_item):
    # Clicar na url
    pyautogui.moveTo(1497, 53)
    pyautogui.click()

    # Cola link do item
    pyperclip.copy(item["url"])
    pyautogui.hotkey("ctrl", "v")
    time.sleep(0.1)

    pyautogui.press("enter")
    time.sleep(3)

    if first_item == True:
        time.sleep(3)

    # Obter dados do item
    pyautogui.hotkey("ctrl", "a")
    pyautogui.hotkey("ctrl", "c")
    item_str = pyperclip.paste()
    time.sleep(0.2)

    # REMOVER MARCAÇÃO AZUL
    pyautogui.moveTo(1400, 500)
    pyautogui.click()
    time.sleep(0.2)

    # Sroll
    pyautogui.scroll(-1500)

    time.sleep(0.3)

    return item_str

import re

def check_item_market_data(item_text):
    sales_count, buy_orders_count = extract_orders_and_sales(item_text)

    return {
        "buy": extract_prices(item_text, "Comprar", "buy"),
        "sell": extract_prices(item_text, "Vender", "sell"),
        "sales_count": sales_count,
        "buy_count": buy_orders_count
    }






def extract_prices(item_text, section_type, mode):
    """
    mode:
      - "buy"  -> completa com preços altos
      - "sell" -> completa com preços baixos
    """

    pattern = (
        rf"{section_type}.*?\r?\n"
        rf"Preço\s+Quantidade\r?\n"
        rf"((?:R\$\s*[0-9]+,[0-9]{{2}}\s+\d+\r?\n){{1,5}})"
    )

    match = re.search(pattern, item_text, re.DOTALL)
    values = []

    if match:
        section_block = match.group(1)
        values = re.findall(
            r"R\$\s*([0-9]+,[0-9]{2})\s+(\d+)",
            section_block
        )

    result = [
        {
            "price": float(price.replace(",", ".")),
            "quantity": int(quantity)
        }
        for price, quantity in values
    ]

    missing = 5 - len(result)

    if missing > 0:
        if mode == "buy":
            filler_prices = [150000 - i * 10000 for i in range(missing)]
        else:
            filler_prices = [0.10 + i * 0.01 for i in range(missing)]

        for p in filler_prices:
            result.append({
                "price": p,
                "quantity": 0
            })

    return result


def extract_orders_and_sales(item_text):
    sales_match = re.search(
        r"(Meus anúncios|My listings)\s*\((\d+)\)",
        item_text
    )
    buy_orders_match = re.search(
        r"(Minhas encomendas|My buy orders)\s*\((\d+)\)",
        item_text
    )

    sales_count = int(sales_match.group(2)) if sales_match else 0
    buy_orders_count = int(buy_orders_match.group(2)) if buy_orders_match else 0

    return sales_count, buy_orders_count