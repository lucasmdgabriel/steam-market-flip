from decimal import Decimal
import pyautogui
import pyperclip
import time
import random

def buy_action(value, steam_wallet, buy_limit, total_buying):
    if value > steam_wallet:
        print("Saldo insuficiente. Ignorando.")
        return False, total_buying, value
    
    if buy_limit < (float(value) + total_buying):
        print("Limite alcançado.")
        return False, total_buying, value

    time.sleep(0.25)

    # CLICAR EM COMPRAR
    pyautogui.moveTo(720, 160)
    pyautogui.click()
    time.sleep(0.25)

    find_pos = False
    while find_pos == False:
        find_pos = True
        try:
            pos_cada = pyautogui.locateOnScreen("assets/Word_cada.png")
        except pyautogui.ImageNotFoundException:
            input("Erro ao encontra rpos_cada")
            find_pos = True
    max_value = Decimal("0.0")
    value -= Decimal("0.01")

    while float(max_value) != float(value):
        value += Decimal("0.01")

        # MUDAR VALOR
        pyautogui.moveTo(pos_cada.left - 39, pos_cada.top + 8)
        for i in range(3):
            pyautogui.click()
            time.sleep(0.1)

        pyperclip.copy(value)
        pyautogui.hotkey("ctrl", "v")

        pyautogui.moveTo(pos_cada.left - 39, pos_cada.top + 8 + 75)
        for i in range(2):
            pyautogui.click()
            time.sleep(0.1)

        pyautogui.hotkey("ctrl", "c")
        max_value = pyperclip.paste().replace(",", ".")


    find_pos = False
    while find_pos == False:
        find_pos = True
        try:
            pos_aceito = pyautogui.locateOnScreen("assets/Button.png")
        except pyautogui.ImageNotFoundException:
            input("Erro ao encontra pos_aceito")
            find_pos = True
    # CONCORDAR COM TERMOS
    pyautogui.moveTo(pos_aceito.left - 13, pos_aceito.top + 5)
    pyautogui.click()
    time.sleep(0.1)

    # COMPRAR
    pyautogui.moveTo(pos_aceito.left + 585, pos_aceito.top -20)
    pyautogui.click()
    
    image_found = False

    while image_found == False:
        image_found = True

        try:
            pyautogui.locateOnScreen("assets/Word_sucesso.png")
        except pyautogui.ImageNotFoundException:
            image_found = False

    return True, ( total_buying + float(value) ), value


def sell_action(value, name):
    time.sleep(0.25)

    # CLICAR EM VENDER
    pyautogui.moveTo(1160, 180)
    pyautogui.click()
    time.sleep(2)

    # TEXTO DE TITULO
    pyautogui.moveTo(755, 510)
    pyautogui.click()
    time.sleep(0.2)

    pyperclip.copy(name)
    pyautogui.hotkey("ctrl", "v")

    # CLICAR NO ITEM
    pyautogui.moveTo(565, 595)
    pyautogui.click()
    time.sleep(0.2)

    pyautogui.scroll(-1500 - random.randrange(500))

    # CLICAR EM VENDER
    pyautogui.moveTo(1090, 970)
    pyautogui.click()
    time.sleep(0.5)

    pyautogui.press('tab')
    time.sleep(0.5)

    pyperclip.copy(value)
    pyautogui.hotkey("ctrl", "v")

    # ACEITR TERMOS
    pyautogui.moveTo(540, 800)
    pyautogui.click()
    time.sleep(0.5)

    # CONFIRMAR COMPRA
    pyautogui.moveTo(1300, 830)
    pyautogui.click()
    time.sleep(0.5)

    # CONFIRMAR COMPRA (2)
    pyautogui.moveTo(1330, 720)
    pyautogui.click()
    time.sleep(0.5)

    return True
