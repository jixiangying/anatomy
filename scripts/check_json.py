import json

with open('data/anatomy_data_simple.json', 'r') as f:
    data = json.load(f)

for k, v in data.items():
    print(f"{k}: {len(v)}")

# Sample a few from each system to see if there are obvious errors
for k, v in data.items():
    print(f"\n--- {k} ---")
    for item in v[:5]:
        print(f"  {item['id']}: {item['nameEn']} -> {item['nameCn']}")
