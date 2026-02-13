import json

with open('data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
items = data["items"]
buy_and_sell = data["buy_and_sell"]

days = []
items_data = {}
for item in buy_and_sell:
    day = ""
    if "date" in item:
        day = f"{item["date"]["day"]}/{item["date"]["month"]}/{item["date"]["year"]}"
    else:
        day = "None"


    if day in items_data:
        items_data[day] += item["profit"]
    elif day != "None":
        items_data[day] = item["profit"]
        days.append(day)

total = 0
last_day = ""
quant_days = 0
profit_days = 0
for day in days:
    day_str = day.split("/")[0]

    if last_day != "" and day_str != "1" and int(last_day) + 1 != int(day_str):
        quant_days += 1

    quant_days += 1
    profit_days += 1
    last_day = str(day_str)

    print(f"{day}: {round(items_data[day], 2)}")
    total += items_data[day]

print("")
print(f"Quantidade de dias: {quant_days}")
print(f"Dias de lucro: {profit_days}")
print(f"Lucro total: R${round(total, 2)}")
print(f"Lucro médio: R${round(total/quant_days, 2)}")