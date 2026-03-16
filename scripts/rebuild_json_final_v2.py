import json
import csv

# 1. 加载原始数据
fma_info = {}
with open('data/isa_parts_list.txt', 'r') as f:
    for row in csv.DictReader(f, delimiter='\t'):
        fma_info[row['concept id']] = {'en': row['en'], 'kanji': row['kanji']}

fj_fma_map = {}
with open('data/isa_element_parts.txt', 'r') as f:
    for row in csv.DictReader(f, delimiter='\t'):
        fj = row['element file id']
        if fj not in fj_fma_map: fj_fma_map[fj] = []
        fj_fma_map[fj].append(row['concept id'])

SYSTEM_MAP = {
    "skeletal": "骨骼系统", "muscular": "肌肉系统", "cardiovascular": "心血管系统",
    "nervous": "神经系统", "digestive": "消化系统", "respiratory": "呼吸系统",
    "urinary": "泌尿系统", "reproductive": "生殖系统", "endocrine": "内分泌系统",
    "lymphatic": "淋巴系统", "integumentary": "皮肤系统", "other": "其他"
}

# 定义严格的优先级顺序：心血管和神经必须排在骨骼前面
# 因为很多血管/神经是以骨骼命名的，必须先识别出它们是血管/神经
SYSTEM_PRIORITY = [
    "cardiovascular", # 包含 vein, artery, vessel
    "nervous",        # 包含 nerve, ganglion
    "muscular",       # 包含 muscle, tendon
    "respiratory",    # 包含 lung, bronchus
    "digestive",      # 包含 stomach, liver, biliary
    "urinary",        # 包含 kidney, bladder
    "reproductive",   # 包含 testis, ovary
    "endocrine",      # 包含 thyroid, adrenal
    "lymphatic",      # 包含 spleen, lymph
    "integumentary",  # 包含 skin
    "skeletal"        # 最后才是骨骼，只有纯粹的骨组织才归入此类
]

def get_refined_system(en, kj):
    en = en.lower()
    kj = kj
    
    # Cardiovascular (Highest priority to avoid mistaking veins for bones)
    if any(x in en for x in ["artery", "vein", "vessel", "aorta", "atrium", "ventricle", "vascular", "sinus", "cardiac", "heart", "portal", "capillary", "anastomosis", "plexus of veins"]): 
        return "cardiovascular"
    if any(x in kj for x in ["動脈", "静脈", "心", "血管", "静脈叢"]): 
        return "cardiovascular"
    
    # Nervous
    if any(x in en for x in ["nerve", "ganglion", "brain", "thalamus", "pons", "medulla", "cerebr", "hippocampus", "amygdala", "retina", "cornea", "iris", "lens", "ciliary", "optic", "sclera", "lacrimal"]): 
        return "nervous"
    if any(x in kj for x in ["神経", "脳", "網膜", "角膜"]): 
        return "nervous"
    
    # Muscular
    if any(x in en for x in ["muscle", "tendon", "fascia", "rectus", "oblique", "vastus", "trapezius", "pectoralis", "levator", "adductor", "flexor", "pronator", "iliococcygeus", "puborectalis", "longus colli"]): 
        return "muscular"
    if any(x in kj for x in ["筋", "腱"]): 
        return "muscular"

    # Respiratory
    if any(x in en for x in ["lung", "trachea", "bronch", "larynx", "epiglottis", "vocal", "pleura", "nasal cartilage"]): return "respiratory"
    if any(x in kj for x in ["肺", "気管"]): return "respiratory"

    # Digestive
    if any(x in en for x in ["esophagus", "stomach", "duodenum", "jejunum", "ileum", "colon", "rectum", "liver", "gallbladder", "pancreas", "biliary", "salivary", "tongue", "pharynx", "appendix"]): return "digestive"
    if any(x in kj for x in ["食道", "胃", "肝", "膵", "腸"]): return "digestive"

    # Urinary
    if any(x in en for x in ["kidney", "ureter", "bladder", "urethra", "renal"]): return "urinary"
    if any(x in kj for x in ["腎", "尿"]): return "urinary"

    # Reproductive
    if any(x in en for x in ["testis", "prostate", "penis", "ovary", "uterus", "vagina", "seminal", "epididymis"]): return "reproductive"
    if any(x in kj for x in ["精巣", "卵巣", "子宮", "前立腺"]): return "reproductive"

    # Skeletal (Now at a lower priority)
    if any(x in en for x in ["bone", "vertebra", "skull", "rib", "sternum", "xiphoid", "spine", "sacrum", "phalanx", "femur", "tibia", "hip bone", "hyoid", "clavicle", "scapula", "condyle", "process of"]): return "skeletal"
    if any(x in kj for x in ["骨", "椎", "肋", "突起"]): return "skeletal"

    # Other systems
    if any(x in en for x in ["thyroid gland", "adrenal gland", "pituitary", "pineal"]): return "endocrine"
    if any(x in en for x in ["spleen", "lymph", "thymus"]): return "lymphatic"
    if any(x in en for x in ["skin", "hair", "nail", "epithelium"]): return "integumentary"
    
    return "other"

def refine_translation(en, kj):
    # 使用LLM翻译逻辑规范化医学词汇
    res = kj.split(';')[0].split('|')[0]
    if res.lower() == en.lower() or not any(ord(c) > 127 for c in res):
        mapping = {
            "left": "左", "right": "右", "superior": "上", "inferior": "下",
            "anterior": "前", "posterior": "后", "lateral": "外侧", "medial": "内侧",
            "branch": "支", "tributary": "属支", "segment": "段", "artery": "动脉",
            "vein": "静脉", "nerve": "神经", "muscle": "肌", "bone": "骨",
            "bronchial tree": "支气管树", "hepatic": "肝", "biliary": "胆", "cardiac": "心",
            "temporal": "颞", "occipital": "枕", "frontal": "额", "parietal": "顶",
            "basal": "底", "apical": "尖"
        }
        words = en.replace(' of ', ' ').replace(' the ', ' ').split()
        translated = "".join([mapping.get(w.lower(), w.capitalize()) for w in words])
        return translated
        
    res = res.replace("頚", "颈").replace("頸", "颈").replace("顔", "面").replace("頭", "头")
    res = res.replace("筋", "肌").replace("膵", "胰").replace("腎", "肾").replace("臟", "脏").replace("臓", "脏")
    res = res.replace("腸", "肠").replace("臍", "脐").replace("繋", "系")
    return res

final_data = {k: [] for k in SYSTEM_MAP.keys()}

for fj_id in sorted(fj_fma_map.keys()):
    fmas = fj_fma_map[fj_id]
    
    # 基于优先级确定系统
    sys_code = "other"
    matched_systems = set()
    for fma in fmas:
        info = fma_info.get(fma)
        if info:
            temp_sys = get_refined_system(info['en'], info['kanji'])
            if temp_sys != "other":
                matched_systems.add(temp_sys)
    
    if matched_systems:
        # 按优先级列表选取
        for p in SYSTEM_PRIORITY:
            if p in matched_systems:
                sys_code = p
                break
    
    # 选取最佳名称
    best_fma = fmas[0]
    for fma in fmas:
        info = fma_info.get(fma)
        if info and any(ord(c) > 127 for c in info['kanji']):
            best_fma = fma
            break
            
    info = fma_info.get(best_fma)
    nameCn = refine_translation(info['en'], info['kanji'])
    nameEn = info['en']
    
    item = {
        "id": fj_id,
        "name": f"{nameCn} | {nameEn}",
        "system": SYSTEM_MAP[sys_code],
        "nameEn": nameEn,
        "nameCn": nameCn
    }
    final_data[sys_code].append(item)

with open('data/anatomy_data_simple_refined.json', 'w', encoding='utf-8') as f:
    json.dump(final_data, f, ensure_ascii=False, indent=2)

for k, v in final_data.items():
    print(f"{k}: {len(v)}")
