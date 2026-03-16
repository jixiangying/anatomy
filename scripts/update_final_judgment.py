import csv

MAPPING = {
    "skeletal": "骨骼", "muscular": "肌肉", "cardiovascular": "心血管",
    "nervous": "神经", "digestive": "消化", "respiratory": "呼吸",
    "urinary": "泌尿", "reproductive": "生殖", "endocrine": "内分泌",
    "lymphatic": "淋巴", "integumentary": "皮肤", "other": "其他"
}
REVERSE_MAPPING = {v: k for k, v in MAPPING.items()}

rows = []
with open('anatomy_names.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    header = next(reader)
    if len(header) < 7:
        header.append('最终判断')
    
    for i, row in enumerate(reader, 2):
        old_sys_code = row[3]
        old_sys_cn = MAPPING.get(old_sys_code, old_sys_code)
        expert_sys_cn = row[4]
        
        final_judgment = ""
        
        if i <= 1000:
            # 逻辑处理
            if i == 164:
                final_judgment = old_sys_cn
            elif 866 <= i <= 999:
                final_judgment = old_sys_cn
            elif old_sys_cn != expert_sys_cn:
                # 其他差异行取专家判定
                final_judgment = expert_sys_cn
            else:
                # 一致的行
                final_judgment = expert_sys_cn
        else:
            # 1000行之后暂时留空
            final_judgment = ""
            
        # 补齐行长
        if len(row) < 7:
            row.append(final_judgment)
        else:
            row[6] = final_judgment
            
        rows.append(row)

with open('anatomy_names.csv', 'w', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(rows)

print("已完成前1000行的最终判断录入。")
