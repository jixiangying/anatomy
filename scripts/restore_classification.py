import json
import csv

# 1. 加载当前数据（包含用户修复的中文和改进后的英文）
with open('data/anatomy_data_simple_refined.json', 'r', encoding='utf-8') as f:
    current_data = json.load(f)

# 将所有部件拍平，提取 ID -> (nameEn, nameCn) 的映射
all_items = []
for sys in current_data:
    all_items.extend(current_data[sys])

# 2. 专家级分类逻辑（恢复 v5 版）
SYSTEM_RULES = [
    (['artery', 'vein', 'vessel', 'aorta', 'atrium', 'ventricle', 'vascular', 'sinus', 'cardiac', 'heart', 'portal', 'capillary', 'anastomosis', 'plexus', 'tributary', 'arcuate'], 'cardiovascular'),
    (['nerve', 'ganglion', 'brain', 'thalamus', 'pons', 'medulla', 'cerebr', 'hippocampus', 'amygdala', 'callosum', 'matter', 'hemisphere', 'retina', 'cornea', 'iris', 'lens', 'ciliary', 'optic', 'sclera', 'lacrimal', 'eyeball', 'vitreous', 'conjunctiva'], 'nervous'),
    (['esophagus', 'stomach', 'duodenum', 'jejunum', 'ileum', 'colon', 'rectum', 'liver', 'gallbladder', 'pancreas', 'biliary', 'salivary', 'tongue', 'tooth', 'teeth', 'dental', 'gingiva', 'palate', 'lip', 'pharynx', 'appendix', 'hepatic', 'common bile duct'], 'digestive'),
    (['lung', 'trachea', 'bronch', 'larynx', 'epiglottis', 'vocal', 'pleura', 'nasal', 'choana', 'nasopharynx', 'cricoid', 'thyroid cartilage'], 'respiratory'),
    (['kidney', 'ureter', 'bladder', 'urethra', 'renal'], 'urinary'),
    (['testis', 'prostate', 'penis', 'ovary', 'uterus', 'vagina', 'seminal', 'epididymis', 'scrotum', 'vulva', 'deferent'], 'reproductive'),
    (['thyroid gland', 'adrenal gland', 'pituitary', 'pineal', 'parathyroid', 'islet'], 'endocrine'),
    (['spleen', 'lymph', 'thymus', 'tonsil'], 'lymphatic'),
    (['skin', 'hair', 'nail', 'epithelium', 'dermis', 'epidermis', 'integument', 'sebaceous', 'sweat'], 'integumentary'),
    (['muscle', 'tendon', 'fascia', 'rectus', 'oblique', 'vastus', 'trapezius', 'pectoralis', 'levator', 'adductor', 'flexor', 'pronator', 'aponeurosis', 'muscular'], 'muscular'),
    (['bone', 'vertebra', 'skull', 'rib', 'sternum', 'xiphoid', 'spine', 'sacrum', 'phalanx', 'femur', 'tibia', 'hip bone', 'hyoid', 'clavicle', 'scapula', 'condyle', 'process', 'ligament', 'suture', 'joint', 'articulation', 'cartilage', 'membrane', 'disk', 'disc', 'meniscus'], 'skeletal'),
]

SYSTEM_PRIORITY = ["cardiovascular", "nervous", "respiratory", "digestive", "urinary", "reproductive", "endocrine", "lymphatic", "integumentary", "muscular", "skeletal"]

system_names = {
    "skeletal": "骨骼系统", "muscular": "肌肉系统", "cardiovascular": "心血管系统",
    "nervous": "神经系统", "digestive": "消化系统", "respiratory": "呼吸系统",
    "urinary": "泌尿系统", "reproductive": "生殖系统", "endocrine": "内分泌系统",
    "lymphatic": "淋巴系统", "integumentary": "皮肤系统", "other": "其他"
}

# 3. 重新分拣
final_data = {k: [] for k in system_names.keys()}

for item in all_items:
    en = item['nameEn'].lower()
    sys_code = "other"
    
    # 根据专家逻辑判定系统
    matched_codes = set()
    for keywords, code in SYSTEM_RULES:
        if any(k in en for k in keywords):
            matched_codes.add(code)
    
    if matched_codes:
        for p in SYSTEM_PRIORITY:
            if p in matched_codes:
                sys_code = p
                break
    
    # 强制修正一些明显的错位
    if "bone" in en: sys_code = "skeletal"
    if "muscle" in en: sys_code = "muscular"
    if "tooth" in en or "teeth" in en: sys_code = "digestive"
    
    # 保持原有 ID、改进后的英文名和用户的中文名
    item['system'] = system_names[sys_code]
    # 更新完整名称显示
    item['name'] = f"{item['nameCn']} | {item['nameEn']}"
    
    final_data[sys_code].append(item)

# 4. 覆盖保存
with open('data/anatomy_data_simple_refined.json', 'w', encoding='utf-8') as f:
    json.dump(final_data, f, ensure_ascii=False, indent=2)

print("分类已回滚至专家版本，同时保留了具体的英文名和您的中文翻译。")
for k, v in final_data.items():
    print(f"{k}: {len(v)}")
