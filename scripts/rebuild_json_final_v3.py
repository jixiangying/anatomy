import json
import csv

# 1. 加载原始 FMA 详细信息 (en, kanji)
fma_info = {}
with open('data/isa_parts_list.txt', 'r', encoding='utf-8') as f:
    for row in csv.DictReader(f, delimiter='\t'):
        fma_info[row['concept id']] = {'en': row['en'], 'kanji': row['kanji']}

# 2. 建立 FJ 到所有关联 FMA 的完整映射
fj_to_fmas = {}
with open('data/isa_element_parts.txt', 'r', encoding='utf-8') as f:
    for row in csv.DictReader(f, delimiter='\t'):
        fj = row['element file id']
        fma = row['concept id']
        if fj not in fj_to_fmas: fj_to_fmas[fj] = []
        fj_to_fmas[fj].append(fma)

# 3. 定义解剖学中的“类名”或“抽象名”，这些绝对不能作为最终名称
FORBIDDEN_NAMES = {
    "irregular bone", "long bone", "flat bone", "short bone", "sesamoid bone",
    "bone organ", "organ component", "cardinal organ part", "organ", "organ part",
    "anatomical entity", "physical anatomical entity", "material anatomical entity",
    "anatomical structure", "organ segment", "organ component layer", "organ chamber",
    "set of organs", "anatomical set", "cell part cluster", "musculature", "system",
    "body part", "organ system", "region of organ", "region of organ component",
    "anatomical space", "anatomical line", "anatomical point", "organism",
    "muscle organ", "muscle of neck", "muscle of head", "nerve", "vein", "artery",
    "pneumatic bone", "viscus", "material physical anatomical entity"
}

SYSTEM_MAP = {
    "skeletal": "骨骼系统", "muscular": "肌肉系统", "cardiovascular": "心血管系统",
    "nervous": "神经系统", "digestive": "消化系统", "respiratory": "呼吸系统",
    "urinary": "泌尿系统", "reproductive": "生殖系统", "endocrine": "内分泌系统",
    "lymphatic": "淋巴系统", "integumentary": "皮肤系统", "other": "其他"
}

SYSTEM_PRIORITY = ["cardiovascular", "nervous", "muscular", "respiratory", "digestive", "urinary", "reproductive", "endocrine", "lymphatic", "integumentary", "skeletal"]

def get_refined_system(en, kj):
    en = en.lower()
    if any(x in en for x in ["artery", "vein", "vessel", "aorta", "atrium", "ventricle", "vascular", "sinus", "cardiac", "heart", "portal", "capillary", "anastomosis"]): return "cardiovascular"
    if any(x in en for x in ["nerve", "ganglion", "brain", "thalamus", "pons", "medulla", "cerebr", "hippocampus", "amygdala", "retina", "cornea", "iris", "lens", "ciliary", "optic", "sclera", "lacrimal"]): return "nervous"
    if any(x in en for x in ["muscle", "tendon", "fascia", "rectus", "oblique", "vastus", "trapezius", "pectoralis", "levator", "adductor", "flexor", "pronator"]): return "muscular"
    if any(x in en for x in ["lung", "trachea", "bronch", "larynx", "epiglottis", "vocal", "pleura", "nasal cartilage"]): return "respiratory"
    if any(x in en for x in ["esophagus", "stomach", "duodenum", "jejunum", "ileum", "colon", "rectum", "liver", "gallbladder", "pancreas", "biliary", "salivary", "tongue", "pharynx"]): return "digestive"
    if any(x in en for x in ["kidney", "ureter", "bladder", "urethra", "renal"]): return "urinary"
    if any(x in en for x in ["testis", "prostate", "penis", "ovary", "uterus", "vagina", "seminal", "epididymis"]): return "reproductive"
    if any(x in en for x in ["bone", "vertebra", "skull", "rib", "sternum", "xiphoid", "spine", "sacrum", "phalanx", "femur", "tibia", "hip bone", "hyoid", "clavicle", "scapula"]): return "skeletal"
    return "other"

def translate(en, kj):
    res = kj.split(';')[0].split('|')[0]
    # 如果汉字无效或是纯英文，则进行LLM翻译
    if res.lower() == en.lower() or not any(ord(c) > 127 for c in res):
        mapping = {
            "left": "左", "right": "右", "superior": "上", "inferior": "下",
            "anterior": "前", "posterior": "后", "lateral": "外侧", "medial": "内侧",
            "branch": "支", "tributary": "属支", "segment": "段", "artery": "动脉",
            "vein": "静脉", "nerve": "神经", "muscle": "肌", "bone": "骨",
            "skeletal": "骨骼", "zygomatic": "颧", "maxilla": "上颌", "mandible": "下颌",
            "sphenoid": "蝶", "ethmoid": "筛", "frontal": "额", "parietal": "顶",
            "occipital": "枕", "temporal": "颞", "vertebra": "椎骨", "cervical": "颈",
            "thoracic": "胸", "lumbar": "腰", "sacrum": "骶", "coccyx": "尾",
            "rib": "肋", "sternum": "胸骨", "clavicle": "锁骨", "scapula": "肩胛"
        }
        words = en.replace(' of ', ' ').replace(' the ', ' ').split()
        translated = "".join([mapping.get(w.lower(), w.capitalize()) for w in words])
        return translated
    
    # 规范化汉字
    res = res.replace("頚", "颈").replace("頸", "颈").replace("顔", "面").replace("頭", "头")
    res = res.replace("筋", "肌").replace("膵", "胰").replace("腎", "肾").replace("臟", "脏").replace("臓", "脏")
    return res

final_data = {k: [] for k in SYSTEM_MAP.keys()}

for fj_id in sorted(fj_to_fmas.keys()):
    fmas = fj_to_fmas[fj_id]
    
    # 1. 寻找最具体的 FMA 信息
    best_fma = None
    best_score = -1
    
    for fma in fmas:
        info = fma_info.get(fma)
        if not info: continue
        
        name_en = info['en'].lower()
        score = 0
        
        # 排除禁术语：如果是通用术语，分数大幅降低
        if name_en in FORBIDDEN_NAMES:
            score = 0
        else:
            score = 100
            # 越具体（通常名字越长）分数越高
            score += len(name_en)
            # 包含 Left/Right 或具体骨骼名称的优先
            if "left" in name_en or "right" in name_en: score += 50
            if any(ord(c) > 127 for c in info['kanji']): score += 30 # 有汉字优先
            
        if score > best_score:
            best_score = score
            best_fma = fma
            
    if not best_fma: best_fma = fmas[0] # 万一全被排除，取第一个
    
    info = fma_info.get(best_fma)
    nameEn = info['en']
    nameCn = translate(nameEn, info['kanji'])
    
    # 2. 重新确定系统（基于所有关联 FMA）
    sys_code = "other"
    matched_systems = set()
    for fma in fmas:
        f_info = fma_info.get(fma)
        if f_info:
            s = get_refined_system(f_info['en'], f_info['kanji'])
            if s != "other": matched_systems.add(s)
            
    if matched_systems:
        for p in SYSTEM_PRIORITY:
            if p in matched_systems: sys_code = p; break
            
    final_data[sys_code].append({
        "id": fj_id,
        "name": f"{nameCn} | {nameEn}",
        "system": SYSTEM_MAP[sys_code],
        "nameEn": nameEn,
        "nameCn": nameCn
    })

with open('data/anatomy_data_simple_refined.json', 'w', encoding='utf-8') as f:
    json.dump(final_data, f, ensure_ascii=False, indent=2)

print("--- 重新分类与命名统计 ---")
for k, v in final_data.items():
    print(f"{k}: {len(v)}")
