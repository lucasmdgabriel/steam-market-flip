import pyautogui
import time
from decimal import Decimal

def cancel_action_buy(value, total_buying):
    try:
        pos_cancel = pyautogui.locateOnScreen(
            "assets/Button_cancelar.png",
        )
    except pyautogui.ImageNotFoundException:
        return total_buying

    pyautogui.click(pos_cancel)
    time.sleep(2.5)

    return total_buying - float(value)

def cancel_action_sell():
    try:
        pos_cancel = pyautogui.locateOnScreen(
            "assets/Button_remover.png",
        )
    except pyautogui.ImageNotFoundException:
        return

    pyautogui.click(pos_cancel)
    time.sleep(2.50)

    pos_cancel = None

    # CONFIRMAR CANCELAMENTO
    try:
        pos_cancel = pyautogui.locateOnScreen(
            "assets/Button_remove_off.png",
        )
    except pyautogui.ImageNotFoundException:
        print("Erro ao encontrar remofe_off 1")

    if pos_cancel == None:
        try:
            pos_cancel = pyautogui.locateOnScreen(
                "assets/Button_remove_off2.png",
            )
        except pyautogui.ImageNotFoundException:
            pyautogui.moveTo(1121, 602)
            print("Erro ao encontrar remofe_off 2")
    
    if pos_cancel != None:
        pyautogui.click(pos_cancel)
    else:
        pyautogui.click()
    
    time.sleep(1.75)