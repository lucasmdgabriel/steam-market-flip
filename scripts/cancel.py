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
