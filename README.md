# 人体解剖学3D交互图谱 | Human Anatomy Explorer

基于 **BodyParts3D** 真实MRI扫描数据的3D人体解剖可视化应用，支持11大系统交互式浏览。

---

## ✨ 功能特点

- ✅ **真实人体模型** - 基于2mm MRI扫描的医学级数据
- ✅ **11大解剖系统** - 骨骼、肌肉、心血管、神经、消化、呼吸、泌尿、生殖、内分泌、淋巴、皮肤
- ✅ **双语标注** - 中文 + 英文解剖学术语
- ✅ **全局搜索** - 一键搜索所有系统，自动打开对应图层
- ✅ **智能高亮** - 选中模型高亮显示，其他模型自动半透明
- ✅ **图层控制** - 独立开关各系统，自由组合显示
- ✅ **双向交互** - 点击列表项或3D模型相互联动
- ✅ **平滑动画** - 相机自动聚焦到选中部位

---

## 🚀 快速开始

### 在线访问
🌐 **GitHub Pages**: https://jixiangying.github.io/anatomy/

### 本地运行
```bash
git clone https://github.com/jixiangying/anatomy.git
cd anatomy
python3 -m http.server 3000
# 浏览器访问 http://localhost:3000
```

---

## 🎮 使用说明

| 操作 | 功能 |
|------|------|
| 左键拖动 | 旋转视角 |
| 右键拖动 | 平移视角 |
| 滚轮 | 缩放 |
| 搜索框 | 全局搜索所有系统的部位 |
| 点击左侧列表 | 高亮3D模型并聚焦 |
| 点击3D模型 | 自动高亮并滚动左侧列表 |
| 点击空白处 | 取消选择，恢复全不透明 |
| 右侧图层控制 | 开关各系统显示 |

---

## 📁 项目结构

```
Anatomy/
├── index.html                      # 主页面 - 3D解剖查看器
├── README.md                       # 项目说明
├── anatomy_names.csv               # 2234条解剖学术语对照表
├── favicon.svg                     # 网站图标
│
├── js/                             # JavaScript库
│   ├── OBJLoader.js               # Three.js OBJ加载器
│   └── OrbitControls.js           # 轨道控制器
│
├── data/                           # 解剖学数据
│   ├── anatomy_data_simple_refined.json  # 前端使用的结构化数据
│   ├── model_classification_table.json   # 模型分类表
│   └── isa_*.txt                   # BodyParts3D官方元数据
│
├── scripts/                        # 数据处理脚本
│   ├── refine_anatomy.py          # 术语翻译与精炼
│   └── rebuild_json_final_*.py    # 数据转换脚本
│
└── isa_BP3D_4.0_obj_99/           # 3D模型文件夹
    └── FJ*.obj                    # 2,234个OBJ文件（约210MB）
```

---

## 🏥 数据来源

- **项目**: BodyParts3D / Anatomography
- **机构**: 日本东京大学生命科学数据库中心
- **技术**: 2mm间隔全身MRI扫描
- **许可**: CC BY-SA 2.1 Japan
- **模型数**: 1,258个OBJ文件（约210MB）

### 官方下载
- 官网: https://dbarchive.biosciencedbc.jp/data/bodyparts3d/
- 模型文件: `isa_BP3D_4.0_obj_99.zip`

### 引用格式
```
BodyParts3D, © The Database Center for Life Science 
licensed under CC Attribution-Share Alike 2.1 Japan
http://dbarchive.biosciencedbc.jp/en/bodyparts3d/
```

---

## 🛠️ 技术栈

- **Three.js r128** - 3D渲染引擎
- **Tailwind CSS** - UI样式
- **原生JavaScript** - 应用逻辑
- **Python 3** - 数据处理

---

## 📄 许可

本项目代码遵循 MIT 许可。

BodyParts3D数据遵循 **CC BY-SA 2.1 Japan** 许可：
- ✅ 允许自由使用、修改、分发
- ✅ 允许商业使用
- ⚠️ 需要注明出处

---

Created with ❤️ for anatomy education
