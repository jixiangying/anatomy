import json
import csv

# 1. 加载用户当前已修复的中文名
with open('data/anatomy_data_simple_refined.json', 'r', encoding='utf-8') as f:
    current_json = json.load(f)

id_to_user_cn = {}
for sys in current_json:
    for item in current_json[sys]:
        id_to_user_cn[item['id']] = item['nameCn']

# 2. 从原始文本中挖掘最具体的英文名（改进逻辑）
GENERIC_FILTER = {"organ with cavitated organ parts", "organ part", "organ component", "cardinal organ part", "organ", "anatomical entity", "physical anatomical entity", "material anatomical entity", "anatomical structure", "organ segment", "material physical anatomical entity", "set of organs", "viscus", "bone organ"}

fj_names = {}
with open('data/isa_element_parts.txt', 'r', encoding='utf-8') as f:
    for row in csv.DictReader(f, delimiter='\t'):
        fj, name = row['element file id'], row['name']
        if fj not in fj_names: fj_names[fj] = []
        fj_names[fj].append(name)

def get_best_en(names):
    best = names[0]
    max_score = -1
    for n in names:
        n_l = n.lower()
        score = 1000 if n_l not in GENERIC_FILTER else 0
        score += len(n) + (500 if "left" in n_l or "right" in n_l else 0)
        if score > max_score: max_score = score; best = n
    return best

# 3. 专家级系统分类逻辑（全量恢复）
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
system_names = {"skeletal":"骨骼系统","muscular":"肌肉系统","cardiovascular":"心血管系统","nervous":"神经系统","digestive":"消化系统","respiratory":"呼吸系统","urinary":"泌尿系统","reproductive":"生殖系统","endocrine":"内分泌系统","lymphatic":"淋巴系统","integumentary":"皮肤系统","other":"其他"}

# 4. 生成最终结果
final_output = {k: [] for k in system_names.keys()}
for fj_id in sorted(fj_names.keys()):
    best_en = get_best_en(fj_names[fj_id])
    
    # 重新应用专家分类逻辑
    sys_code = "other"
    matched_sys = set()
    # 检查该模型关联的所有名称来决定分类
    for name_candidate in fj_names[fj_id]:
        nc_l = name_candidate.lower()
        for keywords, code in SYSTEM_RULES:
            if any(k in nc_l for k in keywords): matched_sys.add(code)
    
    if matched_sys:
        for p in SYSTEM_PRIORITY:
            if p in matched_sys: sys_code = p; break
    
    # 二次强制修正
    be_l = best_en.lower()
    if "bone" in be_l: sys_code = "skeletal"
    if "muscle" in be_l: sys_code = "muscular"
    if "artery" in be_l or "vein" in be_l: sys_code = "cardiovascular"
    
    name_cn = id_to_user_cn.get(fj_id, best_en)
    
    final_output[sys_code].append({
        "id": fj_id,
        "name": f"{name_cn} | {best_en}",
        "system": system_names[sys_code],
        "nameEn": best_en,
        "nameCn": name_cn
    })

with open('data/anatomy_data_simple_refined.json', 'w', encoding='utf-8') as f:
    json.dump(final_output, f, ensure_ascii=False, indent=2)

print("--- 最终修复完成 ---")
for k, v in final_output.items():
    print(f"{k}: {len(v)}")
