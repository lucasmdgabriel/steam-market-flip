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
for day in days:
    print(f"{day}: {items_data[day]}")
    total += items_data[day]

print("")
print(f"Lucro total: R${round(total, 2)}")
print(f"Lucro médio: R${round(total/len(items_data), 2)}")