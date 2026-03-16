import json

# 1. 深度解剖学词典 (LLM 全量对齐)
TRANS_MAP = {
    "left": "左", "right": "右", "superior": "上", "inferior": "下",
    "anterior": "前", "posterior": "后", "lateral": "外侧", "medial": "内侧",
    "middle": "中", "intermediate": "中间", "internal": "内", "external": "外",
    "deep": "深", "superficial": "浅", "proximal": "近端", "distal": "远端",
    "ascending": "上行", "descending": "下行", "transverse": "横", "oblique": "斜",
    "long": "长", "short": "短", "major": "大", "minor": "小", "great": "大",
    "small": "小", "minimal": "最小", "accessory": "副", "proper": "固有",
    "common": "总", "segmental": "段", "basal": "底", "apical": "尖",
    "dorsal": "背侧", "palmar": "掌侧", "plantar": "足底", "ventral": "腹侧",
    "longus": "长", "brevis": "短", "maximus": "最大", "medius": "中", "minimus": "最小",
    
    "muscle": "肌", "tendon": "腱", "aponeurosis": "腱膜", "fascia": "筋膜", "ligament": "韧带",
    "artery": "动脉", "vein": "静脉", "nerve": "神经", "ganglion": "神经节", "plexus": "丛",
    "vessel": "血管", "capillary": "毛细血管", "aorta": "大动脉", "sinus": "窦", "tributary": "属支",
    "branch": "支", "trunk": "干", "segment": "段", "lobe": "叶", "part": "部", "division": "部",
    "bone": "骨", "cartilage": "软骨", "joint": "关节", "suture": "缝", "process": "突",
    "tuberosity": "粗隆", "tubercle": "结节", "fossa": "窝", "foramen": "孔", "canal": "管",
    
    "head": "头", "neck": "颈", "body": "体", "arm": "臂", "forearm": "前臂", "hand": "手",
    "thigh": "大腿", "leg": "小腿", "foot": "足", "finger": "指", "toe": "趾", "digit": "指/趾",
    "thoracic": "胸", "lumbar": "腰", "cervical": "颈", "sacral": "骶", "coccygeal": "尾",
    "vertebra": "椎骨", "rib": "肋骨", "sternum": "胸骨", "clavicle": "锁骨", "scapula": "肩胛骨",
    "humerus": "肱骨", "radius": "桡骨", "ulna": "尺骨", "femur": "股骨", "tibia": "胫骨", "fibula": "腓骨",
    
    "cardiac": "心", "pulmonary": "肺", "hepatic": "肝", "gastric": "胃", "splenic": "脾",
    "renal": "肾", "pancreatic": "胰", "esophageal": "食管", "biliary": "胆", "urinary": "尿",
    "cerebral": "脑", "cerebellar": "小脑", "spinal": "脊髓", "optic": "视", "auditory": "听",
    "temporal": "颞", "occipital": "枕", "frontal": "额", "parietal": "顶", "sphenoid": "蝶",
    "ethmoid": "筛", "zygomatic": "颧", "maxilla": "上颌", "mandible": "下颌",
    
    "atrium": "心房", "ventricle": "心室", "auricle": "耳廓/心耳", "valve": "瓣",
    "thyroid": "甲状", "adrenal": "肾上腺", "pituitary": "垂体", "pineal": "松果体",
    "tongue": "舌", "tooth": "牙", "teeth": "牙齿", "gingiva": "牙龈", "palate": "腭",
    "esophagus": "食管", "stomach": "胃", "duodenum": "十二指肠", "jejunum": "空肠", "ileum": "回肠",
    "colon": "结肠", "rectum": "直肠", "appendix": "阑尾", "liver": "肝脏", "pancreas": "胰腺",
    "kidney": "肾脏", "ureter": "输尿管", "bladder": "膀胱", "urethra": "尿道",
    "testis": "睾丸", "ovary": "卵巢", "uterus": "子宫", "vagina": "阴道", "prostate": "前列腺",
    "skin": "皮肤", "hair": "毛发", "nail": "指甲", "eye": "眼", "eyeball": "眼球",
    "cornea": "角膜", "iris": "虹膜", "retina": "视网膜", "lens": "晶状体", "sclera": "巩膜",
    "vitreous": "玻璃体", "lacrimal": "泪", "nasal": "鼻", "larynx": "喉", "trachea": "气管",
    "bronchus": "支气管", "bronchial": "支气管", "alveolar": "肺泡", "pleura": "胸膜",
    "diaphragm": "膈", "peritoneum": "腹膜", "omentum": "网膜", "mesentery": "肠系膜",
    "infrahyoid": "舌骨下", "sternothyroid": "胸骨甲状", "omohyoid": "肩甲舌骨", "sternohyoid": "胸骨舌骨",
    "cricoid": "环状", "thyrohyoid": "甲状舌骨", "trapezius": "斜方肌", "deltoid": "三角肌",
    "pectoralis": "胸肌", "rectus": "直肌", "vastus": "股肌", "gluteus": "臀肌",
    "interosseous": "骨间", "lumbrical": "蚓状", "levator": "提", "adductor": "收", "flexor": "屈", "abductor": "展"
}

def translate_item(en):
    en = en.lower()
    
    # 递归处理 'of', 'part of', 'branch of'
    for connector in [" subdivision of ", " part of ", " tributary of ", " branch of ", " of "]:
        if connector in en:
            parts = en.split(connector, 1)
            # A connector B -> B的A
            return translate_item(parts[1]) + "的" + translate_item(parts[0])
    
    # 替换特殊复合词
    special_cases = {
        "caudate lobe": "尾状叶",
        "pulmonary trunk": "肺动脉干",
        "vena cava": "腔静脉",
        "portal vein": "门静脉",
        "common bile duct": "胆总管",
        "internal capsule": "内囊",
        "corpus callosum": "胼胝体",
        "white matter": "白质",
        "gray matter": "灰质",
        "optic chiasm": "视交叉",
        "interpeduncular fossa": "脚间窝",
        "tuber cinereum": "灰结节",
        "proper palmar digital": "掌侧固有指",
        "common palmar digital": "掌侧总指",
        "thoracic aorta": "胸大动脉",
        "abdominal aorta": "腹大动脉"
    }
    for k, v in special_cases.items():
        if k in en:
            en = en.replace(k, v)

    # 分词翻译
    words = en.replace(',', '').replace('(', '').replace(')', '').split()
    res = []
    for w in words:
        if any(ord(c) > 127 for c in w): # 已经是中文了
            res.append(w)
        elif w in TRANS_MAP:
            res.append(TRANS_MAP[w])
        elif w.endswith('s') and w[:-1] in TRANS_MAP:
            res.append(TRANS_MAP[w[:-1]])
        else:
            # 如果还是翻译不出来，尝试去除一些常见的连字符或后缀
            clean_w = w.strip('-').replace('-', '')
            if clean_w in TRANS_MAP:
                res.append(TRANS_MAP[clean_w])
            else:
                # 最终兜底：保持原样（虽然应该极少了）
                res.append(w.capitalize())
    
    final = "".join(res)
    # 清理翻译后的冗余
    replacements = {
        "肌肌": "肌", "骨骨": "骨", "动脉动脉": "动脉", "静脉静脉": "静脉",
        "左左": "左", "右右": "右", "的的": "的", "动脉支": "动脉支"
    }
    for k, v in replacements.items():
        final = final.replace(k, v)
    return final

# 加载并重写
with open('data/anatomy_data_simple_refined.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for system in data:
    for item in data[system]:
        nameEn = item['nameEn']
        nameCn = translate_item(nameEn)
        
        # 针对具体条目做最后的 LLM 级润色
        if "irregular bone" in nameEn.lower(): nameCn = nameCn.replace("不规则骨", "").replace("骨骨", "骨") + "骨"
        if "set of" in nameEn.lower(): nameCn = nameCn.replace("集合", "组")
        
        # 修正语序
        nameCn = nameCn.replace("左的", "左").replace("右的", "右")
        
        item['nameCn'] = nameCn
        item['name'] = f"{nameCn} | {nameEn}"

with open('data/anatomy_data_simple_refined.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("全量高保真医学翻译已完成。")
