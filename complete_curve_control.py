#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完整弯曲控制程序
包含三个核心参数：上底平移距离 + 偏移量 + 位置比例
"""

import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                               QHBoxLayout, QLabel, QSlider, QPushButton, QGroupBox)
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
    'outline_width': 2
}


class CompleteTrapezoidWidget(QWidget):
    """完整参数控制的梯形Widget"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # 三个核心参数
        self.top_offset = 200.0        # 上底平移距离（像素，负值向右，正值向左）
        self.curve_offset = 27.0       # 弯曲偏移量（像素）
        self.position_ratio = 0.5      # 控制点位置比例（0.0-1.0）
        
        self.setMinimumSize(BASE_DIMENSIONS['bottom_base'] + 200, BASE_DIMENSIONS['height'] + 100)
        self.setStyleSheet("background-color: #BDC5D5;")
    
    def set_parameters(self, top_offset, curve_offset, position_ratio):
        """设置完整参数"""
        self.top_offset = top_offset
        self.curve_offset = curve_offset
        self.position_ratio = position_ratio
        self.update()
    
    def _create_trapezoid_geometry(self):
        """创建弯曲梯形的关键点坐标"""
        widget_width = self.width()
        widget_height = self.height()
        
        center_x = widget_width / 2
        start_y = (widget_height - BASE_DIMENSIONS['height']) / 2
        
        # 计算上底位置（使用平移参数）
        curved_center_x = center_x - self.top_offset  # 正值向左，负值向右
        
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
        """创建贝塞尔曲线路径"""
        path = QPainterPath()
        path.moveTo(start_point)
        
        # 计算基础位置（根据位置比例）
        base_x = start_point.x() + (end_point.x() - start_point.x()) * self.position_ratio
        base_y = start_point.y() + (end_point.y() - start_point.y()) * self.position_ratio
        
        # 使用弯曲偏移量
        control_point = QPointF(base_x + self.curve_offset, base_y)
        
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
        
        # 绘制参考线（可选）
        if hasattr(self, 'show_guides') and self.show_guides:
            self._draw_guide_lines(painter, geometry)
    
    def _draw_guide_lines(self, painter, geometry):
        """绘制辅助参考线"""
        painter.setPen(QPen(QColor("#FF0000"), 1, Qt.DashLine))
        
        # 绘制中心线
        center_x = self.width() / 2
        painter.drawLine(QPointF(center_x, 0), QPointF(center_x, self.height()))
        
        # 绘制上底中心线
        top_center_x = (geometry['top_left'].x() + geometry['top_right'].x()) / 2
        painter.drawLine(QPointF(top_center_x, 0), QPointF(top_center_x, self.height()))
        
        # 标注偏移距离
        painter.setPen(QColor("#FF0000"))
        offset_text = f"偏移: {self.top_offset:.0f}px"
        painter.drawText(10, 30, offset_text)
    
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


class CompleteControlWindow(QMainWindow):
    """完整参数控制窗口"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("完整弯曲控制系统 - 三参数精确控制")
        self.setGeometry(100, 100, 900, 800)
        
        # 创建中心Widget和布局
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # 添加标题
        title = QLabel("完整弯曲控制系统")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 22px; font-weight: bold; margin: 15px;")
        layout.addWidget(title)
        
        # 参数说明
        param_info = QLabel(
            "🎯 三参数控制系统:\n"
            "1️⃣ 上底平移距离: 控制梯形的整体倾斜程度\n"
            "2️⃣ 弯曲偏移量: 控制腰线的弯曲程度\n"
            "3️⃣ 控制点位置比例: 控制弯曲的重心位置"
        )
        param_info.setStyleSheet(
            "background-color: #E3F2FD; padding: 15px; "
            "border: 1px solid #2196F3; border-radius: 8px; margin: 10px;"
        )
        layout.addWidget(param_info)
        
        # 创建梯形显示Widget
        self.trapezoid_widget = CompleteTrapezoidWidget()
        layout.addWidget(self.trapezoid_widget)
        
        # 创建控制面板
        controls_frame = QWidget()
        controls_frame.setStyleSheet(
            "background-color: #F5F5F5; border: 1px solid #CCCCCC; "
            "border-radius: 8px; padding: 15px; margin: 10px;"
        )
        controls_layout = QHBoxLayout(controls_frame)
        
        # 上底平移距离控制
        top_offset_group = QGroupBox("上底平移距离")
        top_offset_layout = QVBoxLayout(top_offset_group)
        
        self.top_offset_slider = QSlider(Qt.Horizontal)
        self.top_offset_slider.setRange(-200, 400)  # -200到400像素
        self.top_offset_slider.setValue(200)
        self.top_offset_label = QLabel("200px (向左)")
        
        top_offset_layout.addWidget(QLabel("← 向右    向左 →"))
        top_offset_layout.addWidget(self.top_offset_slider)
        top_offset_layout.addWidget(self.top_offset_label)
        controls_layout.addWidget(top_offset_group)
        
        # 弯曲偏移量控制
        curve_offset_group = QGroupBox("弯曲偏移量")
        curve_offset_layout = QVBoxLayout(curve_offset_group)
        
        self.curve_offset_slider = QSlider(Qt.Horizontal)
        self.curve_offset_slider.setRange(0, 100)  # 0-100像素
        self.curve_offset_slider.setValue(27)
        self.curve_offset_label = QLabel("27px")
        
        curve_offset_layout.addWidget(QLabel("直线 ← → 弯曲"))
        curve_offset_layout.addWidget(self.curve_offset_slider)
        curve_offset_layout.addWidget(self.curve_offset_label)
        controls_layout.addWidget(curve_offset_group)
        
        # 位置比例控制
        position_group = QGroupBox("控制点位置比例")
        position_layout = QVBoxLayout(position_group)
        
        self.position_slider = QSlider(Qt.Horizontal)
        self.position_slider.setRange(0, 100)
        self.position_slider.setValue(50)
        self.position_label = QLabel("0.50 (中点)")
        
        position_layout.addWidget(QLabel("起点 ← → 终点"))
        position_layout.addWidget(self.position_slider)
        position_layout.addWidget(self.position_label)
        controls_layout.addWidget(position_group)
        
        layout.addWidget(controls_frame)
        
        # 连接滑块事件
        self.top_offset_slider.valueChanged.connect(self.update_parameters)
        self.curve_offset_slider.valueChanged.connect(self.update_parameters)
        self.position_slider.valueChanged.connect(self.update_parameters)
        
        # 预设效果区域
        presets_frame = QWidget()
        presets_frame.setStyleSheet(
            "background-color: #F8F9FA; border: 1px solid #DEE2E6; "
            "border-radius: 8px; padding: 15px; margin: 10px;"
        )
        presets_layout = QVBoxLayout(presets_frame)
        
        presets_title = QLabel("🎨 预设效果:")
        presets_title.setStyleSheet("font-weight: bold; margin-bottom: 10px;")
        presets_layout.addWidget(presets_title)
        
        # 预设按钮组
        presets_grid = QHBoxLayout()
        
        # 预设配置 (上底偏移, 弯曲偏移, 位置比例)
        presets = [
            ("直立梯形", 0, 0, 50),
            ("轻微左倾", 100, 15, 50),
            ("中度左倾", 200, 27, 50),
            ("强烈左倾", 300, 40, 50),
            ("右倾梯形", -100, 20, 50),
            ("起点弯曲", 200, 35, 20),
            ("终点弯曲", 200, 35, 80),
            ("S型弯曲", 150, 60, 30),
        ]
        
        for name, top_offset, curve_offset, position in presets:
            btn = QPushButton(name)
            btn.clicked.connect(lambda checked, t=top_offset, c=curve_offset, p=position: 
                              self.apply_preset(t, c, p))
            btn.setStyleSheet("padding: 8px 12px; margin: 2px;")
            presets_grid.addWidget(btn)
        
        presets_layout.addLayout(presets_grid)
        layout.addWidget(presets_frame)
        
        # 辅助功能
        tools_frame = QWidget()
        tools_layout = QHBoxLayout(tools_frame)
        
        # 显示参考线按钮
        self.guide_btn = QPushButton("显示参考线")
        self.guide_btn.setCheckable(True)
        self.guide_btn.clicked.connect(self.toggle_guide_lines)
        tools_layout.addWidget(self.guide_btn)
        
        # 重置按钮
        reset_btn = QPushButton("重置为默认")
        reset_btn.clicked.connect(lambda: self.apply_preset(200, 27, 50))
        tools_layout.addWidget(reset_btn)
        
        tools_layout.addStretch()
        layout.addWidget(tools_frame)
        
        # 添加参数说明
        explanation_info = QLabel(
            "📐 参数详解:\n"
            "• 上底平移距离: 正值向左移动，负值向右移动，0为居中\n"
            "• 弯曲偏移量: 控制腰线向右凸起的程度，0为直线\n"
            "• 控制点位置比例: 0.0在起点附近弯曲，0.5在中点弯曲，1.0在终点附近弯曲\n\n"
            "💡 组合效果: 三个参数独立控制，可以创造出丰富的梯形变形效果"
        )
        explanation_info.setStyleSheet(
            "margin: 10px; padding: 15px; "
            "background-color: #E8F5E8; border: 1px solid #4CAF50; "
            "border-radius: 8px; font-size: 11px;"
        )
        layout.addWidget(explanation_info)
    
    def update_parameters(self):
        """更新参数并重绘"""
        top_offset = self.top_offset_slider.value()
        curve_offset = self.curve_offset_slider.value()
        position = self.position_slider.value() / 100.0
        
        # 更新标签
        direction = "向左" if top_offset > 0 else "向右" if top_offset < 0 else "居中"
        self.top_offset_label.setText(f"{abs(top_offset)}px ({direction})")
        
        self.curve_offset_label.setText(f"{curve_offset}px")
        
        position_text = f"{position:.2f}"
        if position <= 0.1:
            position_text += " (起点)"
        elif 0.4 <= position <= 0.6:
            position_text += " (中点)"
        elif position >= 0.9:
            position_text += " (终点)"
        self.position_label.setText(position_text)
        
        # 更新梯形Widget
        self.trapezoid_widget.set_parameters(top_offset, curve_offset, position)
    
    def apply_preset(self, top_offset, curve_offset, position):
        """应用预设效果"""
        self.top_offset_slider.setValue(top_offset)
        self.curve_offset_slider.setValue(curve_offset)
        self.position_slider.setValue(position)
    
    def toggle_guide_lines(self, checked):
        """切换参考线显示"""
        self.trapezoid_widget.show_guides = checked
        self.guide_btn.setText("隐藏参考线" if checked else "显示参考线")
        self.trapezoid_widget.update()


def main():
    """应用程序入口点"""
    app = QApplication(sys.argv)
    
    # 创建完整控制窗口
    window = CompleteControlWindow()
    window.show()
    
    # 运行应用程序
    sys.exit(app.exec())


if __name__ == "__main__":
    main()