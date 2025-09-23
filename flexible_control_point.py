#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
灵活控制点位置演示程序
展示控制点可以在线段上任意位置进行偏移
"""

import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                               QHBoxLayout, QLabel, QSlider)
from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QPainter, QLinearGradient, QPen, QColor, QPainterPath


class FlexibleControlPointWidget(QWidget):
    """灵活控制点演示Widget"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # 控制参数
        self.curve_intensity = 0.4      # 弯曲强度
        self.control_point_ratio = 0.3  # 横向偏移比例
        self.position_ratio = 0.5       # 控制点在线段上的位置比例 (0.0=起点, 1.0=终点)
        
        self.setFixedSize(800, 500)
        self.setStyleSheet("background-color: #FFFFFF; border: 2px solid #333333;")
    
    def set_parameters(self, curve_intensity, control_point_ratio, position_ratio):
        """设置参数并重绘"""
        self.curve_intensity = curve_intensity
        self.control_point_ratio = control_point_ratio
        self.position_ratio = position_ratio
        self.update()
    
    def paintEvent(self, event):
        """绘制灵活控制点演示"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        
        try:
            # 定义基本参数
            height = 300
            start_point = QPointF(100, 100)
            end_point = QPointF(200, 400)
            
            # 计算控制点在线段上的基础位置
            base_x = start_point.x() + (end_point.x() - start_point.x()) * self.position_ratio
            base_y = start_point.y() + (end_point.y() - start_point.y()) * self.position_ratio
            base_point = QPointF(base_x, base_y)
            
            # 计算横向偏移量
            offset_x = self.curve_intensity * height * self.control_point_ratio
            control_point = QPointF(base_x + offset_x, base_y)
            
            # 1. 绘制直线（参考线）
            painter.setPen(QPen(QColor("#CCCCCC"), 2, Qt.DashLine))
            painter.drawLine(start_point, end_point)
            
            # 2. 绘制贝塞尔曲线
            path = QPainterPath()
            path.moveTo(start_point)
            path.quadTo(control_point, end_point)
            
            painter.setPen(QPen(QColor("#FF6B6B"), 4))
            painter.drawPath(path)
            
            # 3. 绘制关键点
            # 起点
            painter.setPen(QPen(QColor("#4ECDC4"), 2))
            painter.setBrush(QColor("#4ECDC4"))
            painter.drawEllipse(start_point, 8, 8)
            
            # 终点
            painter.drawEllipse(end_point, 8, 8)
            
            # 线段上的基础位置点
            painter.setPen(QPen(QColor("#45B7D1"), 2))
            painter.setBrush(QColor("#45B7D1"))
            painter.drawEllipse(base_point, 8, 8)
            
            # 控制点
            painter.setPen(QPen(QColor("#FF9F43"), 2))
            painter.setBrush(QColor("#FF9F43"))
            painter.drawEllipse(control_point, 10, 10)
            
            # 4. 绘制辅助线
            # 基础位置到控制点的偏移线
            painter.setPen(QPen(QColor("#FF9F43"), 2, Qt.DashLine))
            painter.drawLine(base_point, control_point)
            
            # 垂直参考线
            painter.setPen(QPen(QColor("#DDDDDD"), 1, Qt.DotLine))
            painter.drawLine(QPointF(base_x, 50), QPointF(base_x, 450))
            painter.drawLine(QPointF(control_point.x(), 50), QPointF(control_point.x(), 450))
            
            # 5. 添加标注
            painter.setPen(QColor("#333333"))
            painter.drawText(start_point.x() - 40, start_point.y() - 15, "起点 (0%)")
            painter.drawText(end_point.x() - 40, end_point.y() + 25, "终点 (100%)")
            painter.drawText(base_point.x() - 60, base_point.y() - 15, f"基础位置 ({self.position_ratio*100:.0f}%)")
            painter.drawText(control_point.x() + 15, control_point.y() - 10, "控制点")
            
            # 6. 绘制详细信息
            info_x = 350
            painter.drawText(info_x, 80, "控制点位置计算:")
            painter.drawText(info_x, 100, "─" * 30)
            painter.drawText(info_x, 120, f"1. 位置比例: {self.position_ratio:.2f}")
            painter.drawText(info_x, 140, f"   基础位置 = 起点 + (终点-起点) × {self.position_ratio:.2f}")
            painter.drawText(info_x, 160, f"   基础X = {start_point.x():.0f} + ({end_point.x():.0f}-{start_point.x():.0f}) × {self.position_ratio:.2f} = {base_x:.1f}")
            painter.drawText(info_x, 180, f"   基础Y = {start_point.y():.0f} + ({end_point.y():.0f}-{start_point.y():.0f}) × {self.position_ratio:.2f} = {base_y:.1f}")
            
            painter.drawText(info_x, 210, f"2. 横向偏移: {offset_x:.1f}像素")
            painter.drawText(info_x, 230, f"   偏移 = {self.curve_intensity} × {height} × {self.control_point_ratio} = {offset_x:.1f}")
            
            painter.drawText(info_x, 260, f"3. 最终控制点:")
            painter.drawText(info_x, 280, f"   控制点X = {base_x:.1f} + {offset_x:.1f} = {control_point.x():.1f}")
            painter.drawText(info_x, 300, f"   控制点Y = {base_y:.1f} (保持不变)")
            
            # 7. 不同位置比例的效果说明
            painter.setPen(QColor("#FF6B6B"))
            painter.drawText(info_x, 340, "💡 位置比例效果:")
            painter.drawText(info_x, 360, "• 0.0 = 控制点靠近起点 → 起点附近弯曲明显")
            painter.drawText(info_x, 380, "• 0.5 = 控制点在中点 → 中间弯曲明显")
            painter.drawText(info_x, 400, "• 1.0 = 控制点靠近终点 → 终点附近弯曲明显")
            
            # 8. 绘制线段上的位置标记
            painter.setPen(QPen(QColor("#999999"), 1))
            for i in range(11):  # 0%, 10%, 20%, ..., 100%
                ratio = i / 10.0
                mark_x = start_point.x() + (end_point.x() - start_point.x()) * ratio
                mark_y = start_point.y() + (end_point.y() - start_point.y()) * ratio
                painter.drawEllipse(QPointF(mark_x, mark_y), 2, 2)
                if i % 2 == 0:  # 只显示偶数标记的文字
                    painter.drawText(mark_x - 15, mark_y - 10, f"{int(ratio*100)}%")
            
        except Exception as e:
            print(f"绘图错误: {e}")
        finally:
            painter.end()


class FlexibleControlPointWindow(QMainWindow):
    """灵活控制点演示窗口"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("灵活控制点位置演示 - 控制点可以在线段任意位置")
        self.setGeometry(100, 100, 900, 700)
        
        # 创建中心Widget和布局
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # 添加标题
        title = QLabel("控制点可以在线段上任意位置进行偏移")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold; margin: 10px;")
        layout.addWidget(title)
        
        # 创建演示Widget
        self.demo_widget = FlexibleControlPointWidget()
        layout.addWidget(self.demo_widget)
        
        # 创建控制面板
        controls_layout = QHBoxLayout()
        
        # 弯曲强度滑块
        intensity_layout = QVBoxLayout()
        intensity_layout.addWidget(QLabel("弯曲强度:"))
        self.intensity_slider = QSlider(Qt.Horizontal)
        self.intensity_slider.setRange(0, 100)
        self.intensity_slider.setValue(40)
        self.intensity_label = QLabel("0.40")
        intensity_layout.addWidget(self.intensity_slider)
        intensity_layout.addWidget(self.intensity_label)
        controls_layout.addLayout(intensity_layout)
        
        # 控制点比例滑块
        ratio_layout = QVBoxLayout()
        ratio_layout.addWidget(QLabel("横向偏移比例:"))
        self.ratio_slider = QSlider(Qt.Horizontal)
        self.ratio_slider.setRange(0, 50)
        self.ratio_slider.setValue(30)
        self.ratio_label = QLabel("0.30")
        ratio_layout.addWidget(self.ratio_slider)
        ratio_layout.addWidget(self.ratio_label)
        controls_layout.addLayout(ratio_layout)
        
        # 位置比例滑块
        position_layout = QVBoxLayout()
        position_layout.addWidget(QLabel("控制点位置比例:"))
        self.position_slider = QSlider(Qt.Horizontal)
        self.position_slider.setRange(0, 100)
        self.position_slider.setValue(50)
        self.position_label = QLabel("0.50 (中点)")
        position_layout.addWidget(self.position_slider)
        position_layout.addWidget(self.position_label)
        controls_layout.addLayout(position_layout)
        
        layout.addLayout(controls_layout)
        
        # 连接滑块事件
        self.intensity_slider.valueChanged.connect(self.update_parameters)
        self.ratio_slider.valueChanged.connect(self.update_parameters)
        self.position_slider.valueChanged.connect(self.update_parameters)
        
        # 添加说明
        info_text = """
🎯 新增参数 - 控制点位置比例:
• 0.0: 控制点基于起点进行偏移 → 起点附近弯曲明显
• 0.5: 控制点基于中点进行偏移 → 中间弯曲明显 (默认)
• 1.0: 控制点基于终点进行偏移 → 终点附近弯曲明显

📐 完整计算公式:
基础位置 = 起点 + (终点 - 起点) × 位置比例
控制点 = 基础位置 + 横向偏移量

💡 实际应用:
通过调整位置比例，可以控制弯曲的"重心"位置，创造不同的视觉效果。
        """
        
        info_label = QLabel(info_text)
        info_label.setStyleSheet(
            "margin: 10px; padding: 10px; "
            "background-color: #F8F9FA; border: 1px solid #DEE2E6; "
            "border-radius: 5px; font-size: 11px;"
        )
        layout.addWidget(info_label)
    
    def update_parameters(self):
        """更新参数并重绘"""
        intensity = self.intensity_slider.value() / 100.0
        ratio = self.ratio_slider.value() / 100.0
        position = self.position_slider.value() / 100.0
        
        # 更新标签
        self.intensity_label.setText(f"{intensity:.2f}")
        self.ratio_label.setText(f"{ratio:.2f}")
        
        position_text = f"{position:.2f}"
        if position == 0.0:
            position_text += " (起点)"
        elif position == 0.5:
            position_text += " (中点)"
        elif position == 1.0:
            position_text += " (终点)"
        self.position_label.setText(position_text)
        
        # 更新演示Widget
        self.demo_widget.set_parameters(intensity, ratio, position)


def main():
    """应用程序入口点"""
    app = QApplication(sys.argv)
    
    # 创建演示窗口
    window = FlexibleControlPointWindow()
    window.show()
    
    # 运行应用程序
    sys.exit(app.exec())


if __name__ == "__main__":
    main()