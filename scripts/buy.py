import pyautogui
import pyperclip
import time
import random

def buy_action(value, steam_wallet):
    if value > steam_wallet:
        print("Saldo insuficiente. Ignorando.")
        return False

    time.sleep(0.25)

    # CLICAR EM COMPRAR
    pyautogui.moveTo(720, 160)
    pyautogui.click()
    time.sleep(0.25)

    pos_cada = pyautogui.locateOnScreen("assets/Word_cada.png")

    # MUDAR VALOR
    pyautogui.moveTo(pos_cada.left - 39, pos_cada.top + 8)
    for i in range(3):
        pyautogui.click()
        time.sleep(0.1)

    pyperclip.copy(value)
    pyautogui.hotkey("ctrl", "v")

    pos_aceito = pyautogui.locateOnScreen("assets/Button.png")
    # CONCORDAR COM TERMOS
    pyautogui.moveTo(pos_aceito.left - 13, pos_aceito.top + 5)
    pyautogui.click()
    time.sleep(0.1)

    # COMPRAR
    pyautogui.moveTo(pos_aceito.left + 585, pos_aceito.top -20)
    pyautogui.click()
    time.sleep(15)

    # CLIQUE FORA
    pyautogui.moveTo(1400, 500)
    pyautogui.click()
    time.sleep(2)


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
