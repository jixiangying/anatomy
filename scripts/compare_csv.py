import csv

# 定义中英映射（考虑到专家判定的中文名称）
MAPPING = {
    "skeletal": "骨骼",
    "muscular": "肌肉",
    "cardiovascular": "心血管",
    "nervous": "神经",
    "digestive": "消化",
    "respiratory": "呼吸",
    "urinary": "泌尿",
    "reproductive": "生殖",
    "endocrine": "内分泌",
    "lymphatic": "淋巴",
    "integumentary": "皮肤",
    "other": "其他"
}

# 逆向映射（用于双向检查）
REVERSE_MAPPING = {v: k for k, v in MAPPING.items()}

diff_count = 0
with open('anatomy_names.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    header = next(reader)
    
    print(f"{'行号':<6} | {'ID':<8} | {'英文名':<40} | {'旧分类':<15} | {'专家判定':<10}")
    print("-" * 90)
    
    for i, row in enumerate(reader, 2):
        old_sys = row[3].strip()
        expert_sys = row[4].strip()
        
        # 比较核心：判断意思是否一致
        # 如果旧分类是 'integumentary'，映射后应为 '皮肤'
        old_sys_cn = MAPPING.get(old_sys, old_sys)
        
        if old_sys_cn != expert_sys:
            diff_count += 1
            print(f"{i:<6} | {row[0]:<8} | {row[1][:38]:<40} | {old_sys:<15} | {expert_sys:<10}")

print("-" * 90)
print(f"总计不一致行数: {diff_count}")
