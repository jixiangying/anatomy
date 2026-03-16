import json
import csv
import os

# FMA to System mapping heuristics based on keywords in EN and Kanji
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

def classify(en, kanji):
    en = en.lower()
    kj = kanji
    
    # Priority 1: Cardiovascular
    if any(x in en for x in ["artery", "vein", "aorta", "atrium", "ventricle", "sinus", "cardiac", "heart", "pulmonary trunk", "portal vein", "anastomosis", "arch of", "vascular", "trunk of...artery", "trunk of...vein", "carotid", "vena cava"]):
        return "cardiovascular"
    if any(x in kj for x in ["動脈", "静脈", "心臓", "血管", "大動脈", "心", "房", "室", "静脈洞"]):
        return "cardiovascular"
    
    # Priority 2: Nervous
    if any(x in en for x in ["nerve", "ganglion", "plexus", "brain", "cerebr", "thalamus", "hypothalamus", "pons", "medulla", "spinal cord", "hippocampus", "amygdala", "callosum", "matter", "hemisphere", "retina", "optic", "iris", "cornea", "lens", "ciliary", "sclera", "vitreous", "chambers of eyeball"]):
        return "nervous"
    if any(x in kj for x in ["神経", "脳", "丘脳", "終板", "乳頭体", "橋", "網膜", "角膜", "虹彩", "水晶体", "強膜", "脈絡膜"]):
        return "nervous"
        
    # Priority 3: Muscular
    if any(x in en for x in ["muscle", "musculature", "tendon", "fascia", "aponeurosis", "rectus", "oblique", "vastus", "trapezius", "pectoralis", "levator", "adductor", "flexor", "pronator", "iliococcygeus", "pubococcygeus", "puborectalis", "longus colli"]):
        return "muscular"
    if any(x in kj for x in ["筋", "腱", "腱輪"]):
        return "muscular"

    # Priority 4: Skeletal
    if any(x in en for x in ["bone", "vertebra", "skull", "rib", "sternum", "xiphoid process", "spine", "sacrum", "coccyx", "phalanx", "clavicle", "scapula", "humerus", "radius", "ulna", "carpal", "metacarpal", "femur", "tibia", "fibula", "tarsal", "metatarsal", "patella", "hip bone", "hyoid"]):
        return "skeletal"
    if any(x in kj for x in ["骨", "椎", "肋", "剣状突起", "頭蓋"]):
        return "skeletal"

    # Priority 5: Respiratory
    if any(x in en for x in ["lung", "trachea", "bronch", "larynx", "epiglottis", "vocal", "cricoid", "thyroid cartilage", "pleura", "nasopharynx", "oropharynx", "laryngopharynx", "nasolacrimal"]):
        return "respiratory"
    if any(x in kj for x in ["肺", "気管", "喉頭", "会厭", "輪状軟骨", "甲状軟骨"]):
        return "respiratory"

    # Priority 6: Digestive
    if any(x in en for x in ["esophagus", "stomach", "duodenum", "jejunum", "ileum", "cecum", "appendix", "colon", "rectum", "liver", "gallbladder", "pancreas", "salivary", "parotid", "sublingual", "submandibular", "tongue", "tooth", "pharynx", "lip", "hepatic duct"]):
        return "digestive"
    if any(x in kj for x in ["食道", "胃", "十二指腸", "小腸", "大腸", "直腸", "肝", "胆", "膵", "唾液", "舌", "歯", "唇", "咽頭"]):
        return "digestive"

    # Priority 7: Urinary
    if any(x in en for x in ["kidney", "ureter", "bladder", "urethra", "renal"]):
        return "urinary"
    if any(x in kj for x in ["腎", "尿"]):
        return "urinary"

    # Priority 8: Reproductive
    if any(x in en for x in ["testis", "epididymis", "deferent duct", "seminal vesicle", "prostate", "penis", "scrotum", "ovary", "uterus", "uterine", "vagina", "vulva"]):
        return "reproductive"
    if any(x in kj for x in ["精巣", "副精巣", "輸精管", "精嚢", "前立腺", "陰茎", "卵巣", "子宮", "腟"]):
        return "reproductive"

    # Priority 9: Endocrine
    if any(x in en for x in ["thyroid gland", "adrenal gland", "pituitary", "pineal", "parathyroid", "islet", "hypothalamus"]): # hypothalamus is both, but let's prefer nervous
        if "hypothalamus" in en: return "nervous"
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
    # Take first kanji if multiple
    kj = kanji.split(';')[0].split('|')[0]
    
    # Map Japanese Kanji to Chinese
    mapping = {
        "筋": "肌",
        "腱": "腱",
        "靭帯": "韧带",
        "骨": "骨",
        "椎": "椎",
        "動脈": "动脉",
        "静脈": "静脉",
        "幹": "干",
        "枝": "支",
        "弓": "弓",
        "房": "房",
        "室": "室",
        "洞": "洞",
        "孔": "孔",
        "窩": "窝",
        "突起": "突",
        "粗隆": "粗隆",
        "隆起": "隆起",
        "管": "管",
        "道": "道",
        "系": "系",
        "網": "网",
        "叢": "丛",
        "神経": "神经",
        "脳": "脑",
        "橋": "桥",
        "肺": "肺",
        "胃": "胃",
        "脾": "脾",
        "肝": "肝",
        "胆": "胆",
        "膵": "胰",
        "腎": "肾",
        "尿": "尿",
        "膀胱": "膀胱",
        "睾丸": "睾丸",
        "精巣": "睾丸",
        "卵巣": "卵巢",
        "子宮": "子宫",
        "腟": "阴道",
        "甲状腺": "甲状腺",
        "腺": "腺",
        "皮": "皮",
        "肉": "肉",
        "膜": "膜",
        "板": "板",
        "舌": "舌",
        "唇": "唇",
        "歯": "牙",
        "喉": "喉",
        "咽": "咽",
        "胸": "胸",
        "腹": "腹",
        "腰": "腰",
        "背": "背",
        "肩": "肩",
        "腕": "臂",
        "手": "手",
        "指": "指",
        "足": "足",
        "腿": "腿",
        "膝": "膝",
        "踵": "踵",
        "上": "上",
        "下": "下",
        "前": "前",
        "後": "后",
        "内": "内",
        "外": "外",
        "側": "侧",
        "深": "深",
        "浅": "浅",
        "大": "大",
        "小": "小",
        "長": "长",
        "短": "短",
        "斜": "斜",
        "横": "横",
        "縦": "纵",
        "円": "圆",
        "半": "半",
        "直": "直",
        "中": "中",
        "間": "间",
        "端": "端",
        "部": "部",
        "区": "区",
        "域": "域",
        "層": "层",
        "皮質": "皮质",
        "髄質": "髓质",
        "皮下": "皮下",
        "粘膜": "粘膜",
        "漿膜": "浆膜",
        "臓": "脏",
        "嚢": "囊",
        "結節": "结节",
        "結": "结",
        "束": "束",
        "輪": "轮",
        "周": "周",
        "底": "底",
        "尖": "尖",
        "縁": "缘",
        "角": "角",
        "裂": "裂",
        "溝": "沟",
        "縫合": "缝合",
        "関節": "关节",
        "円錐": "圆锥",
        "卵円": "卵圆",
        "正中": "正中",
        "浅": "浅",
        "臓器": "器官",
        "器官": "器官",
        "血管": "血管",
        "大動脈": "大动脉",
        "肺静脈": "肺静脉",
        "肺動脈": "肺动脉",
        "冠状": "冠状",
        "心臓": "心脏",
        "心": "心",
        "眼": "眼",
        "耳": "耳",
        "鼻": "鼻",
        "口": "口",
        "顔": "脸",
        "髪": "发",
        "毛": "毛",
        "爪": "爪",
        "皮": "皮",
        "肤": "肤",
        "皮膚": "皮肤",
    }
    
    # Specific terminology overrides
    if "膵臓" in kj: kj = kj.replace("膵臓", "胰腺")
    if "腎臓" in kj: kj = kj.replace("腎臓", "肾脏")
    if "肝臓" in kj: kj = kj.replace("肝臓", "肝脏")
    if "心臓" in kj: kj = kj.replace("心臓", "心脏")
    if "脾臓" in kj: kj = kj.replace("脾臓", "脾")
    if "精巣" in kj: kj = kj.replace("精巣", "睾丸")
    if "卵巣" in kj: kj = kj.replace("卵巣", "卵巢")
    if "子宮" in kj: kj = kj.replace("子宮", "子宫")
    if "腟" in kj: kj = kj.replace("腟", "阴道")
    if "前立腺" in kj: kj = kj.replace("前立腺", "前列腺")
    if "甲状腺" in kj: kj = kj.replace("甲状腺", "甲状腺")
    if "副甲状腺" in kj: kj = kj.replace("副甲状腺", "上皮小体") # usually called 甲状旁腺
    if "副腎" in kj: kj = kj.replace("副腎", "肾上腺")
    if "胸腺" in kj: kj = kj.replace("胸腺", "胸腺")
    if "唾液腺" in kj: kj = kj.replace("唾液腺", "唾液腺")
    if "涙腺" in kj: kj = kj.replace("涙腺", "泪腺")
    
    # Common Kanji conversion
    res = ""
    i = 0
    while i < len(kj):
        found = False
        # Try longer matches first (2 chars)
        if i + 1 < len(kj):
            pair = kj[i:i+2]
            if pair in mapping:
                res += mapping[pair]
                i += 2
                found = True
        if not found:
            char = kj[i]
            if char in mapping:
                res += mapping[char]
            else:
                res += char
            i += 1
    
    # Manual fixes for common anatomy terms that don't translate literally well
    res = res.replace("膵", "胰")
    res = res.replace("腎", "肾")
    res = res.replace("腸", "肠")
    res = res.replace("頚", "颈")
    res = res.replace("頸", "颈")
    res = res.replace("頭", "头")
    res = res.replace("顔", "面")
    res = res.replace("骨盤", "骨盆")
    res = res.replace("鎖骨", "锁骨")
    res = res.replace("肩甲骨", "肩胛骨")
    res = res.replace("大腿", "大腿")
    res = res.replace("下腿", "小腿")
    res = res.replace("上腕", "上臂")
    res = res.replace("前腕", "前臂")
    res = res.replace("手根", "手腕")
    res = res.replace("足根", "足跗")
    res = res.replace("指", "指")
    res = res.replace("趾", "趾")
    res = res.replace("椎", "椎")
    res = res.replace("胸骨", "胸骨")
    res = res.replace("肋骨", "肋骨")
    res = res.replace("脊椎", "脊柱")
    res = res.replace("寛骨", "髋骨")
    res = res.replace("仙骨", "骶骨")
    res = res.replace("尾骨", "尾骨")
    res = res.replace("膝蓋骨", "髌骨")
    res = res.replace("篩骨", "筛骨")
    res = res.replace("蝶形骨", "蝶骨")
    res = res.replace("後頭骨", "枕骨")
    res = res.replace("側頭骨", "颞骨")
    res = res.replace("前頭骨", "额骨")
    res = res.replace("頬骨", "颧骨")
    res = res.replace("上顎骨", "上颌骨")
    res = res.replace("下顎骨", "下颌骨")
    res = res.replace("舌骨", "舌骨")
    res = res.replace("甲状旁腺", "甲状旁腺")
    res = res.replace("上皮小体", "甲状旁腺")
    
    # If the resulting name is just English (no kanji mapping found), use a simpler approach or just return it
    if res == kj and any(ord(c) < 128 for c in kj) and len(kj) > 0:
        # It might be untranslated English in the kanji field
        return en.capitalize()

    return res

# Load FMA data
fma_info = {}
with open('data/isa_parts_list.txt', 'r') as f:
    reader = csv.DictReader(f, delimiter='\t')
    for row in reader:
        fma_info[row['concept id']] = {
            'en': row['en'],
            'kanji': row['kanji'],
            'kana': row['kana']
        }

# Load FJ mapping
fj_to_fma = {}
with open('data/isa_element_parts.txt', 'r') as f:
    reader = csv.DictReader(f, delimiter='\t')
    for row in reader:
        fj_to_fma[row['element file id']] = row['concept id']

# Re-classify all 2234 items
new_data = {k: [] for k in SYSTEMS.keys()}

# Get all unique FJ IDs from isa_element_parts.txt
all_fjs = sorted(fj_to_fma.keys())

for fj_id in all_fjs:
    fma_id = fj_to_fma[fj_id]
    info = fma_info.get(fma_id, {'en': 'unknown', 'kanji': 'unknown'})
    
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

# Save to new JSON
with open('data/anatomy_data_simple_new.json', 'w', encoding='utf-8') as f:
    json.dump(new_data, f, ensure_ascii=False, indent=2)

print("New JSON generated: data/anatomy_data_simple_new.json")
# Print stats
for k, v in new_data.items():
    print(f"{k}: {len(v)}")
