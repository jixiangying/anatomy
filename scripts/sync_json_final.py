import json
import csv

# 1. 加载映射字典
MAPPING_TO_CODE = {
    "骨骼": "skeletal", "肌肉": "muscular", "心血管": "cardiovascular",
    "神经": "nervous", "消化": "digestive", "呼吸": "respiratory",
    "泌尿": "urinary", "生殖": "reproductive", "内分泌": "endocrine",
    "淋巴": "lymphatic", "皮肤": "integumentary", "其他": "other"
}

MAPPING_TO_NAME = {v: k + "系统" if k != "其他" else "其他" for k, v in MAPPING_TO_CODE.items()}
MAPPING_TO_EN = {
    "skeletal": "Skeletal System", "muscular": "Muscular System", "cardiovascular": "Cardiovascular System",
    "nervous": "Nervous System", "digestive": "Digestive System", "respiratory": "Respiratory System",
    "urinary": "Urinary System", "reproductive": "Reproductive System", "endocrine": "Endocrine System",
    "lymphatic": "Lymphatic System", "integumentary": "Integumentary System", "other": "Other"
}

# 2. 从 CSV 读取最新数据
csv_data = {}
with open('anatomy_names.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    next(reader) # skip header
    for row in reader:
        if len(row) >= 7:
            id_val = row[0]
            name_en = row[1]
            name_cn = row[2]
            final_sys_cn = row[6]
            sys_code = MAPPING_TO_CODE.get(final_sys_cn, "other")
            
            csv_data[id_val] = {
                "nameEn": name_en,
                "nameCn": name_cn,
                "sysCode": sys_code,
                "system": MAPPING_TO_NAME.get(sys_code, "其他"),
                "systemEn": MAPPING_TO_EN.get(sys_code, "Other")
            }

# 3. 重新分拣并构建新 JSON
new_json = {code: [] for code in MAPPING_TO_CODE.values()}

# 我们需要确保所有 ID 都被处理（即使 JSON 结构改变了）
for id_val, info in csv_data.items():
    item = {
        "id": id_val,
        "name": f"{info['nameCn']} | {info['nameEn']}",
        "system": info['system'],
        "nameEn": info['nameEn'],
        "nameCn": info['nameCn'],
        "systemEn": info['systemEn']
    }
    new_json[info['sysCode']].append(item)

# 4. 保存
with open('data/anatomy_data_simple_refined.json', 'w', encoding='utf-8') as f:
    json.dump(new_json, f, ensure_ascii=False, indent=2)

print("同步完成：JSON 的分类已根据 CSV 第七列重构，中文名已同步至第三列。")
for k, v in new_json.items():
    print(f"{k}: {len(v)}")
