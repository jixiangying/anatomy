import json

with open('data/anatomy_data_simple.json', 'r') as f:
    data = json.load(f)

def llm_refine_item(item):
    en = item['nameEn'].lower()
    
    # 1. Specific anatomical re-classification & Translation
    if 'hepatic biliary tree' in en:
        item['system'] = '消化系统'
        item['nameCn'] = item['nameEn'].replace('Caudate lobe', '尾状叶').replace('tributary of', '属支').replace('left hepatic biliary tree', '左肝胆管树').replace('right hepatic biliary tree', '右肝胆管树').replace('Anterior superior', '前上').replace('Anterior inferior', '前下').replace('Lateral superior', '外侧上').replace('Lateral inferior', '外侧下').replace('Medial superior', '内侧上').replace('Medial inferior', '内侧下').replace('Posterior superior', '后上').replace('Posterior inferior', '后下')
    
    elif 'lacrimal' in en:
        item['system'] = '神经系统' # Sensory/Eye appendage
        trans = {'lacrimal canaliculus': '泪小管', 'lacrimal gland': '泪腺', 'lacrimal lake': '泪湖', 'lacrimal sac': '泪囊'}
        for k, v in trans.items():
            if k in en: item['nameCn'] = v; break

    elif 'bronchial tree' in en or 'nasal cartilage' in en:
        item['system'] = '呼吸系统'
        if 'bronchial tree' in en:
            item['nameCn'] = item['nameEn'].replace('left', '左').replace('right', '右').replace('apical', '尖').replace('posterior', '后').replace('anterior', '前').replace('superior', '上').replace('inferior', '下').replace('lateral', '外侧').replace('medial', '内侧').replace('basal', '底').replace('segmental bronchial tree', '段支气管树').replace('pulmonary segment of bronchial tree', '支气管树肺段')
        if 'nasal cartilage' in en:
            item['nameCn'] = item['nameEn'].replace('left', '左').replace('right', '右').replace('major alar cartilage', '鼻翼大软骨').replace('lateral nasal cartilage', '鼻侧软骨')

    elif 'artery' in en or 'vein' in en or 'vascular' in en or 'aorta' in en or 'portal vein' in en:
        item['system'] = '心血管系统'
        # Refine common artery/vein phrases
        cn = item['nameEn'].replace('branch of', '分支').replace('trunk of', '干').replace('Left', '左').replace('Right', '右').replace('left', '左').replace('right', '右')
        cn = cn.replace('anterior', '前').replace('posterior', '后').replace('superior', '上').replace('inferior', '下')
        cn = cn.replace('middle', '中').replace('lateral', '外侧').replace('medial', '内侧').replace('temporal', '颞').replace('occipital', '枕').replace('cerebral', '脑')
        cn = cn.replace('artery', '动脉').replace('vein', '静脉').replace('segment of', '段')
        if item['nameCn'] == item['nameEn']: item['nameCn'] = cn

    elif 'muscle' in en or 'rectus' in en or 'longus colli' in en or 'interspinalis' in en:
        item['system'] = '肌肉系统'
        if item['nameCn'] == item['nameEn']:
            cn = item['nameEn'].replace('left', '左').replace('right', '右').replace('muscle', '肌').replace('rectus', '直肌').replace('longus colli', '颈长肌')
            item['nameCn'] = cn

    elif 'small intestine' in en or 'jejunum' in en or 'pancreas' in en:
        item['system'] = '消化系统'
        if 'small intestine' in en: item['nameCn'] = item['nameEn'].replace('zone of small intestine', '小肠区')
        if 'jejunum' in en: item['nameCn'] = item['nameEn'].replace('proximal part of jejunum', '空肠近端')

    elif 'hepatovenous' in en:
        item['system'] = '心血管系统'
        item['nameCn'] = item['nameEn'].replace('segment ix', '第IX段').replace('hepatovenous', '肝静脉')

    # Update the full name field
    item['name'] = f"{item['nameCn']} | {item['nameEn']}"
    return item

refined_data = {k: [] for k in data.keys()}
all_items = []
for k in data:
    all_items.extend(data[k])

for item in all_items:
    refined_item = llm_refine_item(item)
    refined_data[refined_item['system_code'] if 'system_code' in refined_item else 'other'].append(refined_item)

# Re-sort into the 12 categories based on refined system
final_output = {
    "skeletal": [], "muscular": [], "cardiovascular": [], "nervous": [],
    "digestive": [], "respiratory": [], "urinary": [], "reproductive": [],
    "endocrine": [], "lymphatic": [], "integumentary": [], "other": []
}

system_map = {
    "骨骼系统": "skeletal", "肌肉系统": "muscular", "心血管系统": "cardiovascular",
    "神经系统": "nervous", "消化系统": "digestive", "呼吸系统": "respiratory",
    "泌尿系统": "urinary", "生殖系统": "reproductive", "内分泌系统": "endocrine",
    "淋巴系统": "lymphatic", "皮肤系统": "integumentary", "其他": "other"
}

for item in all_items:
    sys_key = system_map.get(item['system'], "other")
    final_output[sys_key].append(item)

with open('data/anatomy_data_simple_refined.json', 'w', encoding='utf-8') as f:
    json.dump(final_output, f, ensure_ascii=False, indent=2)

print("Refined JSON generated: data/anatomy_data_simple_refined.json")
