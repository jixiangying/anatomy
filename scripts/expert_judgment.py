import csv

# 专家知识库规则
RULES = [
    (['artery', 'vein', 'vessel', 'aorta', 'atrium', 'ventricle', 'vascular', 'sinus', 'cardiac', 'heart', 'portal', 'capillary', 'anastomosis', 'plexus', 'tributary', 'arcuate', 'venous'], 'cardiovascular'),
    (['nerve', 'ganglion', 'brain', 'thalamus', 'pons', 'medulla', 'cerebr', 'hippocampus', 'amygdala', 'callosum', 'matter', 'hemisphere', 'retina', 'cornea', 'iris', 'lens', 'ciliary', 'optic', 'sclera', 'lacrimal', 'eyeball', 'vitreous', 'conjunctiva', 'habenula', 'commissure', 'gyrus', 'sulcus', 'olfactory'], 'nervous'),
    (['lung', 'trachea', 'bronch', 'larynx', 'epiglottis', 'vocal', 'pleura', 'nasal', 'choana', 'nasopharynx', 'cricoid', 'thyroid cartilage', 'arytenoid'], 'respiratory'),
    (['esophagus', 'stomach', 'duodenum', 'jejunum', 'ileum', 'colon', 'rectum', 'liver', 'gallbladder', 'pancreas', 'biliary', 'salivary', 'tongue', 'tooth', 'teeth', 'dental', 'gingiva', 'palate', 'lip', 'pharynx', 'appendix', 'hepatic', 'common bile duct', 'peritoneum', 'omentum', 'mesentery', 'falciform'], 'digestive'),
    (['kidney', 'ureter', 'bladder', 'urethra', 'renal'], 'urinary'),
    (['testis', 'prostate', 'penis', 'ovary', 'uterus', 'vagina', 'seminal', 'epididymis', 'scrotum', 'vulva', 'deferent', 'clitoris'], 'reproductive'),
    (['thyroid gland', 'adrenal gland', 'pituitary', 'pineal', 'parathyroid', 'islet'], 'endocrine'),
    (['spleen', 'lymph', 'thymus', 'tonsil'], 'lymphatic'),
    (['skin', 'hair', 'nail', 'epithelium', 'dermis', 'epidermis', 'integument', 'sebaceous', 'sweat', 'mammary'], 'integumentary'),
    (['muscle', 'tendon', 'fascia', 'rectus', 'oblique', 'vastus', 'trapezius', 'pectoralis', 'levator', 'adductor', 'flexor', 'pronator', 'aponeurosis', 'interspinalis', 'intertransversarius', 'diaphragm'], 'muscular'),
    (['bone', 'vertebra', 'skull', 'rib', 'sternum', 'xiphoid', 'spine', 'sacrum', 'phalanx', 'femur', 'tibia', 'hip bone', 'hyoid', 'clavicle', 'scapula', 'condyle', 'process', 'ligament', 'suture', 'joint', 'articulation', 'cartilage', 'membrane', 'disk', 'disc', 'meniscus', 'symphysis'], 'skeletal'),
]

SYSTEM_PRIORITY = ["cardiovascular", "nervous", "respiratory", "digestive", "urinary", "reproductive", "endocrine", "lymphatic", "integumentary", "muscular", "skeletal"]

# 存疑项知识库
DOUBTFUL_KEYWORDS = [
    'pharynx',    # 消化 vs 呼吸
    'pancreas',   # 消化 vs 内分泌
    'urethra',    # 泌尿 vs 生殖
    'hypothalamus', # 神经 vs 内分泌
    'sinus',      # 可能是血管窦或呼吸副鼻窦
    'duct',       # 需看前缀
    'region of',  # 范围描述
    'anatomical', # 抽象术语
    'caudate lobe' # 肝脏的一部分，需确认为实质还是血管
]

def judge_system(en):
    en = en.lower()
    matches = []
    for keywords, code in RULES:
        if any(k in en for k in keywords):
            matches.append(code)
    
    # 逻辑优先级处理
    if not matches:
        return "other", ""
    
    # 选取最高优先级
    final_code = "other"
    for p in SYSTEM_PRIORITY:
        if p in matches:
            final_code = p
            break
            
    # 判断是否存疑
    doubt = ""
    if len(matches) > 1:
        doubt = "存疑"
    if any(k in en for k in DOUBTFUL_KEYWORDS):
        doubt = "存疑"
        
    return final_code, doubt

# 执行 CSV 判定更新
updated_rows = []
with open('anatomy_names.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    header = next(reader)
    # 增加标题
    header = header + ['Expert Judgment', 'Notes']
    
    for row in reader:
        en_name = row[1]
        best_sys, doubt = judge_system(en_name)
        updated_rows.append(row + [best_sys, doubt])

with open('anatomy_names.csv', 'w', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(updated_rows)

print("专家判定已录入第五、六列。")
