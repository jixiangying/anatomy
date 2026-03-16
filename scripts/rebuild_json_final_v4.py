import json
import csv

# 1. 加载原始数据
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

# 2. 扩充禁术语列表，确保命名具体
FORBIDDEN_NAMES = {
    "irregular bone", "long bone", "flat bone", "short bone", "sesamoid bone",
    "bone organ", "organ component", "cardinal organ part", "organ", "organ part",
    "anatomical entity", "physical anatomical entity", "material anatomical entity",
    "anatomical structure", "organ segment", "organ component layer", "organ chamber",
    "set of organs", "anatomical set", "cell part cluster", "musculature", "system",
    "body part", "organ system", "region of organ", "region of organ component",
    "anatomical space", "anatomical line", "anatomical point", "organism",
    "muscle organ", "muscle of neck", "muscle of head", "nerve", "vein", "artery",
    "pneumatic bone", "viscus", "material physical anatomical entity", "zone of small intestine"
}

SYSTEM_MAP = {
    "skeletal": "骨骼系统", "muscular": "肌肉系统", "cardiovascular": "心血管系统",
    "nervous": "神经系统", "digestive": "消化系统", "respiratory": "呼吸系统",
    "urinary": "泌尿系统", "reproductive": "生殖系统", "endocrine": "内分泌系统",
    "lymphatic": "淋巴系统", "integumentary": "皮肤系统", "other": "其他"
}

# 优先级顺序：临床重要系统优先识别
SYSTEM_PRIORITY = ["cardiovascular", "nervous", "respiratory", "digestive", "urinary", "reproductive", "endocrine", "lymphatic", "muscular", "integumentary", "skeletal"]

def get_refined_system(en, kj):
    en = en.lower()
    kj = kj
    
    # Cardiovascular
    if any(x in en for x in ["artery", "vein", "vessel", "aorta", "atrium", "ventricle", "vascular", "sinus", "cardiac", "heart", "portal", "capillary", "anastomosis", "plexus of veins"]): return "cardiovascular"
    if any(x in kj for x in ["動脈", "静脈", "心", "血管"]): return "cardiovascular"
    
    # Nervous
    if any(x in en for x in ["nerve", "ganglion", "plexus", "brain", "thalamus", "pons", "medulla", "cerebr", "hippocampus", "amygdala", "retina", "cornea", "iris", "lens", "ciliary", "optic", "sclera", "lacrimal"]): return "nervous"
    if any(x in kj for x in ["神経", "脳", "網膜", "角膜", "虹彩"]): return "nervous"
    
    # Respiratory
    if any(x in en for x in ["lung", "trachea", "bronch", "larynx", "epiglottis", "vocal", "pleura", "nasal cartilage", "choana", "nasopharynx"]): return "respiratory"
    if any(x in kj for x in ["肺", "気管", "喉頭"]): return "respiratory"
    
    # Digestive
    if any(x in en for x in ["esophagus", "stomach", "duodenum", "jejunum", "ileum", "colon", "rectum", "liver", "gallbladder", "pancreas", "biliary", "salivary", "tongue", "pharynx", "appendix", "tooth", "teeth", "dental", "gingiva", "palate", "lip"]): return "digestive"
    if any(x in kj for x in ["食道", "胃", "肝", "膵", "腸", "舌", "歯", "牙"]): return "digestive"
    
    # Urinary
    if any(x in en for x in ["kidney", "ureter", "bladder", "urethra", "renal"]): return "urinary"
    if any(x in kj for x in ["腎", "尿"]): return "urinary"
    
    # Reproductive
    if any(x in en for x in ["testis", "prostate", "penis", "ovary", "uterus", "vagina", "seminal", "epididymis", "scrotum", "vulva"]): return "reproductive"
    if any(x in kj for x in ["精巣", "卵巣", "子宮", "前立腺"]): return "reproductive"
    
    # Endocrine
    if any(x in en for x in ["thyroid gland", "adrenal gland", "pituitary", "pineal", "parathyroid", "islet"]): return "endocrine"
    if any(x in kj for x in ["甲状腺", "副腎", "下垂体"]): return "endocrine"
    
    # Lymphatic
    if any(x in en for x in ["spleen", "lymph", "thymus", "tonsil"]): return "lymphatic"
    if any(x in kj for x in ["脾", "リンパ"]): return "lymphatic"
    
    # Muscular
    if any(x in en for x in ["muscle", "tendon", "fascia", "rectus", "oblique", "vastus", "trapezius", "pectoralis", "levator", "adductor", "flexor", "pronator", "aponeurosis"]): return "muscular"
    if any(x in kj for x in ["肌", "筋", "腱"]): return "muscular"
    
    # Integumentary
    if any(x in en for x in ["skin", "hair", "nail", "epithelium", "dermis", "epidermis", "integument"]): return "integumentary"
    if any(x in kj for x in ["皮膚", "毛", "爪"]): return "integumentary"
    
    # Skeletal
    if any(x in en for x in ["bone", "vertebra", "skull", "rib", "sternum", "xiphoid", "spine", "sacrum", "phalanx", "femur", "tibia", "hip bone", "hyoid", "clavicle", "scapula", "condyle", "process of", "ligament", "suture", "joint", "articulation"]): return "skeletal"
    if any(x in kj for x in ["骨", "椎", "突起", "靭帯", "関節", "縫合"]): return "skeletal"
    
    return "other"

def translate(en, kj):
    res = kj.split(';')[0].split('|')[0]
    if res.lower() == en.lower() or not any(ord(c) > 127 for c in res):
        mapping = {
            "left": "左", "right": "右", "superior": "上", "inferior": "下",
            "anterior": "前", "posterior": "后", "lateral": "外侧", "medial": "内侧",
            "branch": "支", "tributary": "属支", "segment": "段", "artery": "动脉",
            "vein": "静脉", "nerve": "神经", "muscle": "肌", "bone": "骨",
            "tooth": "牙", "teeth": "牙齿", "skin": "皮肤", "ligament": "韧带",
            "vertebra": "椎骨", "thoracic": "胸", "lumbar": "腰", "cervical": "颈"
        }
        words = en.replace(' of ', ' ').replace(' the ', ' ').split()
        translated = "".join([mapping.get(w.lower(), w.capitalize()) for w in words])
        return translated
    
    res = res.replace("頚", "颈").replace("頸", "颈").replace("顔", "面").replace("頭", "头")
    res = res.replace("筋", "肌").replace("膵", "胰").replace("腎", "肾").replace("臟", "脏").replace("臓", "脏")
    res = res.replace("腸", "肠").replace("歯", "牙").replace("皮膚", "皮肤")
    return res

final_data = {k: [] for k in SYSTEM_MAP.keys()}

for fj_id in sorted(fj_to_fmas.keys()):
    fmas = fj_to_fmas[fj_id]
    
    # 选最佳 FMA
    best_fma = None
    best_score = -1
    for fma in fmas:
        info = fma_info.get(fma)
        if not info: continue
        name_en = info['en'].lower()
        score = 0
        if name_en in FORBIDDEN_NAMES: score = 0
        else:
            score = 100 + len(name_en)
            if "left" in name_en or "right" in name_en: score += 50
            if any(ord(c) > 127 for c in info['kanji']): score += 30
        if score > best_score:
            best_score = score
            best_fma = fma
            
    if not best_fma: best_fma = fmas[0]
    
    info = fma_info.get(best_fma)
    nameEn = info['en']
    nameCn = translate(nameEn, info['kanji'])
    
    # 选系统
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

print("--- 重新分类统计 (v4) ---")
for k, v in final_data.items():
    print(f"{k}: {len(v)}")
