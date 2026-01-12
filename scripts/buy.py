import pyautogui
import pyperclip
import time

def buy_action(value):
    pyautogui.scroll(-300)

    # Minimizar VS Code
    pyautogui.moveTo(727, 826)
    pyautogui.click()
    time.sleep(0.1)

    pos_cada = pyautogui.locateOnScreen("assets/Word_cada.png")
    pos_aceito = pyautogui.locateOnScreen("assets/Button.png")

    # MUDAR VALOR
    pyautogui.moveTo(pos_cada.left - 39, pos_cada.top + 8)
    for i in range(3):
        pyautogui.click()
        time.sleep(0.1)

    pyperclip.copy(value)
    pyautogui.hotkey("ctrl", "v")


    print(pos_aceito)

    # CONCORDAR COM TERMOS
    pyautogui.moveTo(pos_aceito.left - 13, pos_aceito.top + 5)
    pyautogui.click()
    time.sleep(0.1)

    # COMPRAR
    pyautogui.moveTo(pos_aceito.left + 585, pos_aceito.top - 27)
    pyautogui.click()
    time.sleep(15)
