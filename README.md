# 人体解剖学交互图谱 | Human Anatomy Explorer

基于 **BodyParts3D** 真实MRI扫描数据的3D人体骨骼可视化应用。

---

## 🎉 项目特点

- ✅ **真实人体模型** - 基于2mm MRI扫描的医学级数据
- ✅ **202个骨骼** - 近乎完整的人体骨骼系统
- ✅ **双语标注** - 中文 + 英文解剖学术语
- ✅ **双向交互** - 点击3D模型或列表相互联动
- ✅ **双语搜索** - 支持中英文搜索骨骼
- ✅ **开源免费** - CC BY-SA 许可

---

## 📁 项目结构

```
Anatomy/
├── index.html                      # 主页面 - 3D解剖查看器
├── README.md                       # 项目说明
├── MODELS.md                       # 模型数据来源
├── PROJECT_STRUCTURE.md            # 详细结构说明
│
├── data/                           # BodyParts3D官方数据
│   ├── partof_parts_list.txt       # 部位列表
│   ├── partof_parts_list_e.txt     # 英文部位列表
│   └── partof_element_parts.txt    # 元素-文件对应关系
│
├── js/                             # JavaScript库
│   └── OrbitControls.js            # Three.js轨道控制器
│
├── scripts/                        # 数据处理脚本
│   └── extract_bones.py            # 骨骼提取脚本
│
└── partof_BP3D_4.0_obj_99/         # 3D模型文件夹
    └── FJ*.obj                     # 1,258个OBJ文件
```

---

## 🚀 快速开始

### 在线访问（推荐）

🌐 **GitHub Pages**: https://jixiangying.github.io/anatomy/

无需安装，直接在浏览器中访问即可查看3D人体骨骼模型。

### 本地运行

如需本地修改或开发：

```bash
git clone https://github.com/jixiangying/anatomy.git
cd anatomy
python3 -m http.server 3000
# 浏览器访问 http://localhost:3000
```

---

## 📊 包含的骨骼系统（202块）

| 分类 | 数量 | 主要骨骼 |
|------|------|----------|
| **颅骨** | 24 | 额骨、顶骨、颞骨、枕骨、蝶骨、筛骨、下颌骨、上颌骨、颧骨、鼻骨、泪骨、腭骨、犁骨、下鼻甲、舌骨 |
| **脊柱** | 25 | 颈椎C1-C7（含寰椎、枢椎）、胸椎T1-T12、腰椎L1-L5、骶骨 |
| **胸廓** | 27 | 胸骨、左右各12根肋骨 |
| **上肢** | 64 | 锁骨、肩胛骨、肱骨、尺骨、桡骨、8块腕骨×2、5块掌骨×2、14块指骨×2 |
| **下肢** | 62 | 髋骨、股骨、髌骨、胫骨、腓骨、7块跗骨×2、5块跖骨×2、14块趾骨×2 |

**总计：202块骨骼**（接近完整的成人骨骼系统，缺少听骨6块和尾骨1块）

---

## 🎮 使用说明

| 操作 | 功能 |
|------|------|
| 左键拖动 | 旋转视角 |
| 右键拖动 | 平移视角 |
| 滚轮 | 缩放 |
| 点击左侧列表 | 高亮3D模型并显示详情 |
| 点击3D模型 | 自动滚动并高亮左侧列表项 |
| 搜索框 | 中英文搜索骨骼 |

---

## 🏥 数据来源

- **项目**: BodyParts3D / Anatomography
- **机构**: 日本东京大学生命科学数据库中心
- **技术**: 2mm间隔全身MRI扫描
- **许可**: CC BY-SA 2.1 Japan
- **模型数**: 1,258个OBJ文件（约210MB）

### 官方下载

- 官网: https://dbarchive.biosciencedbc.jp/data/bodyparts3d/
- 模型文件: `partof_BP3D_4.0_obj_99.zip` (62MB压缩包)
- 数据说明: `partof_*.txt` 文件

### 引用格式

```
BodyParts3D, © The Database Center for Life Science 
licensed under CC Attribution-Share Alike 2.1 Japan
http://dbarchive.biosciencedbc.jp/en/bodyparts3d/
```

---

## ⚠️ 已知限制

1. **缺少听骨**（6块）- 锤骨、砧骨、镫骨左右各3块
   - 原因：2mm分辨率MRI无法清晰重建3mm大小的听骨

2. **缺少尾骨**（1块）- 通常由3-5块尾椎融合而成
   - 原因：在BodyParts3D中可能归类为骶骨的一部分

3. **重复骨骼**（3块记录）
   - 舌骨：2个文件（FJ2772, FJ3201）
   - 胸骨：3个文件（FJ3153, FJ3178, FJ3290）
   - 实际独特骨骼：199块

---

## 🛠️ 技术栈

- **Three.js r128** - 3D渲染引擎
- **Tailwind CSS** - UI样式（CDN）
- **原生JavaScript** - 应用逻辑
- **Python 3** - 数据处理

---

## 📄 许可

BodyParts3D数据遵循 **CC BY-SA 2.1 Japan** 许可：
- ✅ 允许自由使用、修改、分发
- ✅ 允许商业使用
- ⚠️ 需要注明出处

---

Created with ❤️ for anatomy education
