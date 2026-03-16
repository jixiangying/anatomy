import json
import re

mapping = {
    "left": "左", "right": "右", "superior": "上", "inferior": "下",
    "medial": "内侧", "lateral": "外侧", "anterior": "前", "posterior": "后",
    "middle": "中", "distal": "远节", "proximal": "近节",
    "proper palmar digital vein": "掌侧指固有静脉",
    "proper palmar digital artery": "掌侧指固有动脉",
    "proper plantar digital vein": "足底趾固有静脉",
    "proper plantar digital artery": "足底趾固有动脉",
    "common palmar digital artery": "掌侧指总动脉",
    "common palmar digital vein": "掌侧指总静脉",
    "interosseous membrane": "骨间膜",
    "long plantar ligament": "长跖韧带",
    "cricoid cartilage": "环状软骨",
    "cuneiform cartilage": "楔状软骨",
    "arytenoid cartilage": "杓状软骨",
    "corniculate cartilage": "小角软骨",
    "conus elasticus": "弹性圆锥",
    "median cricothyroid ligament": "环甲正中韧带",
    "thyroid cartilage": "甲状软骨",
    "hip bone": "髋骨",
    "xiphoid process": "剑突",
    "vertebra": "椎骨",
    "cervical": "颈", "thoracic": "胸", "lumbar": "腰", "sacral": "骶",
    "sternum": "胸骨",
    "phalanx": "指骨",
    "index finger": "食指", "little finger": "小指", "middle finger": "中指", "ring finger": "无名指", "thumb": "拇指",
    "big toe": "拇趾", "second toe": "第2趾", "third toe": "第3趾", "fourth toe": "第4趾", "little toe": "小趾",
    "pneumatized bone": "含气骨",
    "frontal bone": "额骨",
    "intervertebral disk": "椎间盘",
    "rib": "肋",
    "tenth": "第10", "eleventh": "第11", "twelfth": "第12", "first": "第1", "second": "第2", "third": "第3", "fourth": "第4", "fifth": "第5", "sixth": "第6", "seventh": "第7", "eighth": "第8", "ninth": "第9",
    "clavicle": "锁骨",
    "costal cartilage": "肋软骨",
    "metacarpal bone": "掌骨",
    "metatarsal bone": "跖骨",
    "calcaneus": "跟骨",
    "capitate": "头状骨",
    "cuboid bone": "骰骨",
    "femur": "股骨",
    "fibula": "腓骨",
    "hamate": "钩骨",
    "humerus": "肱骨",
    "inferior nasal concha": "下鼻甲",
    "intermediate cuneiform bone": "中间楔骨",
    "lateral cuneiform bone": "外侧楔骨",
    "medial cuneiform bone": "内侧楔骨",
    "sesamoid bone": "籽骨",
    "lunate": "月骨",
    "maxilla": "上颌骨",
    "nasal bone": "鼻骨",
    "palatine bone": "腭骨",
    "parietal bone": "顶骨",
    "patella": "髌骨",
    "pisiform": "豌豆骨",
    "radius": "桡骨",
    "scaphoid": "手舟骨",
    "scapula": "肩胛骨",
    "talus": "距骨",
    "temporal bone": "颞骨",
    "tibia": "胫骨",
    "trapezium": "大多角骨",
    "trapezoid": "小多角骨",
    "triquetral": "三角骨",
    "ulna": "尺骨",
    "zygomatic bone": "颧骨",
    "mandible": "下颌骨",
    "manubrium": "胸骨柄",
    "navicular bone": "足舟骨",
    "occipital bone": "枕骨",
    "sacrum": "骶骨",
    "vomer": "犁骨",
    "rectus": "直肌",
    "oblique": "斜肌",
    "levator palpebrae superioris": "上睑提肌",
    "common tendinous ring": "总腱环",
    "trochlea": "滑车",
    "check ligament": "张紧韧带",
    "lumbrical": "蚓状肌",
    "plantar interosseous": "骨间足底肌",
    "tendon": "腱",
    "anterior chamber": "前房",
    "eyeball": "眼球",
    "tarsal plate": "睑板",
    "upper eyelid": "上睑",
    "lower eyelid": "下睑",
    "vitreous body": "玻璃体",
    "decussation": "交叉",
    "white matter": "白质",
    "neuraxis": "脑脊髓轴",
    "brachium": "臂",
    "colliculus": "丘",
    "habenula": "缰核",
    "interventricular foramen": "室间孔",
    "interpeduncular fossa": "脚间窝",
    "stria terminalis": "终纹",
    "tuber cinereum": "灰结节",
    "posterior commissure": "后连合",
    "telencephalon": "端脑",
    "septum": "隔",
    "hepatovenous segment": "肝静脉段",
    "anatomical junction": "解剖连接",
    "pancreatic duct tree": "胰管树",
    "pterygomandibular raphe": "翼下颌缝",
    "pharyngeal raphe": "咽缝",
    "subdivision": "部",
    "auriculotemporal": "耳颞",
    "cystic duct": "胆囊管",
    "deferent duct": "输精管",
    "visceral peritoneum": "脏腹膜",
    "region": "区域",
    "foot": "足",
    "arm": "臂",
    "leg": "小腿",
    "forearm": "前臂",
    "hand": "手",
    "body": "体",
    "part": "部",
    "tributary": "属支",
    "hepatic biliary tree": "肝胆管树",
    "caudate lobe": "尾状叶",
    "intertransversarius": "横突间肌",
    "segment": "段",
    "ix": "IX", "x": "X", "viii": "VIII", "vii": "VII", "vi": "VI", "v": "V", "iv": "IV", "iii": "III", "ii": "II", "i": "I"
}

def translate_simple(text):
    text = text.lower().strip()
    if text in mapping:
        return mapping[text]
    res = text
    sorted_keys = sorted(mapping.keys(), key=len, reverse=True)
    for k in sorted_keys:
        if k in res:
            res = res.replace(k, mapping[k])
    return res

def translate_en(en):
    en = en.lower()
    if "tributary of left hepatic biliary tree" in en and "caudate lobe" in en:
        return "左肝胆管树尾状叶属支"
    if "check ligament of left medial rectus" in en:
        return "左内直肌张紧韧带"
    if "lateral lumbar intertransversarius" in en:
        return "腰外侧横突间肌"

    m = re.search(r"(distal|middle|proximal) phalanx of (left|right) (.*)", en)
    if m:
        pos_en, side_en, finger_en = m.groups()
        side = mapping[side_en]
        pos = mapping[pos_en]
        f_cn = translate_simple(finger_en)
        f_cn = f_cn.replace("finger", "").replace("toe", "")
        bone_type = "指骨" if ("finger" in finger_en or finger_en in ["thumb", "index finger", "little finger", "middle finger", "ring finger"]) else "趾骨"
        return f"{side}{f_cn}{pos}{bone_type}"

    if " of " in en:
        parts = en.split(" of ")
        if len(parts) == 2:
            a = translate_en(parts[0])
            b = translate_en(parts[1])
            if b.startswith(("左", "右")): return b + a
            return b + a

    res = translate_simple(en)
    res = res.replace(" ", "").replace("的", "")
    res = res.replace("big", "拇").replace("index", "食").replace("little", "小").replace("middle", "中").replace("ring", "无名").replace("thumb", "拇")
    res = res.replace("toe", "趾").replace("finger", "指")
    return res

def get_correct_system(item):
    name_en = item['nameEn'].lower()
    if any(word in name_en for word in ["nerve", "neural", "brain", "spinal", "colliculus", "foramen", "fossa", "stria", "thalamus", "commissure", "white matter", "habenula", "tuber cinereum", "decussation", "telencephalon", "septum"]):
        return "nervous", "神经系统"
    if any(word in name_en for word in ["artery", "vein", "venous", "heart", "atrium", "ventricle", "aorta", "capillary", "vascular"]):
        return "cardiovascular", "心血管系统"
    if any(word in name_en for word in ["duct", "gastric", "liver", "hepatic", "pancreas", "pancreatic", "esophagus", "intestine", "colon", "rectum", "bile", "gallbladder", "pharynx", "pharyngeal", "tongue", "tooth", "teeth", "salivary", "peritoneum"]):
        return "digestive", "消化系统"
    if any(word in name_en for word in ["lung", "bronchus", "trachea", "larynx", "nasal", "nose", "bronchial"]):
        return "respiratory", "呼吸系统"
    if any(word in name_en for word in ["kidney", "ureter", "bladder", "urethra", "urinary"]):
        return "urinary", "泌尿系统"
    if any(word in name_en for word in ["testis", "ovary", "uterus", "vagina", "prostate", "penis", "deferent", "seminal", "epididymis", "reproductive"]):
        return "reproductive", "生殖系统"
    if any(word in name_en for word in ["gland", "endocrine", "pituitary", "adrenal", "thyroid", "parathyroid", "pineal"]):
        if "cartilage" not in name_en: return "endocrine", "内分泌系统"
    if any(word in name_en for word in ["lymph", "spleen", "thymus", "tonsil"]):
        return "lymphatic", "淋巴系统"
    if any(word in name_en for word in ["muscle", "muscular", "tendon", "rectus", "oblique", "levator", "sphincter", "lumbrical", "interosseous muscle", "intertransversarius", "raphe"]):
        return "muscular", "肌肉系统"
    if any(word in name_en for word in ["bone", "skeletal", "vertebra", "rib", "phalanx", "cartilage", "ligament", "clavicle", "femur", "tibia", "radius", "ulna", "scapula", "sternum", "hip", "patella", "skull", "maxilla", "mandible", "ossicle"]):
        return "skeletal", "骨骼系统"
    if any(word in name_en for word in ["skin", "hair", "nail", "sweat", "sebaceous", "integument", "eyeball", "eye", "lens", "retina", "cornea", "iris", "vitreous", "tarsal plate", "chamber", "eyelid"]):
        return "integumentary", "感觉系统"
    return "other", "其他"

with open('data/anatomy_data_simple_refined.json', 'r') as f:
    data = json.load(f)
new_data = {k: [] for k in ["skeletal", "muscular", "cardiovascular", "nervous", "digestive", "respiratory", "urinary", "reproductive", "endocrine", "lymphatic", "integumentary", "other"]}
for skey in data:
    for item in data[skey]:
        item['nameCn'] = translate_en(item['nameEn'])
        item['name'] = f"{item['nameCn']} | {item['nameEn']}"
        new_key, new_system_name = get_correct_system(item)
        item['system'] = new_system_name
        new_data[new_key].append({
            "id": item["id"], "name": item["name"], "system": item["system"], "nameEn": item["nameEn"], "nameCn": item["nameCn"]
        })
with open('data/anatomy_data_simple_refined.json', 'w', encoding='utf-8') as f:
    json.dump(new_data, f, ensure_ascii=False, indent=2)
print("Processing complete.")
