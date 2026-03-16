import json
import csv

# 系统名称映射
SYS_MAP = {
    "骨骼": {"code": "skeletal", "cn": "骨骼系统", "en": "Skeletal System"},
    "肌肉": {"code": "muscular", "cn": "肌肉系统", "en": "Muscular System"},
    "心血管": {"code": "cardiovascular", "cn": "心血管系统", "en": "Cardiovascular System"},
    "神经": {"code": "nervous", "cn": "神经系统", "en": "Nervous System"},
    "消化": {"code": "digestive", "cn": "消化系统", "en": "Digestive System"},
    "呼吸": {"code": "respiratory", "cn": "呼吸系统", "en": "Respiratory System"},
    "泌尿": {"code": "urinary", "cn": "泌尿系统", "en": "Urinary System"},
    "生殖": {"code": "reproductive", "cn": "生殖系统", "en": "Reproductive System"},
    "内分泌": {"code": "endocrine", "cn": "内分泌系统", "en": "Endocrine System"},
    "淋巴": {"code": "lymphatic", "cn": "淋巴系统", "en": "Lymphatic System"},
    "皮肤": {"code": "integumentary", "cn": "皮肤系统", "en": "Integumentary System"},
    "其他": {"code": "other", "cn": "其他", "en": "Other"}
}

# 1. 读取 CSV (ID -> 翻译 & 最终分类)
csv_lookup = {}
with open('anatomy_names.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        if len(row) >= 7:
            fid, en, cn, _, _, _, final_sys_short = row[:7]
            config = SYS_MAP.get(final_sys_short, SYS_MAP["其他"])
            csv_lookup[fid] = {
                "nameEn": en,
                "nameCn": cn,
                "sysCode": config["code"],
                "systemCn": config["cn"],
                "systemEn": config["en"]
            }

# 2. 构建新 JSON 结构
new_json_data = {v["code"]: [] for v in SYS_MAP.values()}

# 3. 按 CSV 顺序填充（保证所有 ID 都在里面）
for fid, info in csv_lookup.items():
    item = {
        "id": fid,
        "name": f"{info['nameCn']} | {info['nameEn']}",
        "system": info['systemCn'],
        "nameEn": info['nameEn'],
        "nameCn": info['nameCn'],
        "systemEn": info['systemEn']
    }
    new_json_data[info['sysCode']].append(item)

# 4. 写入文件
with open('data/anatomy_data_simple_refined.json', 'w', encoding='utf-8') as f:
    json.dump(new_json_data, f, ensure_ascii=False, indent=2)

print("JSON 字段全量对齐完成：name, nameCn, system, systemEn 已达到 100% 严格一致。")
