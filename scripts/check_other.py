import json

with open('data/anatomy_data_simple.json', 'r') as f:
    data = json.load(f)

print(f"Items in other: {len(data['other'])}")
for item in data['other']:
    print(f"{item['id']}: {item['nameEn']} -> {item['nameCn']}")
