import pyautogui
import pyperclip
import time

def check_item(item, account_name):
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
    item_data = texto = pyperclip.paste()

    print(item_data)

    print (f"{item}")