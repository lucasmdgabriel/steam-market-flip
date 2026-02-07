import json

with open('data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
items = data["items"]

wallet_value = float(input("Carteira: "))
wallet_pendent = float(input("Pendente: "))

total_value = wallet_value + wallet_pendent
quant = 0
for item in items:
    for sell_data in item["sell_data"]:
        print(f"\n{item["name"]}")
        print(sell_data)
        total_value += sell_data["buy_price"]
        quant += 1

print(f"Quant: {quant}")
total_value = round(total_value, 2)
print(f"Patrimônio: {total_value}")