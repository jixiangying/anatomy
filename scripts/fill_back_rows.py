import json
import csv

# 1. 读取 CSV 中的所有中文名（严格保持顺序）
chinese_names = []
with open('anatomy_names.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    next(reader) # 跳过表头
    for row in reader:
        if len(row) >= 2:
            chinese_names.append(row[1])

# 2. 加载当前的 JSON
json_path = 'data/anatomy_data_simple_refined.json'
with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# 3. 按生成 CSV 时的系统顺序严格回填
SYSTEM_ORDER = ['skeletal', 'muscular', 'cardiovascular', 'nervous', 'digestive', 'respiratory', 'urinary', 'reproductive', 'endocrine', 'lymphatic', 'integumentary', 'other']

idx = 0
for sys in SYSTEM_ORDER:
    if sys in data:
        for item in data[sys]:
            if idx < len(chinese_names):
                new_cn = chinese_names[idx]
                item['nameCn'] = new_cn
                item['name'] = f"{new_cn} | {item['nameEn']}"
                idx += 1

# 4. 覆盖保存
with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"严格按行回填完成。共回填 {idx} 行。")
