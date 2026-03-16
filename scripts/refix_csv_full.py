import csv

# 定义标准映射以防万一
MAPPING = {
    "skeletal": "骨骼", "muscular": "肌肉", "cardiovascular": "心血管",
    "nervous": "神经", "digestive": "消化", "respiratory": "呼吸",
    "urinary": "泌尿", "reproductive": "生殖", "endocrine": "内分泌",
    "lymphatic": "淋巴", "integumentary": "皮肤", "other": "其他"
}

all_rows = []
with open('anatomy_names.csv', 'r', encoding='utf-8') as f:
    reader = list(csv.reader(f))
    header = reader[0]
    # 确保有第七列
    if len(header) < 7: header.append('最终判断')
    
    # 遍历所有数据行（从索引1开始）
    for i, row in enumerate(reader[1:], 2):
        old_sys_code = row[3]
        old_sys_cn = MAPPING.get(old_sys_code, old_sys_code)
        expert_sys_cn = row[4]
        
        # 确保行长度至少为 7
        while len(row) < 7: row.append("")
        
        # 核心逻辑应用
        if i <= 1000:
            if i == 164:
                row[6] = old_sys_cn
            elif 866 <= i <= 999:
                row[6] = old_sys_cn
            else:
                # 之前一致或不一致但取第五列的情况
                if old_sys_cn == expert_sys_cn:
                    row[6] = expert_sys_cn
                else:
                    row[6] = expert_sys_cn
        else:
            # 1000 行之后
            row[6] = expert_sys_cn
            # 专项修正
            if i == 2192 or i == 2195:
                row[6] = "肌肉"
        
        all_rows.append(row)

with open('anatomy_names.csv', 'w', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(all_rows)

print("全量 CSV 第七列更新指令已执行。")
