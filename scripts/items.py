import pyautogui
import pyperclip
import time
import re

def get_item_data(item):
    # Clicar na url
    pyautogui.moveTo(1410, 70)
    pyautogui.click()

    # Cola link do item
    pyperclip.copy(item["url"])
    pyautogui.hotkey("ctrl", "v")
    time.sleep(0.1)

    pyautogui.press("enter")
    time.sleep(2)

    # Obter dados do item
    pyautogui.hotkey("ctrl", "a")
    pyautogui.hotkey("ctrl", "c")
    item_str = pyperclip.paste()

    return item_str

import re

def check_item_market_data(item_text):
    sales_count, buy_orders_count = extract_orders_and_sales(item_text)

    return {
        "buy": extract_prices(item_text, "Comprar"),
        "sell": extract_prices(item_text, "Vender"),
        "sales_count": sales_count,
        "buy_count": buy_orders_count
    }






def extract_prices(item_text, section_type):
    pattern = (
        rf"{section_type}.*?\r?\n"
        rf"Preço\s+Quantidade\r?\n"
        rf"((?:R\$\s*[0-9]+,[0-9]{{2}}\s+\d+\r?\n){{5}})"
    )

    match = re.search(pattern, item_text, re.DOTALL)
    if not match:
        return []

    section_block = match.group(1)

    values = re.findall(
        r"R\$\s*([0-9]+,[0-9]{2})\s+(\d+)",
        section_block
    )

    return [
        {
            "price": float(price.replace(',', '.')),
            "quantity": int(quantity)
        }
        for price, quantity in values
    ]


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