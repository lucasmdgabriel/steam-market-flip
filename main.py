from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

def aguardar_pagina(driver):
    WebDriverWait(driver, 10).until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )

driver = webdriver.Chrome()
# URL de login da Steam
login_url = "https://store.steampowered.com/login/?redir=&redir_ssl=1"
driver.get(login_url)

wait = WebDriverWait(driver, 300)

try:
    # Espera a URL mudar
    wait.until(EC.url_changes(login_url))
    
    print("Sucesso! Você está logado.")
    print(f"Página atual: {driver.current_url}")

except Exception as e:
    print(f"Tempo de login esgotado: {e}")
    exit()

# driver.find_element("xpath", "//button[text()='Criar conta']").click()

driver.get("https://steamcommunity.com/market/listings/753/282010-Splat")
aguardar_pagina(driver)


buy_price_quant = driver.find_elements(By.CLASS_NAME, "market_listing_price")

buy_price = buy_price_quant[0].text.strip().replace("R$ ", "")
buy_quant = buy_price_quant[1].text.strip()

print(f"Preço: {buy_price}")
print(f"Quantidade: {buy_quant}")


input("Pressione Enter para fechar...")
driver.quit()