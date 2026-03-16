import json
import csv
import os

SYSTEMS = {
    "skeletal": "骨骼系统",
    "muscular": "肌肉系统",
    "cardiovascular": "心血管系统",
    "nervous": "神经系统",
    "digestive": "消化系统",
    "respiratory": "呼吸系统",
    "urinary": "泌尿系统",
    "reproductive": "生殖系统",
    "endocrine": "内分泌系统",
    "lymphatic": "淋巴系统",
    "integumentary": "皮肤系统",
    "other": "其他"
}

GENERIC_NAMES = [
    "anatomical entity", "physical anatomical entity", "material anatomical entity",
    "organ", "organ part", "organ component", "cardinal organ part",
    "set of organs", "anatomical set", "anatomical structure", "organ segment",
    "organ component layer", "organ chamber", "material physical anatomical entity",
    "region of organ", "region of organ component", "anatomical space", "anatomical line",
    "anatomical point", "cell part cluster", "musculature", "system", "body part",
    "organ system", "set of", "region of layer of wall of eyeball", "organism"
]

def classify(en, kanji):
    en = en.lower()
    kj = kanji
    
    # Priority 1: Cardiovascular
    if any(x in en for x in ["artery", "vein", "aorta", "atrium", "ventricle", "sinus", "cardiac", "heart", "pulmonary trunk", "portal vein", "anastomosis", "arch of", "vascular", "carotid", "vena cava", "vessel"]):
        return "cardiovascular"
    if any(x in kj for x in ["動脈", "静脈", "心臓", "血管", "大動脈", "心", "房", "室", "静脈洞"]):
        return "cardiovascular"
    
    # Priority 2: Nervous
    if any(x in en for x in ["nerve", "ganglion", "plexus", "brain", "cerebr", "thalamus", "hypothalamus", "pons", "medulla", "spinal cord", "hippocampus", "amygdala", "callosum", "matter", "hemisphere", "retina", "optic", "iris", "cornea", "lens", "ciliary", "sclera", "vitreous", "eyeball"]):
        return "nervous"
    if any(x in kj for x in ["神経", "脳", "丘脳", "終板", "乳頭体", "橋", "網膜", "角膜", "虹彩", "水晶体", "強膜", "脈絡膜"]):
        return "nervous"
        
    # Priority 3: Muscular
    if any(x in en for x in ["muscle", "musculature", "tendon", "fascia", "aponeurosis", "rectus", "oblique", "vastus", "trapezius", "pectoralis", "levator", "adductor", "flexor", "pronator", "iliococcygeus", "pubococcygeus", "puborectalis", "longus colli", "muscular"]):
        return "muscular"
    if any(x in kj for x in ["筋", "腱", "腱輪"]):
        return "muscular"

    # Priority 4: Skeletal
    if any(x in en for x in ["bone", "vertebra", "skull", "rib", "sternum", "xiphoid process", "spine", "sacrum", "coccyx", "phalanx", "clavicle", "scapula", "humerus", "radius", "ulna", "carpal", "metacarpal", "femur", "tibia", "fibula", "tarsal", "metatarsal", "patella", "hip bone", "hyoid", "skeletal"]):
        return "skeletal"
    if any(x in kj for x in ["骨", "椎", "肋", "剣状突起", "頭蓋"]):
        return "skeletal"

    # Priority 5: Respiratory
    if any(x in en for x in ["lung", "trachea", "bronch", "larynx", "epiglottis", "vocal", "cricoid", "thyroid cartilage", "pleura", "nasopharynx", "oropharynx", "laryngopharynx", "nasolacrimal"]):
        return "respiratory"
    if any(x in kj for x in ["肺", "気管", "喉頭", "会厭", "輪状軟骨", "甲状軟骨"]):
        return "respiratory"

    # Priority 6: Digestive
    if any(x in en for x in ["esophagus", "stomach", "duodenum", "jejunum", "ileum", "cecum", "appendix", "colon", "rectum", "liver", "gallbladder", "pancreas", "salivary", "parotid", "sublingual", "submandibular", "tongue", "tooth", "pharynx", "lip", "hepatic duct", "digestive"]):
        return "digestive"
    if any(x in kj for x in ["食道", "胃", "十二指腸", "小腸", "大腸", "直腸", "肝", "胆", "膵", "唾液", "舌", "歯", "唇", "咽頭"]):
        return "digestive"

    # Priority 7: Urinary
    if any(x in en for x in ["kidney", "ureter", "bladder", "urethra", "renal", "urinary"]):
        return "urinary"
    if any(x in kj for x in ["腎", "尿"]):
        return "urinary"

    # Priority 8: Reproductive
    if any(x in en for x in ["testis", "epididymis", "deferent duct", "seminal vesicle", "prostate", "penis", "scrotum", "ovary", "uterus", "uterine", "vagina", "vulva", "reproductive"]):
        return "reproductive"
    if any(x in kj for x in ["精巣", "副精巣", "輸精管", "精嚢", "前立腺", "陰茎", "卵巣", "子宮", "腟"]):
        return "reproductive"

    # Priority 9: Endocrine
    if any(x in en for x in ["thyroid gland", "adrenal gland", "pituitary", "pineal", "parathyroid", "islet"]):
        return "endocrine"
    if any(x in kj for x in ["甲状腺", "副甲状腺", "腎上腺", "下垂体", "松果体"]):
        return "endocrine"

    # Priority 10: Lymphatic
    if any(x in en for x in ["spleen", "lymph", "thymus", "tonsil"]):
        return "lymphatic"
    if any(x in kj for x in ["脾", "リンパ", "胸腺"]):
        return "lymphatic"

    # Priority 11: Integumentary
    if any(x in en for x in ["skin", "hair", "nail"]):
        return "integumentary"
    if any(x in kj for x in ["皮膚", "毛", "爪"]):
        return "integumentary"

    return "other"

def translate(kanji, en):
    kj = kanji.split(';')[0].split('|')[0]
    if kj.lower() == en.lower(): return en.capitalize()
    
    mapping = {
        "筋": "肌", "腱": "腱", "靭帯": "韧带", "骨": "骨", "椎": "椎",
        "動脈": "动脉", "静脈": "静脉", "幹": "干", "枝": "支", "弓": "弓",
        "房": "房", "室": "室", "洞": "洞", "孔": "孔", "窩": "窝",
        "突起": "突", "粗隆": "粗隆", "隆起": "隆起", "管": "管", "道": "道",
        "系": "系", "網": "网", "叢": "丛", "神経": "神经", "脳": "脑",
        "橋": "桥", "肺": "肺", "胃": "胃", "脾": "脾", "肝": "肝",
        "胆": "胆", "膵": "胰", "腎": "肾", "尿": "尿", "膀胱": "膀胱",
        "睾丸": "睾丸", "精巣": "睾丸", "卵巣": "卵巢", "子宮": "子宫",
        "腟": "阴道", "甲状腺": "甲状腺", "腺": "腺", "皮": "皮",
        "肉": "肉", "膜": "膜", "板": "板", "舌": "舌", "唇": "唇",
        "歯": "牙", "喉": "喉", "咽": "咽", "胸": "胸", "腹": "腹",
        "腰": "腰", "背": "背", "肩": "肩", "腕": "臂", "手": "手",
        "指": "指", "足": "足", "腿": "腿", "膝": "膝", "踵": "踵",
        "上": "上", "下": "下", "前": "前", "後": "后", "内": "内",
        "外": "外", "側": "侧", "深": "深", "浅": "浅", "大": "大",
        "小": "小", "长": "长", "短": "短", "斜": "斜", "横": "横",
        "纵": "纵", "円": "圆", "半": "半", "直": "直", "中": "中",
        "间": "间", "端": "端", "部": "部", "区": "区", "域": "域",
        "层": "层", "皮质": "皮质", "髓质": "髓质", "皮下": "皮下",
        "粘膜": "粘膜", "浆膜": "浆膜", "脏": "脏", "囊": "囊",
        "结节": "结节", "结": "结", "束": "束", "轮": "轮", "周": "周",
        "底": "底", "尖": "尖", "缘": "缘", "角": "角", "裂": "裂",
        "沟": "沟", "缝合": "缝合", "关节": "关节", "圆锥": "圆锥",
        "卵圆": "卵圆", "正中": "正中", "器官": "器官", "血管": "血管",
        "大动脉": "大动脉", "肺静脉": "肺静脉", "肺动脉": "肺动脉",
        "冠状": "冠状", "心脏": "心脏", "心": "心", "眼": "眼",
        "耳": "耳", "鼻": "鼻", "口": "口", "脸": "脸", "发": "发",
        "毛": "毛", "爪": "爪", "皮肤": "皮肤", "皮": "皮", "肤": "肤",
    }
    
    # Simple replacement for common Japanese patterns
    if "膵臓" in kj: kj = kj.replace("膵臓", "胰腺")
    if "腎臓" in kj: kj = kj.replace("腎臓", "肾脏")
    if "肝臓" in kj: kj = kj.replace("肝臓", "肝脏")
    if "心臓" in kj: kj = kj.replace("心臓", "心脏")
    if "脾臓" in kj: kj = kj.replace("脾臓", "脾")
    if "精巣" in kj: kj = kj.replace("精巣", "睾丸")
    if "卵巣" in kj: kj = kj.replace("卵巣", "卵巢")
    if "子宮" in kj: kj = kj.replace("子宮", "子宫")
    if "前立腺" in kj: kj = kj.replace("前立腺", "前列腺")
    if "靭帯" in kj: kj = kj.replace("靭帯", "韧带")

    res = ""
    i = 0
    while i < len(kj):
        char = kj[i]
        res += mapping.get(char, char)
        i += 1
    
    # Final manual touch-ups
    res = res.replace("頚", "颈").replace("頸", "颈").replace("顔", "面")
    res = res.replace("頭", "头").replace("腸", "肠").replace("膵", "胰")
    res = res.replace("腎", "肾").replace("臟", "脏").replace("臓", "脏")
    res = res.replace("臍", "脐").replace("繋", "系")
    
    if res == kj and any(ord(c) < 128 for c in kj) and len(kj) > 0:
        return en.capitalize()
    return res

# 1. Load FMA metadata
fma_info = {}
with open('data/isa_parts_list.txt', 'r') as f:
    reader = csv.DictReader(f, delimiter='\t')
    for row in reader:
        fma_info[row['concept id']] = {
            'en': row['en'],
            'kanji': row['kanji']
        }

# 2. Load all FMAs for each FJ, and pick the best one
fj_fma_map = {}
with open('data/isa_element_parts.txt', 'r') as f:
    reader = csv.DictReader(f, delimiter='\t')
    for row in reader:
        fj = row['element file id']
        fma = row['concept id']
        name = row['name'].lower()
        if fj not in fj_fma_map:
            fj_fma_map[fj] = []
        fj_fma_map[fj].append((fma, name))

def get_best_fma(fmas):
    # Sort by specificity: non-generic names are better
    specific = []
    for fma, name in fmas:
        is_generic = any(g in name for g in GENERIC_NAMES)
        if not is_generic:
            specific.append((fma, name))
    
    if specific:
        # Sort by length of name (usually more specific is longer)
        specific.sort(key=lambda x: len(x[1]), reverse=True)
        return specific[0][0]
    
    # If all are generic, pick the one with longest name
    fmas.sort(key=lambda x: len(x[1]), reverse=True)
    return fmas[0][0]

# 3. Process
new_data = {k: [] for k in SYSTEMS.keys()}
for fj_id in sorted(fj_fma_map.keys()):
    best_fma = get_best_fma(fj_fma_map[fj_id])
    info = fma_info.get(best_fma, {'en': 'unknown', 'kanji': 'unknown'})
    
    en = info['en']
    kanji = info['kanji']
    
    sys_code = classify(en, kanji)
    nameCn = translate(kanji, en)
    
    item = {
        "id": fj_id,
        "name": f"{nameCn} | {en}",
        "system": SYSTEMS[sys_code],
        "nameEn": en,
        "nameCn": nameCn
    }
    new_data[sys_code].append(item)

with open('data/anatomy_data_simple_new.json', 'w', encoding='utf-8') as f:
    json.dump(new_data, f, ensure_ascii=False, indent=2)

for k, v in new_data.items():
    print(f"{k}: {len(v)}")
