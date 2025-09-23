# 设计文档

## 概述

此设计实现了一个基于PySide6的自定义Widget，用于渲染具有特定渐变效果和轮廓样式的等腰梯形。该组件将继承QWidget并重写paintEvent方法来实现自定义绘图。

## 架构

### 核心组件
- **TrapezoidWidget**: 主要的自定义Widget类，继承自QWidget
- **MainWindow**: 应用程序主窗口，用于展示TrapezoidWidget
- **Application**: 应用程序入口点

### 技术栈
- **PySide6**: GUI框架
- **QPainter**: 2D图形绘制
- **QLinearGradient**: 渐变效果实现
- **QPen**: 轮廓线样式控制
- **QPolygonF**: 梯形几何形状定义

## 组件和接口

### TrapezoidWidget类

```python
class TrapezoidWidget(QWidget):
    def __init__(self, parent=None):
        # 初始化尺寸参数
        self.height = 300
        self.top_base = 30
        self.bottom_base = 500
        
    def paintEvent(self, event):
        # 自定义绘图逻辑
        
    def _create_trapezoid_polygon(self):
        # 创建梯形多边形坐标
        
    def _create_gradient(self):
        # 创建渐变填充
        
    def _setup_outline_pen(self):
        # 设置轮廓线样式
```

### 几何计算

梯形坐标计算：
- 上底中心对齐，左右各延伸15像素（30/2）
- 下底中心对齐，左右各延伸250像素（500/2）
- 高度为300像素
- 腰边连接上下底的对应端点

### 渐变配置

垂直线性渐变设置：
- 起点：(0, 0) - 颜色#B6B384，透明度0（完全透明）
- 中点：(0, 150) - 颜色#FEFFAF，透明度127（50%透明）
- 终点：(0, 300) - 颜色#B7B286，透明度0（完全透明）

## 数据模型

### 颜色定义
```python
COLORS = {
    'top': '#B6B384',      # 顶部颜色
    'middle': '#FEFFAF',   # 中间颜色
    'bottom': '#B7B286',   # 底部颜色
    'outline': '#B7B286'   # 轮廓颜色
}
```

### 尺寸参数
```python
DIMENSIONS = {
    'height': 300,
    'top_base': 30,
    'bottom_base': 500,
    'outline_width': 2
}
```

## 错误处理

### 绘图错误处理
- 检查Widget尺寸是否足够容纳梯形
- 验证颜色值格式的有效性
- 处理QPainter初始化失败的情况

### 参数验证
- 确保所有尺寸参数为正数
- 验证颜色代码格式正确性
- 检查透明度值在有效范围内（0-255）

## 测试策略

### 单元测试
- 测试梯形坐标计算的准确性
- 验证渐变颜色设置
- 测试轮廓线样式配置

### 集成测试
- 测试完整的绘图流程
- 验证Widget在不同窗口尺寸下的表现
- 测试颜色渲染的准确性

### 视觉测试
- 验证梯形形状的正确性
- 检查渐变效果的平滑过渡
- 确认只有侧边有轮廓线
- 验证颜色和透明度的准确性

### 性能测试
- 测试绘图性能，确保流畅的重绘
- 验证内存使用情况
- 测试窗口调整大小时的响应性