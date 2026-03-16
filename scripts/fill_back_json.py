import json
import csv

# 1. 加载修改后的 CSV 数据
# CSV 格式：English Name, Chinese Name
csv_entries = []
with open('anatomy_names.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    next(reader) # 跳过表头
    for row in reader:
        if len(row) >= 2:
            csv_entries.append({'en': row[0], 'cn': row[1]})

# 2. 加载当前的 JSON
json_path = 'data/anatomy_data_simple_refined.json'
with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# 3. 按顺序回填
# 因为 CSV 是按 JSON 顺序生成的，我们直接遍历 JSON 并从 csv_entries 中提取对应的中文
csv_idx = 0
total_updated = 0

# 系统排序与生成 CSV 时的顺序保持一致
SYSTEM_ORDER = ['skeletal', 'muscular', 'cardiovascular', 'nervous', 'digestive', 'respiratory', 'urinary', 'reproductive', 'endocrine', 'lymphatic', 'integumentary', 'other']

for sys_key in SYSTEM_ORDER:
    if sys_key not in data: continue
    for item in data[sys_key]:
        if csv_idx < len(csv_entries):
            # 双重校验：确保英文名对得上（忽略大小写）
            if item['nameEn'].lower() == csv_entries[csv_idx]['en'].lower():
                new_cn = csv_entries[csv_idx]['cn']
                item['nameCn'] = new_cn
                item['name'] = f"{new_cn} | {item['nameEn']}"
                total_updated += 1
            csv_idx += 1

# 4. 保存更新后的 JSON
with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"回填完成。共更新了 {total_updated} 个部件的中文名称。")
