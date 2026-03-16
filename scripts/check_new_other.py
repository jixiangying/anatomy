import json
with open('data/anatomy_data_simple_new.json', 'r') as f:
    data = json.load(f)
for item in data['other'][:20]:
    print(f"{item['id']}: {item['nameEn']} | {item['nameCn']}")
