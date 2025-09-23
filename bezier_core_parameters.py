#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
贝塞尔曲线核心参数分析
分析真正决定贝塞尔曲线形状的最终参数
"""

import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                               QHBoxLayout, QLabel, QSlider)
from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QPainter, QPen, QColor, QPainterPath


class BezierCoreWidget(QWidget):
    """贝塞尔曲线核心参数演示Widget"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # 核心参数：真正决定贝塞尔曲线形状的3个参数
        self.top_offset = 0          # 上底平移量 (像素)
        self.position_ratio = 0.5    # 控制点位置比例 (0.0-1.0)
        self.curve_offset = 0        # 横向偏移量 (像素)
        
        # 固定的几何参数 (不影响曲线形状，只影响显示位置和尺寸)
        self.trapezoid_height = 200
        self.trapezoid_top = 20
        self.trapezoid_bottom = 200
        
        self.setFixedSize(600, 400)
        self.setStyleSheet("background-color: #FFFFFF; border: 2px solid #333333;")
    
    def set_core_parameters(self, top_offset, position_ratio, curve_offset):
        """设置核心参数"""
        self.top_offset = top_offset
        self.position_ratio = position_ratio
        self.curve_offset = curve_offset
        self.update()
    
    def create_bezier_curve(self, start_point, end_point):
        """创建贝塞尔曲线 - 只依赖核心参数"""
        path = QPainterPath()
        path.moveTo(start_point)
        
        # 核心参数1: 控制点位置比例 (决定控制点在线段上的位置)
        base_x = start_point.x() + (end_point.x() - start_point.x()) * self.position_ratio
        base_y = start_point.y() + (end_point.y() - start_point.y()) * self.position_ratio
        
        # 核心参数2: 横向偏移量 (决定弯曲程度和方向)
        control_point = QPointF(base_x + self.curve_offset, base_y)
        
        path.quadTo(control_point, end_point)
        return path, control_point
    
    def paintEvent(self, event):
        """绘制贝塞尔曲线核心参数演示"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        
        try:
            # 计算基础位置
            center_x = self.width() / 2
            start_y = (self.height() - self.trapezoid_height) / 2
            
            # 核心参数3: 上底平移量 (决定起点和终点的相对位置)
            top_center_x = center_x + self.top_offset
            
            # 计算梯形顶点
            top_left_x = top_center_x - self.trapezoid_top / 2
            top_right_x = top_center_x + self.trapezoid_top / 2
            bottom_left_x = center_x - self.trapezoid_bottom / 2
            bottom_right_x = center_x + self.trapezoid_bottom / 2
            
            top_y = start_y
            bottom_y = start_y + self.trapezoid_height
            
            # 定义关键点
            top_left = QPointF(top_left_x, top_y)
            top_right = QPointF(top_right_x, top_y)
            bottom_left = QPointF(bottom_left_x, bottom_y)
            bottom_right = QPointF(bottom_right_x, bottom_y)
            
            # 绘制参考线段 (直线)
            painter.setPen(QPen(QColor("#CCCCCC"), 1, Qt.DashLine))
            painter.drawLine(top_left, bottom_left)
            painter.drawLine(top_right, bottom_right)
            
            # 绘制贝塞尔曲线
            left_curve, left_control = self.create_bezier_curve(top_left, bottom_left)
            right_curve, right_control = self.create_bezier_curve(top_right, bottom_right)
            
            painter.setPen(QPen(QColor("#FF6B6B"), 4))
            painter.drawPath(left_curve)
            painter.drawPath(right_curve)
            
            # 绘制关键点
            # 起点和终点
            painter.setPen(QPen(QColor("#4ECDC4"), 2))
            painter.setBrush(QColor("#4ECDC4"))
            painter.drawEllipse(top_left, 6, 6)
            painter.drawEllipse(top_right, 6, 6)
            painter.drawEllipse(bottom_left, 6, 6)
            painter.drawEllipse(bottom_right, 6, 6)
            
            # 控制点
            painter.setPen(QPen(QColor("#FF9F43"), 2))
            painter.setBrush(QColor("#FF9F43"))
            painter.drawEllipse(left_control, 8, 8)
            painter.drawEllipse(right_control, 8, 8)
            
            # 绘制控制线
            painter.setPen(QPen(QColor("#FF9F43"), 1, Qt.DashLine))
            painter.drawLine(top_left, left_control)
            painter.drawLine(left_control, bottom_left)
            painter.drawLine(top_right, right_control)
            painter.drawLine(right_control, bottom_right)
            
            # 标注
            painter.setPen(QColor("#333333"))
            painter.drawText(10, 30, "贝塞尔曲线核心参数分析")
            painter.drawText(10, 50, "=" * 30)
            
            painter.drawText(10, 80, f"参数1 - 上底平移量: {self.top_offset:+.0f} 像素")
            painter.drawText(10, 100, f"参数2 - 控制点位置比例: {self.position_ratio:.2f}")
            painter.drawText(10, 120, f"参数3 - 横向偏移量: {self.curve_offset:+.0f} 像素")
            
            painter.drawText(10, 150, "影响分析:")
            painter.drawText(10, 170, f"• 上底平移 → 改变起点终点相对位置")
            painter.drawText(10, 190, f"• 位置比例 → 控制点在线段上的位置")
            painter.drawText(10, 210, f"• 横向偏移 → 弯曲程度和方向")
            
            # 数学表达
            painter.drawText(350, 80, "数学表达:")
            painter.drawText(350, 100, "起点: (x₀ + 上底平移, y₀)")
            painter.drawText(350, 120, "终点: (x₁, y₁)")
            painter.drawText(350, 140, "控制点X: x₀ + (x₁-x₀) × 位置比例 + 横向偏移")
            painter.drawText(350, 160, "控制点Y: y₀ + (y₁-y₀) × 位置比例")
            
            painter.drawText(350, 190, "贝塞尔曲线公式:")
            painter.drawText(350, 210, "B(t) = (1-t)²P₀ + 2(1-t)tP₁ + t²P₂")
            painter.drawText(350, 230, "其中 P₀=起点, P₁=控制点, P₂=终点")
            
        except Exception as e:
            print(f"绘图错误: {e}")
        finally:
            painter.end()


class BezierCoreWindow(QMainWindow):
    """贝塞尔曲线核心参数分析窗口"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("贝塞尔曲线核心参数分析 - 3个参数决定曲线形状")
        self.setGeometry(100, 100, 800, 600)
        
        # 创建中心Widget和布局
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # 添加标题
        title = QLabel("🔍 贝塞尔曲线的3个核心参数")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold; margin: 10px;")
        layout.addWidget(title)
        
        # 创建演示Widget
        self.demo_widget = BezierCoreWidget()
        layout.addWidget(self.demo_widget)
        
        # 创建控制面板
        controls_layout = QHBoxLayout()
        
        # 上底平移量
        offset_layout = QVBoxLayout()
        offset_layout.addWidget(QLabel("上底平移量:"))
        self.offset_slider = QSlider(Qt.Horizontal)
        self.offset_slider.setRange(-150, 150)
        self.offset_slider.setValue(0)
        self.offset_label = QLabel("0 px")
        offset_layout.addWidget(self.offset_slider)
        offset_layout.addWidget(self.offset_label)
        controls_layout.addLayout(offset_layout)
        
        # 控制点位置比例
        position_layout = QVBoxLayout()
        position_layout.addWidget(QLabel("控制点位置比例:"))
        self.position_slider = QSlider(Qt.Horizontal)
        self.position_slider.setRange(0, 100)
        self.position_slider.setValue(50)
        self.position_label = QLabel("0.50")
        position_layout.addWidget(self.position_slider)
        position_layout.addWidget(self.position_label)
        controls_layout.addLayout(position_layout)
        
        # 横向偏移量
        curve_layout = QVBoxLayout()
        curve_layout.addWidget(QLabel("横向偏移量:"))
        self.curve_slider = QSlider(Qt.Horizontal)
        self.curve_slider.setRange(-100, 100)
        self.curve_slider.setValue(0)
        self.curve_label = QLabel("0 px")
        curve_layout.addWidget(self.curve_slider)
        curve_layout.addWidget(self.curve_label)
        controls_layout.addLayout(curve_layout)
        
        layout.addLayout(controls_layout)
        
        # 连接事件
        self.offset_slider.valueChanged.connect(self.update_parameters)
        self.position_slider.valueChanged.connect(self.update_parameters)
        self.curve_slider.valueChanged.connect(self.update_parameters)
        
        # 添加说明
        info_text = """
🎯 核心结论：贝塞尔曲线形状由且仅由3个参数决定

📐 参数1 - 上底平移量:
• 决定起点和终点的相对位置关系
• 影响整个梯形的倾斜程度
• 在船舶应用中对应舵角的横向效果

📍 参数2 - 控制点位置比例:
• 决定控制点在起点-终点连线上的位置
• 0.0 = 靠近起点，0.5 = 中点，1.0 = 靠近终点
• 影响弯曲的"重心"位置

↔️ 参数3 - 横向偏移量:
• 决定控制点偏离直线的距离和方向
• 正值向右弯曲，负值向左弯曲，零值为直线
• 绝对值越大弯曲越明显

💡 重要发现:
• 其他所有参数（梯形尺寸、颜色、线宽等）都不影响曲线的几何形状
• 这3个参数是贝塞尔曲线的"最小完备参数集"
• 任何复杂的参数配置最终都会归结为这3个核心参数的值

🚢 在船舶转向应用中:
• 舵角、船速、转弯强度等界面参数最终都转换为这3个核心参数
• 这就是为什么我们可以用最少的参数实现最精确的控制
        """
        
        info_label = QLabel(info_text)
        info_label.setStyleSheet(
            "margin: 10px; padding: 10px; "
            "background-color: #F8F9FA; border: 1px solid #DEE2E6; "
            "border-radius: 5px; font-size: 9px;"
        )
        layout.addWidget(info_label)
    
    def update_parameters(self):
        """更新参数"""
        top_offset = self.offset_slider.value()
        position_ratio = self.position_slider.value() / 100.0
        curve_offset = self.curve_slider.value()
        
        # 更新标签
        self.offset_label.setText(f"{top_offset:+d} px")
        self.position_label.setText(f"{position_ratio:.2f}")
        self.curve_label.setText(f"{curve_offset:+d} px")
        
        # 更新演示
        self.demo_widget.set_core_parameters(top_offset, position_ratio, curve_offset)


def main():
    """应用程序入口点"""
    app = QApplication(sys.argv)
    
    # 创建分析窗口
    window = BezierCoreWindow()
    window.show()
    
    # 运行应用程序
    sys.exit(app.exec())


if __name__ == "__main__":
    main()