import json

with open('data/anatomy_data_simple.json', 'r') as f:
    data = json.load(f)

# 1. Inspect 'other'
print("--- OTHERS ---")
for item in data.get('other', []):
    print(f"{item['id']}|{item['nameEn']}|{item['nameCn']}")

# 2. Inspect potentially bad translations
print("\n--- POTENTIAL BAD TRANSLATIONS ---")
for sys, items in data.items():
    for item in items:
        # If nameCn is same as nameEn or has too many English characters
        en_chars = sum(1 for c in item['nameCn'] if ord(c) < 128)
        if en_chars > len(item['nameCn']) * 0.5:
             print(f"{sys}|{item['id']}|{item['nameEn']}|{item['nameCn']}")
