# 移动端适配说明

## 已完成的移动端优化

### 1. Favicon
- 添加了SVG格式的favicon (`favicon.svg`)
- 支持Apple touch icon
- 主题色设置为深色 (#0a0a0f)

### 2. 响应式布局
- **平板/小屏幕 (≤768px)**: 侧边栏变为可滑出的抽屉式菜单
- **手机 (≤480px)**: 侧边栏全屏显示
- 底部统计栏缩小适配

### 3. 触摸优化
- 隐藏了桌面端的tooltip（移动端不适用）
- 增大了点击区域 (bone-item padding增加到12px)
- 添加了移动端控制按钮（☰ 打开列表，ℹ 打开信息面板）

### 4. 移动端控制
- 左下角按钮：打开/关闭骨骼列表
- 右下角按钮：打开/关闭信息面板
- 点击遮罩层或选择骨骼后自动关闭侧边栏

### 5. Meta标签
```html
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<meta name="theme-color" content="#0a0a0f">
<meta name="apple-mobile-web-app-capable" content="yes">
```

## 3D交互（Three.js内置）

Three.js的OrbitControls已内置支持：
- **单指拖动**: 旋转视角
- **双指捏合**: 缩放
- **双指拖动**: 平移

## 测试建议

### iOS Safari
- 检查状态栏颜色
- 测试添加到主屏幕后的表现

### Android Chrome
- 检查主题色
- 测试触摸响应

### 性能考虑
- 202个3D模型在移动端可能较重
- 建议在WiFi环境下使用
- 低端设备可能需要简化模式（未来可考虑）

## 待优化项（可选）

1. **性能优化**: 根据设备性能动态调整渲染质量
2. **加载优化**: 移动端优先加载重要骨骼
3. **手势增强**: 添加双击重置视角等功能
