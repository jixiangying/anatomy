import csv

# 系统映射字典
MAPPING = {
    "skeletal": "骨骼", "muscular": "肌肉", "cardiovascular": "心血管",
    "nervous": "神经", "digestive": "消化", "respiratory": "呼吸",
    "urinary": "泌尿", "reproductive": "生殖", "endocrine": "内分泌",
    "lymphatic": "淋巴", "integumentary": "皮肤", "other": "其他"
}

updated_rows = []
with open('anatomy_names.csv', 'r', encoding='utf-8') as f:
    # 强制加载所有数据以确保不会中途断开
    content = list(csv.reader(f))
    
    header = content[0]
    # 确保 Header 有 7 列
    while len(header) < 7:
        if len(header) == 6: header.append('最终判断')
        else: header.append(f'Col_{len(header)+1}')
    
    updated_rows.append(header)
    
    # 遍历数据行 (i 是行号，从 2 开始)
    for i, row in enumerate(content[1:], 2):
        # 确保行长度至少为 7
        while len(row) < 7: row.append("")
        
        old_sys_code = row[3]
        old_sys_cn = MAPPING.get(old_sys_code, old_sys_code)
        expert_judgment = row[4]
        
        # 逻辑判定
        if i <= 1000:
            if i == 164:
                row[6] = old_sys_cn
            elif 866 <= i <= 999:
                row[6] = old_sys_cn
            else:
                row[6] = expert_judgment
        else:
            # 1000 行之后
            row[6] = expert_judgment
            # 特殊行修正 (基于 Model ID FJ1551 和 FJ1552 的行号)
            if i == 2192 or i == 2195:
                row[6] = "肌肉"
        
        updated_rows.append(row)

# 强制写回文件
with open('anatomy_names.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(updated_rows)

print(f"补全成功。共处理 {len(updated_rows)-1} 行数据。")
