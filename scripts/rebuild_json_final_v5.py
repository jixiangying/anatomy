import json
import csv

# 1. 加载原始数据源
fma_info = {}
with open('data/isa_parts_list.txt', 'r', encoding='utf-8') as f:
    for row in csv.DictReader(f, delimiter='\t'):
        fma_info[row['concept id']] = {'en': row['en'], 'kanji': row['kanji']}

fj_to_fmas = {}
with open('data/isa_element_parts.txt', 'r', encoding='utf-8') as f:
    for row in csv.DictReader(f, delimiter='\t'):
        fj = row['element file id']
        fma = row['concept id']
        if fj not in fj_to_fmas: fj_to_fmas[fj] = []
        fj_to_fmas[fj].append(fma)

# 2. 专家级系统分类词库 (涵盖之前漏掉的 551 个“其他”项)
SYSTEM_RULES = [
    # 心血管优先
    (['artery', 'vein', 'vessel', 'aorta', 'atrium', 'ventricle', 'vascular', 'sinus', 'cardiac', 'heart', 'portal', 'capillary', 'anastomosis', 'plexus', 'tributary', 'arcuate'], 'cardiovascular'),
    # 神经/感觉器官
    (['nerve', 'ganglion', 'brain', 'thalamus', 'pons', 'medulla', 'cerebr', 'hippocampus', 'amygdala', 'callosum', 'matter', 'hemisphere', 'retina', 'cornea', 'iris', 'lens', 'ciliary', 'optic', 'sclera', 'lacrimal', 'eyeball', 'vitreous', 'conjunctiva'], 'nervous'),
    # 消化
    (['esophagus', 'stomach', 'duodenum', 'jejunum', 'ileum', 'colon', 'rectum', 'liver', 'gallbladder', 'pancreas', 'biliary', 'salivary', 'tongue', 'tooth', 'teeth', 'dental', 'gingiva', 'palate', 'lip', 'pharynx', 'appendix', 'hepatic', 'common bile duct'], 'digestive'),
    # 呼吸
    (['lung', 'trachea', 'bronch', 'larynx', 'epiglottis', 'vocal', 'pleura', 'nasal', 'choana', 'nasopharynx', 'cricoid', 'thyroid cartilage'], 'respiratory'),
    # 泌尿
    (['kidney', 'ureter', 'bladder', 'urethra', 'renal'], 'urinary'),
    # 生殖
    (['testis', 'prostate', 'penis', 'ovary', 'uterus', 'vagina', 'seminal', 'epididymis', 'scrotum', 'vulva', 'deferent'], 'reproductive'),
    # 内分泌
    (['thyroid gland', 'adrenal gland', 'pituitary', 'pineal', 'parathyroid', 'islet'], 'endocrine'),
    # 淋巴
    (['spleen', 'lymph', 'thymus', 'tonsil'], 'lymphatic'),
    # 皮肤
    (['skin', 'hair', 'nail', 'epithelium', 'dermis', 'epidermis', 'integument', 'sebaceous', 'sweat'], 'integumentary'),
    # 肌肉
    (['muscle', 'tendon', 'fascia', 'rectus', 'oblique', 'vastus', 'trapezius', 'pectoralis', 'levator', 'adductor', 'flexor', 'pronator', 'aponeurosis', 'muscular'], 'muscular'),
    # 骨骼 (最后兜底)
    (['bone', 'vertebra', 'skull', 'rib', 'sternum', 'xiphoid', 'spine', 'sacrum', 'phalanx', 'femur', 'tibia', 'hip bone', 'hyoid', 'clavicle', 'scapula', 'condyle', 'process', 'ligament', 'suture', 'joint', 'articulation', 'cartilage', 'membrane', 'disk', 'disc', 'meniscus'], 'skeletal'),
]

SYSTEM_PRIORITY = ["cardiovascular", "nervous", "respiratory", "digestive", "urinary", "reproductive", "endocrine", "lymphatic", "integumentary", "muscular", "skeletal"]

# 3. 专家级地道医学翻译词典
MEDICAL_DICT = {
    # 核心部位
    "head": "头", "neck": "颈", "trunk": "躯干", "thorax": "胸", "abdomen": "腹", "pelvis": "骨盆",
    "left": "左", "right": "右", "superior": "上", "inferior": "下", "anterior": "前", "posterior": "后",
    "lateral": "外侧", "medial": "内侧", "middle": "中", "internal": "内", "external": "外",
    "deep": "深", "superficial": "浅", "proximal": "近端", "distal": "远端",
    "branch": "支", "tributary": "属支", "trunk": "干", "segment": "段", "lobe": "叶",
    
    # 骨骼肌肉
    "bone": "骨", "cartilage": "软骨", "ligament": "韧带", "joint": "关节", "suture": "缝",
    "process": "突", "fossa": "窝", "foramen": "孔", "canal": "管", "symphysis": "联合",
    "vertebra": "椎骨", "thoracic": "胸", "lumbar": "腰", "sacrum": "骶", "coccyx": "尾",
    "rib": "肋", "sternum": "胸骨", "clavicle": "锁骨", "scapula": "肩胛骨",
    "humerus": "肱骨", "radius": "桡骨", "ulna": "尺骨", "femur": "股骨", "tibia": "胫骨", "fibula": "腓骨",
    "muscle": "肌", "tendon": "腱", "aponeurosis": "腱膜", "fascia": "筋膜",
    
    # 内脏与软组织
    "artery": "动脉", "vein": "静脉", "nerve": "神经", "lymph": "淋巴",
    "stomach": "胃", "liver": "肝脏", "gallbladder": "胆囊", "pancreas": "胰腺",
    "esophagus": "食管", "esophageal": "食管", "duodenum": "十二指肠", "jejunum": "空肠", "ileum": "回肠",
    "colon": "结肠", "rectum": "直肠", "appendix": "阑尾", "pharynx": "咽",
    "heart": "心脏", "lung": "肺", "kidney": "肾脏", "bladder": "膀胱", "ureter": "输尿管",
    "testis": "睾丸", "prostate": "前列腺", "uterus": "子宫", "ovary": "卵巢",
    "skin": "皮肤", "hair": "毛发", "tooth": "牙", "teeth": "牙齿", "tongue": "舌",
    "retina": "视网膜", "cornea": "角膜", "iris": "虹膜", "lens": "晶状体", "sclera": "巩膜",
    "brain": "脑", "cerebrum": "端脑", "cerebellum": "小脑", "pons": "脑桥", "medulla": "延髓",
    "caudate lobe": "尾状叶", "portal vein": "门静脉", "pulmonary trunk": "肺动脉干",
}

def translate_expert(en):
    original_en = en
    en = en.lower()
    
    # 处理 "branch of", "tributary of" 结构
    for conn in [" branch of ", " tributary of ", " part of ", " subdivision of "]:
        if conn in en:
            parts = en.split(conn)
            return translate_expert(parts[1]) + translate_expert(parts[0])
            
    # 词组匹配
    words = en.replace(',', '').replace('(', '').replace(')', '').split()
    res = []
    for w in words:
        if w in MEDICAL_DICT:
            res.append(MEDICAL_DICT[w])
        elif w.endswith('s') and w[:-1] in MEDICAL_DICT:
            res.append(MEDICAL_DICT[w[:-1]])
        else:
            # 兜底翻译 (首字母大写)
            res.append(w.capitalize())
    
    final_name = "".join(res)
    # 清理多余词汇
    final_name = final_name.replace("骨骨", "骨").replace("肌肌", "肌").replace("动脉动脉", "动脉").replace("静脉静脉", "静脉")
    return final_name

final_data = {
    "skeletal": [], "muscular": [], "cardiovascular": [], "nervous": [],
    "digestive": [], "respiratory": [], "urinary": [], "reproductive": [],
    "endocrine": [], "lymphatic": [], "integumentary": [], "other": []
}

sys_names = {k: v for k, v in zip(final_data.keys(), ["骨骼系统", "肌肉系统", "心血管系统", "神经系统", "消化系统", "呼吸系统", "泌尿系统", "生殖系统", "内分泌系统", "淋巴系统", "皮肤系统", "其他"])}

for fj_id in sorted(fj_to_fmas.keys()):
    fmas = fj_to_fmas[fj_id]
    
    # 1. 识别系统 (全量匹配)
    sys_code = "other"
    matched_systems = set()
    for fma in fmas:
        info = fma_info.get(fma)
        if not info: continue
        en_name = info['en'].lower()
        for keywords, code in SYSTEM_RULES:
            if any(k in en_name for k in keywords):
                matched_systems.add(code)
    
    if matched_systems:
        for p in SYSTEM_PRIORITY:
            if p in matched_systems:
                sys_code = p
                break
                
    # 2. 选取最具体的名称
    best_fma = fmas[0]
    max_score = -1
    for fma in fmas:
        info = fma_info.get(fma)
        if not info: continue
        en = info['en'].lower()
        score = len(en)
        # 排除非常模糊的词
        if any(x == en for x in ["organ component", "cardinal organ part", "organ", "anatomical entity", "physical anatomical entity"]):
            score = 0
        if "left" in en or "right" in en: score += 50
        if score > max_score:
            max_score = score
            best_fma = fma
            
    info = fma_info.get(best_fma)
    nameEn = info['en']
    nameCn = translate_expert(nameEn)
    
    # 3. 针对性修复“其他”中常见的错误
    if "bone" in nameEn.lower() and sys_code == "other": sys_code = "skeletal"
    if "muscle" in nameEn.lower() and sys_code == "other": sys_code = "muscular"
    if "artery" in nameEn.lower() or "vein" in nameEn.lower(): sys_code = "cardiovascular"
    if "tooth" in nameEn.lower() or "teeth" in nameEn.lower(): sys_code = "digestive"

    final_data[sys_code].append({
        "id": fj_id,
        "name": f"{nameCn} | {nameEn}",
        "system": sys_names[sys_code],
        "nameEn": nameEn,
        "nameCn": nameCn
    })

with open('data/anatomy_data_simple_refined.json', 'w', encoding='utf-8') as f:
    json.dump(final_data, f, ensure_ascii=False, indent=2)

for k, v in final_data.items():
    print(f"{k}: {len(v)}")
