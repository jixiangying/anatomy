import json
import csv

# 1. 加载用户当前已修复的 JSON，保留中文翻译
with open('data/anatomy_data_simple_refined.json', 'r', encoding='utf-8') as f:
    current_data = json.load(f)

id_to_old_cn = {}
for sys in current_data:
    for item in current_data[sys]:
        # 如果当前的中文不是那些通用的错误英文，就保留它
        cn = item.get('nameCn', '')
        en_old = item.get('nameEn', '').lower()
        # 只有当中文不是由之前的错误英文占位时，才视为“用户修复过的”
        if cn and cn != item.get('nameEn') and "organ with" not in cn.lower():
            id_to_old_cn[item['id']] = cn

# 2. 从原始文本中挖掘最具体的英文名
# 通用/模糊词黑名单
GENERIC_FILTER = {
    "organ with cavitated organ parts", "organ part", "organ component", 
    "cardinal organ part", "organ", "anatomical entity", "physical anatomical entity",
    "material anatomical entity", "anatomical structure", "organ segment",
    "material physical anatomical entity", "set of organs", "viscus", "bone organ"
}

fj_name_candidates = {}
with open('data/isa_element_parts.txt', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f, delimiter='\t')
    for row in reader:
        fj = row['element file id']
        name = row['name']
        if fj not in fj_name_candidates:
            fj_name_candidates[fj] = []
        fj_name_candidates[fj].append(name)

def pick_best_en(names):
    # 评分机制：非通用词最高，带左右的次之，越长越具体
    best = names[0]
    max_score = -1
    for n in names:
        n_lower = n.lower()
        score = 0
        if n_lower not in GENERIC_FILTER:
            score += 1000
        score += len(n)
        if "left" in n_lower or "right" in n_lower:
            score += 500
        if score > max_score:
            max_score = score
            best = n
    return best

# 3. 重新构建 JSON
new_data = {sys: [] for sys in current_data.keys()}

# 为了保持系统分类逻辑，我们需要重新跑一下简单的系统识别
def get_sys(en):
    en = en.lower()
    if any(x in en for x in ["artery", "vein", "vessel", "aorta", "heart", "atrium", "ventricle"]): return "cardiovascular"
    if any(x in en for x in ["nerve", "brain", "ganglion", "plexus", "thalamus", "retina", "cornea"]): return "nervous"
    if any(x in en for x in ["muscle", "tendon", "fascia", "rectus", "oblique"]): return "muscular"
    if any(x in en for x in ["lung", "trachea", "bronch", "larynx", "nasal"]): return "respiratory"
    if any(x in en for x in ["esophagus", "stomach", "liver", "pancreas", "colon", "tooth", "teeth", "tongue"]): return "digestive"
    if any(x in en for x in ["bone", "vertebra", "skull", "rib", "sternum", "spine", "clavicle", "scapula"]): return "skeletal"
    if any(x in en for x in ["kidney", "bladder", "ureter"]): return "urinary"
    if any(x in en for x in ["testis", "ovary", "prostate", "uterus"]): return "reproductive"
    if any(x in en for x in ["thyroid", "adrenal", "pituitary"]): return "endocrine"
    if "spleen" in en or "lymph" in en: return "lymphatic"
    if "skin" in en or "hair" in en: return "integumentary"
    return "other"

system_names = {"skeletal":"骨骼系统","muscular":"肌肉系统","cardiovascular":"心血管系统","nervous":"神经系统","digestive":"消化系统","respiratory":"呼吸系统","urinary":"泌尿系统","reproductive":"生殖系统","endocrine":"内分泌系统","lymphatic":"淋巴系统","integumentary":"皮肤系统","other":"其他"}

# 遍历所有发现的模型
all_fjs = sorted(fj_name_candidates.keys())
for fj_id in all_fjs:
    best_en = pick_best_en(fj_name_candidates[fj_id])
    sys_code = get_sys(best_en)
    
    # 优先使用用户修复的中文，如果没有，则使用英文名作为中文
    name_cn = id_to_old_cn.get(fj_id, best_en)
    
    new_data[sys_code].append({
        "id": fj_id,
        "name": f"{name_cn} | {best_en}",
        "system": system_names[sys_code],
        "nameEn": best_en,
        "nameCn": name_cn
    })

with open('data/anatomy_data_simple_refined.json', 'w', encoding='utf-8') as f:
    json.dump(new_data, f, ensure_ascii=False, indent=2)

print("英文名称已通过原始数据完成具体化修复，且保留了您的中文翻译。")
