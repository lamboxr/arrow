#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化参数控制程序
直接使用偏移量和位置比例两个参数控制弯曲效果
"""

import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                               QHBoxLayout, QLabel, QSlider)
from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QPainter, QLinearGradient, QPen, QColor, QPainterPath


# 颜色定义
COLORS = {
    'top': '#B6B384',
    'middle': '#FEFFAF',
    'bottom': '#B7B286',
    'outline': '#B7B286'
}

# 基础尺寸参数
BASE_DIMENSIONS = {
    'height': 300,
    'top_base': 30,
    'bottom_base': 500,
    'outline_width': 2,
    'left_offset': 200
}


class SimplifiedTrapezoidWidget(QWidget):
    """简化参数的梯形Widget"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # 简化后的参数
        self.offset_amount = 27.0      # 直接控制偏移量（像素）
        self.position_ratio = 0.5      # 控制点在线段上的位置比例
        
        self.setMinimumSize(BASE_DIMENSIONS['bottom_base'] + 100, BASE_DIMENSIONS['height'] + 100)
        self.setStyleSheet("background-color: #BDC5D5;")
    
    def set_parameters(self, offset_amount, position_ratio):
        """设置简化参数"""
        self.offset_amount = offset_amount
        self.position_ratio = position_ratio
        self.update()
    
    def _create_trapezoid_geometry(self):
        """创建弯曲梯形的关键点坐标"""
        widget_width = self.width()
        widget_height = self.height()
        
        center_x = widget_width / 2
        start_y = (widget_height - BASE_DIMENSIONS['height']) / 2
        
        # 计算弯曲后的上底位置
        curved_center_x = center_x - BASE_DIMENSIONS['left_offset']
        
        # 计算上底的左右端点
        top_left_x = curved_center_x - BASE_DIMENSIONS['top_base'] / 2
        top_right_x = curved_center_x + BASE_DIMENSIONS['top_base'] / 2
        top_y = start_y
        
        # 下底保持原位置不变
        bottom_left_x = center_x - BASE_DIMENSIONS['bottom_base'] / 2
        bottom_right_x = center_x + BASE_DIMENSIONS['bottom_base'] / 2
        bottom_y = start_y + BASE_DIMENSIONS['height']
        
        return {
            'top_left': QPointF(top_left_x, top_y),
            'top_right': QPointF(top_right_x, top_y),
            'bottom_left': QPointF(bottom_left_x, bottom_y),
            'bottom_right': QPointF(bottom_right_x, bottom_y)
        }
    
    def _create_curved_path(self, start_point, end_point):
        """创建贝塞尔曲线路径（使用简化参数）"""
        path = QPainterPath()
        path.moveTo(start_point)
        
        # 计算基础位置（根据位置比例）
        base_x = start_point.x() + (end_point.x() - start_point.x()) * self.position_ratio
        base_y = start_point.y() + (end_point.y() - start_point.y()) * self.position_ratio
        
        # 直接使用偏移量（不需要复杂计算）
        control_point = QPointF(base_x + self.offset_amount, base_y)
        
        # 创建二次贝塞尔曲线
        path.quadTo(control_point, end_point)
        
        return path
    
    def _create_line_gradient(self, start_point, end_point):
        """创建渐变"""
        gradient = QLinearGradient(start_point, end_point)
        
        top_color = QColor(COLORS['top'])
        top_color.setAlpha(100)
        gradient.setColorAt(0.0, top_color)
        
        middle_color = QColor(COLORS['middle'])
        middle_color.setAlpha(200)
        gradient.setColorAt(0.5, middle_color)
        
        bottom_color = QColor(COLORS['bottom'])
        bottom_color.setAlpha(100)
        gradient.setColorAt(1.0, bottom_color)
        
        return gradient
    
    def _draw_trapezoid_outline(self, painter, geometry):
        """绘制弯曲梯形轮廓线"""
        top_left = geometry['top_left']
        top_right = geometry['top_right']
        bottom_left = geometry['bottom_left']
        bottom_right = geometry['bottom_right']
        
        # 绘制左腰线
        left_path = self._create_curved_path(top_left, bottom_left)
        left_gradient = self._create_line_gradient(top_left, bottom_left)
        left_pen = QPen()
        left_pen.setBrush(left_gradient)
        left_pen.setWidth(BASE_DIMENSIONS['outline_width'])
        left_pen.setCapStyle(Qt.RoundCap)
        painter.setPen(left_pen)
        painter.drawPath(left_path)
        
        # 绘制右腰线
        right_path = self._create_curved_path(top_right, bottom_right)
        right_gradient = self._create_line_gradient(top_right, bottom_right)
        right_pen = QPen()
        right_pen.setBrush(right_gradient)
        right_pen.setWidth(BASE_DIMENSIONS['outline_width'])
        right_pen.setCapStyle(Qt.RoundCap)
        painter.setPen(right_pen)
        painter.drawPath(right_path)
    
    def paintEvent(self, event):
        """绘制弯曲梯形"""
        painter = QPainter(self)
        
        try:
            painter.setRenderHint(QPainter.Antialiasing, True)
            
            # 创建几何形状
            geometry = self._create_trapezoid_geometry()
            
            # 绘制带渐变的弯曲腰线
            self._draw_trapezoid_outline(painter, geometry)
            
        except Exception as e:
            print(f"绘图过程中发生错误: {e}")
        finally:
            painter.end()


class SimplifiedControlWindow(QMainWindow):
    """简化控制窗口"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("简化参数控制 - 直接控制偏移量和位置")
        self.setGeometry(100, 100, 800, 700)
        
        # 创建中心Widget和布局
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # 添加标题
        title = QLabel("简化参数控制系统")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 20px; font-weight: bold; margin: 15px;")
        layout.addWidget(title)
        
        # 参数简化说明
        simplification_info = QLabel(
            "🎯 参数简化方案:\n"
            "❌ 原来: 弯曲强度 + 控制点比例 + 梯形高度 → 偏移量\n"
            "✅ 现在: 直接控制偏移量 + 位置比例\n\n"
            "💡 优势: 更直观、更简单、参数更少"
        )
        simplification_info.setStyleSheet(
            "background-color: #E3F2FD; padding: 15px; "
            "border: 1px solid #2196F3; border-radius: 8px; margin: 10px;"
        )
        layout.addWidget(simplification_info)
        
        # 创建梯形显示Widget
        self.trapezoid_widget = SimplifiedTrapezoidWidget()
        layout.addWidget(self.trapezoid_widget)
        
        # 创建控制面板
        controls_frame = QWidget()
        controls_frame.setStyleSheet(
            "background-color: #F5F5F5; border: 1px solid #CCCCCC; "
            "border-radius: 8px; padding: 15px; margin: 10px;"
        )
        controls_layout = QHBoxLayout(controls_frame)
        
        # 偏移量控制
        offset_layout = QVBoxLayout()
        offset_layout.addWidget(QLabel("偏移量 (像素):"))
        self.offset_slider = QSlider(Qt.Horizontal)
        self.offset_slider.setRange(0, 100)  # 0-100像素
        self.offset_slider.setValue(27)
        self.offset_label = QLabel("27.0px")
        offset_layout.addWidget(self.offset_slider)
        offset_layout.addWidget(self.offset_label)
        controls_layout.addLayout(offset_layout)
        
        # 位置比例控制
        position_layout = QVBoxLayout()
        position_layout.addWidget(QLabel("控制点位置比例:"))
        self.position_slider = QSlider(Qt.Horizontal)
        self.position_slider.setRange(0, 100)
        self.position_slider.setValue(50)
        self.position_label = QLabel("0.50 (中点)")
        position_layout.addWidget(self.position_slider)
        position_layout.addWidget(self.position_label)
        controls_layout.addLayout(position_layout)
        
        layout.addWidget(controls_frame)
        
        # 连接滑块事件
        self.offset_slider.valueChanged.connect(self.update_parameters)
        self.position_slider.valueChanged.connect(self.update_parameters)
        
        # 预设效果按钮区域
        presets_frame = QWidget()
        presets_frame.setStyleSheet(
            "background-color: #F8F9FA; border: 1px solid #DEE2E6; "
            "border-radius: 8px; padding: 10px; margin: 10px;"
        )
        presets_layout = QVBoxLayout(presets_frame)
        
        presets_title = QLabel("🎨 预设效果:")
        presets_title.setStyleSheet("font-weight: bold; margin-bottom: 5px;")
        presets_layout.addWidget(presets_title)
        
        buttons_layout = QHBoxLayout()
        
        from PySide6.QtWidgets import QPushButton
        
        # 预设按钮
        presets = [
            ("轻微弯曲", 10, 50),
            ("中等弯曲", 27, 50),
            ("强烈弯曲", 50, 50),
            ("起点弯曲", 30, 20),
            ("终点弯曲", 30, 80),
        ]
        
        for name, offset, position in presets:
            btn = QPushButton(name)
            btn.clicked.connect(lambda checked, o=offset, p=position: self.apply_preset(o, p))
            btn.setStyleSheet("padding: 5px 10px; margin: 2px;")
            buttons_layout.addWidget(btn)
        
        presets_layout.addLayout(buttons_layout)
        layout.addWidget(presets_frame)
        
        # 添加对比说明
        comparison_info = QLabel(
            "📊 参数对比:\n"
            "• 原系统: 3个参数 (弯曲强度 × 控制点比例 × 高度 = 偏移量)\n"
            "• 新系统: 2个参数 (偏移量 + 位置比例)\n"
            "• 效果: 完全相同，但控制更直观简单"
        )
        comparison_info.setStyleSheet(
            "margin: 10px; padding: 10px; "
            "background-color: #E8F5E8; border: 1px solid #4CAF50; "
            "border-radius: 5px; font-size: 11px;"
        )
        layout.addWidget(comparison_info)
    
    def update_parameters(self):
        """更新参数并重绘"""
        offset = self.offset_slider.value()
        position = self.position_slider.value() / 100.0
        
        # 更新标签
        self.offset_label.setText(f"{offset}.0px")
        
        position_text = f"{position:.2f}"
        if position <= 0.1:
            position_text += " (起点)"
        elif 0.4 <= position <= 0.6:
            position_text += " (中点)"
        elif position >= 0.9:
            position_text += " (终点)"
        self.position_label.setText(position_text)
        
        # 更新梯形Widget
        self.trapezoid_widget.set_parameters(offset, position)
    
    def apply_preset(self, offset, position):
        """应用预设效果"""
        self.offset_slider.setValue(offset)
        self.position_slider.setValue(position)


def main():
    """应用程序入口点"""
    app = QApplication(sys.argv)
    
    # 创建简化控制窗口
    window = SimplifiedControlWindow()
    window.show()
    
    # 运行应用程序
    sys.exit(app.exec())


if __name__ == "__main__":
    main()