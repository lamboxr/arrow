#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
控制点比例详细解释程序
可视化展示控制点比例的真实含义
"""

import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QPainter, QLinearGradient, QPen, QColor, QPainterPath


class ControlPointExplanationWidget(QWidget):
    """控制点解释Widget"""
    
    def __init__(self, curve_intensity=0.4, control_point_ratio=0.3, parent=None):
        super().__init__(parent)
        self.curve_intensity = curve_intensity
        self.control_point_ratio = control_point_ratio
        
        self.setFixedSize(600, 400)
        self.setStyleSheet("background-color: #FFFFFF; border: 2px solid #333333;")
    
    def paintEvent(self, event):
        """绘制控制点解释图"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        
        try:
            # 定义基本参数
            height = 200
            start_point = QPointF(100, 100)
            end_point = QPointF(150, 300)
            
            # 计算线段中点
            mid_x = (start_point.x() + end_point.x()) / 2
            mid_y = (start_point.y() + end_point.y()) / 2
            mid_point = QPointF(mid_x, mid_y)
            
            # 计算控制点偏移量
            offset_x = self.curve_intensity * height * self.control_point_ratio
            control_point = QPointF(mid_x + offset_x, mid_y)
            
            # 1. 绘制直线（参考线）
            painter.setPen(QPen(QColor("#CCCCCC"), 2, Qt.DashLine))
            painter.drawLine(start_point, end_point)
            
            # 2. 绘制贝塞尔曲线
            path = QPainterPath()
            path.moveTo(start_point)
            path.quadTo(control_point, end_point)
            
            painter.setPen(QPen(QColor("#FF6B6B"), 3))
            painter.drawPath(path)
            
            # 3. 绘制关键点
            # 起点
            painter.setPen(QPen(QColor("#4ECDC4"), 2))
            painter.setBrush(QColor("#4ECDC4"))
            painter.drawEllipse(start_point, 6, 6)
            
            # 终点
            painter.drawEllipse(end_point, 6, 6)
            
            # 中点
            painter.setPen(QPen(QColor("#45B7D1"), 2))
            painter.setBrush(QColor("#45B7D1"))
            painter.drawEllipse(mid_point, 6, 6)
            
            # 控制点
            painter.setPen(QPen(QColor("#FF9F43"), 2))
            painter.setBrush(QColor("#FF9F43"))
            painter.drawEllipse(control_point, 8, 8)
            
            # 4. 绘制辅助线
            # 中点到控制点的横向偏移线
            painter.setPen(QPen(QColor("#FF9F43"), 2, Qt.DashLine))
            painter.drawLine(mid_point, control_point)
            
            # 垂直参考线
            painter.setPen(QPen(QColor("#DDDDDD"), 1, Qt.DotLine))
            painter.drawLine(QPointF(mid_x, 50), QPointF(mid_x, 350))
            painter.drawLine(QPointF(control_point.x(), 50), QPointF(control_point.x(), 350))
            
            # 5. 添加标注
            painter.setPen(QColor("#333333"))
            painter.drawText(start_point.x() - 30, start_point.y() - 10, "起点")
            painter.drawText(end_point.x() - 30, end_point.y() + 20, "终点")
            painter.drawText(mid_point.x() - 30, mid_point.y() - 10, "中点")
            painter.drawText(control_point.x() + 10, control_point.y() - 10, "控制点")
            
            # 6. 绘制测量信息
            painter.drawText(300, 50, "控制点计算详解:")
            painter.drawText(300, 70, f"弯曲强度: {self.curve_intensity}")
            painter.drawText(300, 90, f"梯形高度: {height}")
            painter.drawText(300, 110, f"控制点比例: {self.control_point_ratio}")
            painter.drawText(300, 130, "─" * 25)
            painter.drawText(300, 150, f"横向偏移 = {self.curve_intensity} × {height} × {self.control_point_ratio}")
            painter.drawText(300, 170, f"横向偏移 = {offset_x:.1f} 像素")
            painter.drawText(300, 190, "─" * 25)
            painter.drawText(300, 210, "控制点位置 = 中点 + 横向偏移")
            painter.drawText(300, 230, f"控制点X = {mid_x:.1f} + {offset_x:.1f} = {control_point.x():.1f}")
            painter.drawText(300, 250, f"控制点Y = {mid_y:.1f} (保持不变)")
            
            # 7. 重要说明
            painter.setPen(QColor("#FF6B6B"))
            painter.drawText(300, 290, "⚠️ 重要:")
            painter.drawText(300, 310, "控制点比例 ≠ 线段距离比例")
            painter.drawText(300, 330, "控制点比例 = 横向偏移的缩放系数")
            painter.drawText(300, 350, "它决定控制点偏离中点的程度")
            
        except Exception as e:
            print(f"绘图错误: {e}")
        finally:
            painter.end()


class ControlPointExplanationWindow(QMainWindow):
    """控制点解释窗口"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("控制点比例详细解释")
        self.setGeometry(100, 100, 650, 500)
        
        # 创建中心Widget和布局
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # 添加标题
        title = QLabel("控制点比例的真实含义")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold; margin: 10px;")
        layout.addWidget(title)
        
        # 添加解释Widget
        explanation_widget = ControlPointExplanationWidget()
        layout.addWidget(explanation_widget)
        
        # 添加详细说明
        info_text = """
📐 控制点比例的含义:

1. 控制点比例 ≠ 线段上的距离比例
2. 控制点比例 = 横向偏移的缩放系数
3. 控制点总是位于线段中点的水平右侧
4. 偏移距离 = 弯曲强度 × 梯形高度 × 控制点比例

🎯 实际作用:
• 控制点比例越大 → 控制点越远离中点 → 弯曲越明显
• 控制点比例越小 → 控制点越接近中点 → 弯曲越轻微

💡 理解要点:
控制点比例是一个"放大系数"，它决定了基础偏移量(弯曲强度×高度)被放大多少倍。
        """
        
        info_label = QLabel(info_text)
        info_label.setStyleSheet(
            "margin: 10px; padding: 10px; "
            "background-color: #F8F9FA; border: 1px solid #DEE2E6; "
            "border-radius: 5px; font-size: 11px;"
        )
        layout.addWidget(info_label)


def main():
    """应用程序入口点"""
    app = QApplication(sys.argv)
    
    # 创建解释窗口
    window = ControlPointExplanationWindow()
    window.show()
    
    # 运行应用程序
    sys.exit(app.exec())


if __name__ == "__main__":
    main()