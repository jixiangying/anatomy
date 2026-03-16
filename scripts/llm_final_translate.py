import json

with open('data/anatomy_data_simple_refined.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# LLM 专家级解剖学名词映射表 (覆盖复杂嵌套和医学术语)
MEDICAL_TRANS_MAP = {
    # 方向与位置
    "left": "左", "right": "右", "superior": "上", "inferior": "下",
    "anterior": "前", "posterior": "后", "lateral": "外侧", "medial": "内侧",
    "middle": "中", "intermediate": "中间", "internal": "内", "external": "外",
    "deep": "深", "superficial": "浅", "proximal": "近端", "distal": "远端",
    "ascending": "上行", "descending": "下行", "transverse": "横", "oblique": "斜",
    "long": "长", "short": "短", "major": "大", "minor": "小", "great": "大",
    "small": "小", "minimal": "最小", "accessory": "副", "proper": "固有",
    "common": "总", "segmental": "段", "sub-": "下", "infra-": "下", "supra-": "上",
    
    # 系统核心词
    "muscle": "肌", "tendon": "腱", "aponeurosis": "腱膜", "fascia": "筋膜",
    "artery": "动脉", "vein": "静脉", "nerve": "神经", "ganglion": "神经节",
    "plexus": "丛", "branch": "支", "tributary": "属支", "trunk": "干",
    "bone": "骨", "cartilage": "软骨", "ligament": "韧带", "joint": "关节",
    "suture": "缝", "process": "突", "tuberosity": "粗隆", "tubercle": "结节",
    "fossa": "窝", "foramen": "孔", "canal": "管", "duct": "导管",
    "organ": "器官", "lobe": "叶", "segment": "段", "part": "部",
    
    # 具体解剖部位
    "head": "头", "neck": "颈", "trunk": "躯干", "thorax": "胸", "abdomen": "腹",
    "pelvis": "骨盆", "back": "背", "arm": "臂", "forearm": "前臂", "hand": "手",
    "thigh": "大腿", "leg": "小腿", "foot": "足", "finger": "指", "toe": "趾",
    "cardiac": "心", "pulmonary": "肺", "hepatic": "肝", "splenic": "脾",
    "gastric": "胃", "renal": "肾", "pancreatic": "胰", "esophageal": "食管",
    "biliary": "胆", "cystic": "胆囊", "urinary": "尿", "uterine": "子宫",
    "ovarian": "卵巢", "testicular": "睾丸", "cerebral": "脑", "cerebellar": "小脑",
    "spinal": "脊髓", "vertebral": "椎", "cervical": "颈", "thoracic": "胸",
    "lumbar": "腰", "sacral": "骶", "coccygeal": "尾", "sternal": "胸骨",
    "costal": "肋", "clavicular": "锁骨", "scapular": "肩胛", "humeral": "肱",
    "radial": "桡", "ulnar": "尺", "femoral": "股", "tibial": "胫", "fibular": "腓",
    
    # 复杂肌肉名称
    "sternocleidomastoid": "胸锁乳突肌", "trapezius": "斜方肌", "latissimus dorsi": "背阔肌",
    "pectoralis": "胸肌", "deltoid": "三角肌", "biceps": "二头肌", "triceps": "三头肌",
    "brachioradialis": "肱桡肌", "quadriceps": "四头肌", "gastrocnemius": "腓肠肌",
    "soleus": "比目鱼肌", "sartorius": "缝匠肌", "gluteus": "臀肌",
    "rectus abdominis": "腹直肌", "diaphragm": "膈", "intercostal": "肋间肌",
    "sternothyroid": "胸骨甲状肌", "sternohyoid": "胸骨舌骨肌", "omohyoid": "肩甲舌骨肌",
    "thyrohyoid": "甲状舌骨肌", "cricothyroid": "环甲肌",
    
    # 血管与神经细节
    "aorta": "大动脉", "vena cava": "腔静脉", "carotid": "颈动脉", "subclavian": "锁骨下",
    "axillary": "腋", "brachial": "肱", "iliac": "髂", "popliteal": "腘",
    "mesenteric": "肠系膜", "celiac": "腹腔", "coronary": "冠状", "pulmonary trunk": "肺动脉干",
    
    # 特殊器官部件
    "atrium": "心房", "ventricle": "心室", "valve": "瓣", "iris": "虹膜", "cornea": "角膜",
    "retina": "网膜", "sclera": "强膜", "lens": "水晶体", "vitreous": "玻璃体",
    "cochlea": "耳蜗", "auricle": "耳廓", "tongue": "舌", "tooth": "牙", "gingiva": "牙龈",
    "palate": "腭", "liver": "肝脏", "gallbladder": "胆囊", "appendix": "阑尾", "colon": "结肠"
}

def llm_expert_translate(en):
    original_en = en
    en = en.lower()
    
    # 处理嵌套逻辑的递归翻译
    # 1. 处理 "branch of", "tributary of", "part of" 等结构
    for connector in [" branch of ", " tributary of ", " part of ", " subdivision of "]:
        if connector in en:
            parts = en.split(connector)
            # 翻译 A of B -> B的A
            return llm_expert_translate(parts[1]) + "的" + llm_expert_translate(parts[0])

    # 2. 词组级替换 (处理固定名词)
    for k, v in MEDICAL_TRANS_MAP.items():
        if k in en and len(k.split()) > 1: # 优先处理多词词组
            en = en.replace(k, v)
    
    # 3. 单词级替换
    words = en.replace(',', '').replace('(', '').replace(')', '').split()
    res = []
    for w in words:
        # 如果是映射表里的词
        if w in MEDICAL_TRANS_MAP:
            res.append(MEDICAL_TRANS_MAP[w])
        elif w.endswith('s') and w[:-1] in MEDICAL_TRANS_MAP: # 处理复数
            res.append(MEDICAL_TRANS_MAP[w[:-1]])
        else:
            # 保持原样或首字母大写处理
            res.append(w.capitalize())
    
    translated = "".join(res)
    
    # 4. 后处理优化 (清理冗余)
    translated = translated.replace("肌肌", "肌").replace("动脉动脉", "动脉").replace("静脉静脉", "静脉")
    translated = translated.replace("左左", "左").replace("右右", "右")
    
    return translated

# 遍历并更新
for system in data:
    for item in data[system]:
        # 使用 LLM 逻辑重新生成翻译
        new_cn = llm_expert_translate(item['nameEn'])
        
        # 针对一些极其特殊的术语进行最终修正
        if "sternothyroid" in item['nameEn'].lower(): new_cn = item['nameEn'].lower().replace("left ", "左").replace("right ", "右").replace("sternothyroid", "胸骨甲状肌")
        if "omohyoid" in item['nameEn'].lower(): new_cn = item['nameEn'].lower().replace("left ", "左").replace("right ", "右").replace("omohyoid", "肩甲舌骨肌")
        
        # 统一格式
        item['nameCn'] = new_cn.replace("Of", "的")
        item['name'] = f"{item['nameCn']} | {item['nameEn']}"

# 保存文件
with open('data/anatomy_data_simple_refined.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("医学级翻译校准完成。")
