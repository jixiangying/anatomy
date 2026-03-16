import csv

rows = []
with open('anatomy_names.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    header = next(reader)
    
    for i, row in enumerate(reader, 2):
        # row[4] 是专家判定，row[6] 是最终判断
        if i > 1000:
            expert_judgment = row[4]
            final_judgment = expert_judgment
            
            # 专项修正
            if i == 2192 or i == 2195:
                final_judgment = "肌肉"
            
            # 更新第七列
            if len(row) < 7:
                row.append(final_judgment)
            else:
                row[6] = final_judgment
        
        rows.append(row)

with open('anatomy_names.csv', 'w', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(rows)

print("已完成全量最终判断录入，并已修正 2192 和 2195 行为肌肉。")
