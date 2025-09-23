#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
偏移量缩放分析程序
分析偏移量与线段长度的关系，对比不同的计算方式
"""

import sys
import math
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                               QHBoxLayout, QLabel, QSlider, QComboBox)
from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QPainter, QLinearGradient, QPen, QColor, QPainterPath


class OffsetScalingWidget(QWidget):
    """偏移量缩放分析Widget"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # 控制参数
        self.scaling_method = "current"  # current, line_length, fixed, hybrid
        self.intensity = 0.3
        self.ratio = 0.3
        
        self.setFixedSize(1000, 700)
        self.setStyleSheet("background-color: #FFFFFF; border: 2px solid #333333;")
    
    def set_parameters(self, scaling_method, intensity, ratio):
        """设置参数并重绘"""
        self.scaling_method = scaling_method
        self.intensity = intensity
        self.ratio = ratio
        self.update()
    
    def calculate_offset(self, method, line_length, height):
        """根据不同方法计算偏移量"""
        if method == "current":
            # 当前方法：基于梯形高度
            return self.intensity * height * self.ratio
        elif method == "line_length":
            # 基于线段长度
            return self.intensity * line_length * self.ratio
        elif method == "fixed":
            # 固定基数
            base_value = 100  # 固定基数
            return self.intensity * base_value * self.ratio
        elif method == "hybrid":
            # 混合方法：线段长度和高度的平均
            return self.intensity * (line_length + height) / 2 * self.ratio
        else:
            return 0
    
    def paintEvent(self, event):
        """绘制偏移量缩放分析"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        
        try:
            # 定义多条不同长度的线段进行对比
            lines = [
                {"start": QPointF(100, 100), "end": QPointF(150, 200), "name": "短线段"},
                {"start": QPointF(200, 100), "end": QPointF(300, 300), "name": "中线段"},
                {"start": QPointF(350, 100), "end": QPointF(500, 400), "name": "长线段"},
                {"start": QPointF(550, 100), "end": QPointF(750, 500), "name": "超长线段"}
            ]
            
            colors = ["#4ECDC4", "#45B7D1", "#FF9F43", "#FF6B6B"]
            
            # 计算每条线段的信息
            for i, line_info in enumerate(lines):
                start = line_info["start"]
                end = line_info["end"]
                name = line_info["name"]
                color = colors[i]
                
                # 计算线段长度
                line_length = math.sqrt((end.x() - start.x())**2 + (end.y() - start.y())**2)
                
                # 计算中点
                mid_x = (start.x() + end.x()) / 2
                mid_y = (start.y() + end.y()) / 2
                
                # 根据选择的方法计算偏移量
                height = 300  # 固定梯形高度用于对比
                offset = self.calculate_offset(self.scaling_method, line_length, height)
                
                # 控制点
                control_point = QPointF(mid_x + offset, mid_y)
                
                # 1. 绘制原始线段
                painter.setPen(QPen(QColor("#CCCCCC"), 1, Qt.DashLine))
                painter.drawLine(start, end)
                
                # 2. 绘制贝塞尔曲线
                path = QPainterPath()
                path.moveTo(start)
                path.quadTo(control_point, end)
                
                painter.setPen(QPen(QColor(color), 3))
                painter.drawPath(path)
                
                # 3. 绘制控制点
                painter.setPen(QPen(QColor(color), 2))
                painter.setBrush(QColor(color))
                painter.drawEllipse(control_point, 6, 6)
                
                # 4. 绘制起点和终点
                painter.drawEllipse(start, 4, 4)
                painter.drawEllipse(end, 4, 4)
                
                # 5. 标注信息
                painter.setPen(QColor("#333333"))
                painter.drawText(start.x() - 20, start.y() - 10, name)
                painter.drawText(start.x() - 20, start.y() + 5, f"长度: {line_length:.0f}px")
                painter.drawText(start.x() - 20, start.y() + 20, f"偏移: {offset:.1f}px")
                
                # 计算偏移比例
                offset_ratio = offset / line_length if line_length > 0 else 0
                painter.drawText(start.x() - 20, start.y() + 35, f"比例: {offset_ratio:.2f}")
            
            # 6. 绘制详细分析面板
            info_x = 800
            painter.setPen(QColor("#333333"))
            painter.drawText(info_x, 50, "偏移量计算方法对比")
            painter.drawText(info_x, 70, "=" * 25)
            
            # 当前方法说明
            method_names = {
                "current": "当前方法 (基于高度)",
                "line_length": "线段长度方法",
                "fixed": "固定基数方法", 
                "hybrid": "混合方法"
            }
            
            painter.drawText(info_x, 100, f"当前方法: {method_names.get(self.scaling_method, '未知')}")
            painter.drawText(info_x, 120, f"强度: {self.intensity:.2f}")
            painter.drawText(info_x, 140, f"比例: {self.ratio:.2f}")
            
            # 方法详解
            painter.drawText(info_x, 170, "计算公式:")
            if self.scaling_method == "current":
                painter.drawText(info_x, 190, "偏移 = 强度 × 高度 × 比例")
                painter.drawText(info_x, 210, f"偏移 = {self.intensity} × 300 × {self.ratio}")
                painter.drawText(info_x, 230, f"偏移 = {self.intensity * 300 * self.ratio:.1f}px")
                painter.setPen(QColor("#FF6B6B"))
                painter.drawText(info_x, 250, "特点: 所有线段偏移相同")
            elif self.scaling_method == "line_length":
                painter.drawText(info_x, 190, "偏移 = 强度 × 线段长度 × 比例")
                painter.setPen(QColor("#00AA00"))
                painter.drawText(info_x, 210, "特点: 偏移与线段长度成比例")
            elif self.scaling_method == "fixed":
                painter.drawText(info_x, 190, "偏移 = 强度 × 100 × 比例")
                painter.setPen(QColor("#45B7D1"))
                painter.drawText(info_x, 210, "特点: 固定基数，便于控制")
            elif self.scaling_method == "hybrid":
                painter.drawText(info_x, 190, "偏移 = 强度 × (长度+高度)/2 × 比例")
                painter.setPen(QColor("#FF9F43"))
                painter.drawText(info_x, 210, "特点: 综合考虑多个因素")
            
            painter.setPen(QColor("#333333"))
            
            # 优缺点分析
            painter.drawText(info_x, 280, "方法对比:")
            painter.drawText(info_x, 300, "─" * 25)
            
            painter.drawText(info_x, 320, "1. 当前方法 (基于高度):")
            painter.drawText(info_x, 340, "   ✓ 简单一致")
            painter.drawText(info_x, 360, "   ✗ 忽略线段长度差异")
            
            painter.drawText(info_x, 390, "2. 线段长度方法:")
            painter.drawText(info_x, 410, "   ✓ 视觉比例协调")
            painter.drawText(info_x, 430, "   ✗ 短线段弯曲不明显")
            
            painter.drawText(info_x, 460, "3. 固定基数方法:")
            painter.drawText(info_x, 480, "   ✓ 参数含义明确")
            painter.drawText(info_x, 500, "   ✗ 需要手动调节基数")
            
            painter.drawText(info_x, 530, "4. 混合方法:")
            painter.drawText(info_x, 550, "   ✓ 平衡各种因素")
            painter.drawText(info_x, 570, "   ✗ 计算稍复杂")
            
            # 建议
            painter.setPen(QColor("#FF6B6B"))
            painter.drawText(info_x, 600, "💡 建议:")
            painter.drawText(info_x, 620, "根据应用场景选择:")
            painter.drawText(info_x, 640, "• 统一效果 → 当前方法")
            painter.drawText(info_x, 660, "• 比例协调 → 线段长度方法")
            
        except Exception as e:
            print(f"绘图错误: {e}")
        finally:
            painter.end()


class OffsetScalingWindow(QMainWindow):
    """偏移量缩放分析窗口"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("偏移量缩放方法分析 - 不同计算方式对比")
        self.setGeometry(100, 100, 1100, 900)
        
        # 创建中心Widget和布局
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # 添加标题
        title = QLabel("偏移量缩放方法对比分析")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold; margin: 10px;")
        layout.addWidget(title)
        
        # 创建演示Widget
        self.demo_widget = OffsetScalingWidget()
        layout.addWidget(self.demo_widget)
        
        # 创建控制面板
        controls_layout = QHBoxLayout()
        
        # 缩放方法选择
        method_layout = QVBoxLayout()
        method_layout.addWidget(QLabel("计算方法:"))
        self.method_combo = QComboBox()
        self.method_combo.addItems([
            "当前方法 (基于高度)",
            "线段长度方法", 
            "固定基数方法",
            "混合方法"
        ])
        method_layout.addWidget(self.method_combo)
        controls_layout.addLayout(method_layout)
        
        # 强度滑块
        intensity_layout = QVBoxLayout()
        intensity_layout.addWidget(QLabel("弯曲强度:"))
        self.intensity_slider = QSlider(Qt.Horizontal)
        self.intensity_slider.setRange(10, 100)
        self.intensity_slider.setValue(30)
        self.intensity_label = QLabel("0.30")
        intensity_layout.addWidget(self.intensity_slider)
        intensity_layout.addWidget(self.intensity_label)
        controls_layout.addLayout(intensity_layout)
        
        # 比例滑块
        ratio_layout = QVBoxLayout()
        ratio_layout.addWidget(QLabel("控制点比例:"))
        self.ratio_slider = QSlider(Qt.Horizontal)
        self.ratio_slider.setRange(10, 50)
        self.ratio_slider.setValue(30)
        self.ratio_label = QLabel("0.30")
        ratio_layout.addWidget(self.ratio_slider)
        ratio_layout.addWidget(self.ratio_label)
        controls_layout.addLayout(ratio_layout)
        
        layout.addLayout(controls_layout)
        
        # 连接事件
        self.method_combo.currentIndexChanged.connect(self.update_parameters)
        self.intensity_slider.valueChanged.connect(self.update_parameters)
        self.ratio_slider.valueChanged.connect(self.update_parameters)
        
        # 添加详细说明
        info_text = """
🔍 偏移量计算方法分析:

📐 当前方法 (基于梯形高度):
• 公式: 偏移 = 弯曲强度 × 梯形高度 × 控制点比例
• 特点: 所有线段使用相同的偏移量，与线段长度无关
• 优点: 简单一致，参数含义明确
• 缺点: 忽略了线段长度的差异，可能导致视觉不协调

📏 线段长度方法:
• 公式: 偏移 = 弯曲强度 × 线段长度 × 控制点比例  
• 特点: 偏移量与线段长度成正比
• 优点: 视觉比例协调，长短线段弯曲程度相对一致
• 缺点: 短线段弯曲可能不够明显

🔧 固定基数方法:
• 公式: 偏移 = 弯曲强度 × 固定基数 × 控制点比例
• 特点: 使用固定的基础数值 (如100像素)
• 优点: 参数含义直观，易于理解和控制
• 缺点: 需要根据应用场景手动选择合适的基数

⚖️ 混合方法:
• 公式: 偏移 = 弯曲强度 × (线段长度 + 高度) / 2 × 控制点比例
• 特点: 综合考虑线段长度和高度
• 优点: 平衡各种因素，适应性强
• 缺点: 计算稍复杂，参数调节需要经验

💡 选择建议:
• 如果希望所有线段有统一的弯曲效果 → 使用当前方法
• 如果希望视觉比例协调 → 使用线段长度方法
• 如果希望参数直观易控制 → 使用固定基数方法
• 如果希望综合平衡 → 使用混合方法
        """
        
        info_label = QLabel(info_text)
        info_label.setStyleSheet(
            "margin: 10px; padding: 10px; "
            "background-color: #F8F9FA; border: 1px solid #DEE2E6; "
            "border-radius: 5px; font-size: 9px;"
        )
        layout.addWidget(info_label)
    
    def update_parameters(self):
        """更新参数并重绘"""
        method_map = {
            0: "current",
            1: "line_length", 
            2: "fixed",
            3: "hybrid"
        }
        
        method = method_map[self.method_combo.currentIndex()]
        intensity = self.intensity_slider.value() / 100.0
        ratio = self.ratio_slider.value() / 100.0
        
        # 更新标签
        self.intensity_label.setText(f"{intensity:.2f}")
        self.ratio_label.setText(f"{ratio:.2f}")
        
        # 更新演示Widget
        self.demo_widget.set_parameters(method, intensity, ratio)


def main():
    """应用程序入口点"""
    app = QApplication(sys.argv)
    
    # 创建演示窗口
    window = OffsetScalingWindow()
    window.show()
    
    # 运行应用程序
    sys.exit(app.exec())


if __name__ == "__main__":
    main()