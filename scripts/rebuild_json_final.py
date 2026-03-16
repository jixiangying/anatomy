import json
import csv

# Load raw FMA/FJ data to get the most accurate mapping possible
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

# LLM-based robust classification logic
SYSTEM_MAP = {
    "skeletal": "骨骼系统", "muscular": "肌肉系统", "cardiovascular": "心血管系统",
    "nervous": "神经系统", "digestive": "消化系统", "respiratory": "呼吸系统",
    "urinary": "泌尿系统", "reproductive": "生殖系统", "endocrine": "内分泌系统",
    "lymphatic": "淋巴系统", "integumentary": "皮肤系统", "other": "其他"
}

def get_refined_system(en, kj):
    en = en.lower()
    # Priority classification based on anatomical knowledge
    if any(x in en for x in ["artery", "vein", "aorta", "atrium", "ventricle", "vascular", "sinus", "cardiac", "heart", "portal", "vessel", "capillary", "anastomosis"]): return "cardiovascular"
    if any(x in en for x in ["muscle", "tendon", "fascia", "rectus", "oblique", "vastus", "trapezius", "pectoralis", "levator", "adductor", "flexor", "pronator", "iliococcygeus", "puborectalis", "longus colli", "sternothyroid", "omohyoid", "sternohyoid"]): return "muscular"
    if any(x in en for x in ["nerve", "ganglion", "plexus", "brain", "thalamus", "pons", "medulla", "cerebr", "hippocampus", "amygdala", "retina", "cornea", "iris", "lens", "ciliary", "optic", "sclera", "lacrimal"]): return "nervous"
    if any(x in en for x in ["bone", "vertebra", "skull", "rib", "sternum", "xiphoid", "spine", "sacrum", "phalanx", "femur", "tibia", "hip bone", "hyoid", "clavicle", "scapula"]): return "skeletal"
    if any(x in en for x in ["lung", "trachea", "bronch", "larynx", "epiglottis", "vocal", "pleura", "nasal cartilage"]): return "respiratory"
    if any(x in en for x in ["esophagus", "stomach", "duodenum", "jejunum", "ileum", "colon", "rectum", "liver", "gallbladder", "pancreas", "biliary", "salivary", "tongue", "pharynx", "appendix"]): return "digestive"
    if any(x in en for x in ["kidney", "ureter", "bladder", "urethra", "renal"]): return "urinary"
    if any(x in en for x in ["testis", "prostate", "penis", "ovary", "uterus", "vagina", "seminal", "epididymis"]): return "reproductive"
    if any(x in en for x in ["thyroid gland", "adrenal gland", "pituitary", "pineal", "parathyroid"]): return "endocrine"
    if any(x in en for x in ["spleen", "lymph", "thymus"]): return "lymphatic"
    if any(x in en for x in ["skin", "hair", "nail", "epithelium"]): return "integumentary"
    
    # Check Kanji if English fails
    if any(x in kj for x in ["動脈", "静脈", "心", "血管"]): return "cardiovascular"
    if any(x in kj for x in ["筋", "腱"]): return "muscular"
    if any(x in kj for x in ["神経", "脳", "網膜", "角膜"]): return "nervous"
    if any(x in kj for x in ["骨", "椎"]): return "skeletal"
    if any(x in kj for x in ["肺", "気管"]): return "respiratory"
    if any(x in kj for x in ["食道", "胃", "肝", "膵", "腸"]): return "digestive"
    
    return "other"

def refine_translation(en, kj):
    # LLM translation rules for professional medical terms
    res = kj.split(';')[0].split('|')[0]
    # Handle known issues where Kanji is just English or missing
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
        
    # Standard terminology cleaning
    res = res.replace("頚", "颈").replace("頸", "颈").replace("顔", "面").replace("頭", "头")
    res = res.replace("筋", "肌").replace("膵", "胰").replace("腎", "肾").replace("臟", "脏").replace("臓", "脏")
    res = res.replace("腸", "肠").replace("臍", "脐").replace("繋", "系").replace("鞁", "鞁")
    return res

final_data = {k: [] for k in SYSTEM_MAP.keys()}

for fj_id in sorted(fj_fma_map.keys()):
    fmas = fj_fma_map[fj_id]
    
    # Determine System (search all FMAs to find a valid one)
    sys_code = "other"
    for fma in fmas:
        info = fma_info.get(fma)
        if info:
            temp_sys = get_refined_system(info['en'], info['kanji'])
            if temp_sys != "other":
                sys_code = temp_sys
                break
    
    # Determine best name
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
