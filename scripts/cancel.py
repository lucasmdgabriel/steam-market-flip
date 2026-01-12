import pyautogui
import time

def cancel_action_buy():
    try:
        pos_cancel = pyautogui.locateOnScreen(
            "assets/Button_cancelar.png",
        )
    except pyautogui.ImageNotFoundException:
        return

    pyautogui.click(pos_cancel)
    time.sleep(1)

def cancel_action_sell():
    try:
        pos_cancel = pyautogui.locateOnScreen(
            "assets/Button_remover.png",
        )
    except pyautogui.ImageNotFoundException:
        return

    pyautogui.click(pos_cancel)
    time.sleep(0.25)

    # CONFIRMAR CANCELAMENTO
    pyautogui.moveTo(1104, 602)
    pyautogui.click()
    time.sleep(0.75)
