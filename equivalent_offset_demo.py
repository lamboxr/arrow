#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
等效偏移量演示程序
验证：相同偏移量 + 相同位置比例 = 相同形态
"""

import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                               QHBoxLayout, QLabel, QFrame)
from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QPainter, QLinearGradient, QPen, QColor, QPainterPath


class EquivalentCurveWidget(QWidget):
    """等效曲线演示Widget"""
    
    def __init__(self, curve_intensity, control_point_ratio, position_ratio=0.5, 
                 title="", subtitle="", parent=None):
        super().__init__(parent)
        self.curve_intensity = curve_intensity
        self.control_point_ratio = control_point_ratio
        self.position_ratio = position_ratio
        self.title = title
        self.subtitle = subtitle
        
        self.setFixedSize(280, 200)
        self.setStyleSheet("background-color: #FFFFFF; border: 2px solid #333333; margin: 2px;")
    
    def _create_trapezoid_geometry(self):
        """创建弯曲梯形的关键点坐标"""
        widget_width = self.width()
        widget_height = self.height()
        
        # 计算梯形在Widget中的居中位置
        center_x = widget_width / 2
        start_y = (widget_height - 120) / 2 + 25  # 留出标题空间
        
        # 计算弯曲后的上底位置
        curved_center_x = center_x - 60  # 缩小的左移距离
        
        # 计算上底的左右端点
        top_left_x = curved_center_x - 8
        top_right_x = curved_center_x + 8
        top_y = start_y
        
        # 下底保持原位置不变
        bottom_left_x = center_x - 100
        bottom_right_x = center_x + 100
        bottom_y = start_y + 120
        
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
        
        # 计算向右的偏移量
        offset_x = self.curve_intensity * 120 * self.control_point_ratio  # 使用缩小的高度
        
        # 控制点位置
        control_point = QPointF(base_x + offset_x, base_y)
        
        # 创建二次贝塞尔曲线
        path.quadTo(control_point, end_point)
        
        return path
    
    def _create_line_gradient(self, start_point, end_point):
        """创建渐变"""
        gradient = QLinearGradient(start_point, end_point)
        
        top_color = QColor("#B6B384")
        top_color.setAlpha(120)
        gradient.setColorAt(0.0, top_color)
        
        middle_color = QColor("#FEFFAF")
        middle_color.setAlpha(220)
        gradient.setColorAt(0.5, middle_color)
        
        bottom_color = QColor("#B7B286")
        bottom_color.setAlpha(120)
        gradient.setColorAt(1.0, bottom_color)
        
        return gradient
    
    def paintEvent(self, event):
        """绘制弯曲梯形"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        
        try:
            # 创建几何形状
            geometry = self._create_trapezoid_geometry()
            
            # 绘制左腰线
            left_path = self._create_curved_path(geometry['top_left'], geometry['bottom_left'])
            left_gradient = self._create_line_gradient(geometry['top_left'], geometry['bottom_left'])
            left_pen = QPen()
            left_pen.setBrush(left_gradient)
            left_pen.setWidth(3)
            left_pen.setCapStyle(Qt.RoundCap)
            painter.setPen(left_pen)
            painter.drawPath(left_path)
            
            # 绘制右腰线
            right_path = self._create_curved_path(geometry['top_right'], geometry['bottom_right'])
            right_gradient = self._create_line_gradient(geometry['top_right'], geometry['bottom_right'])
            right_pen = QPen()
            right_pen.setBrush(right_gradient)
            right_pen.setWidth(3)
            right_pen.setCapStyle(Qt.RoundCap)
            painter.setPen(right_pen)
            painter.drawPath(right_path)
            
            # 绘制标题和参数信息
            painter.setPen(QColor("#333333"))
            painter.drawText(5, 15, self.title)
            painter.drawText(5, 30, self.subtitle)
            
            # 计算并显示偏移量
            offset = self.curve_intensity * 120 * self.control_point_ratio
            painter.drawText(5, 185, f"偏移:{offset:.1f}px")
            
        except Exception as e:
            print(f"绘图错误: {e}")
        finally:
            painter.end()


class EquivalentOffsetWindow(QMainWindow):
    """等效偏移量演示窗口"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("等效偏移量验证 - 相同偏移量产生相同形态")
        self.setGeometry(100, 100, 1200, 800)
        
        # 创建中心Widget和布局
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # 添加主标题
        main_title = QLabel("等效偏移量验证实验")
        main_title.setAlignment(Qt.AlignCenter)
        main_title.setStyleSheet("font-size: 20px; font-weight: bold; margin: 15px;")
        layout.addWidget(main_title)
        
        # 理论说明
        theory_label = QLabel(
            "🧮 理论假设: 偏移量 = 弯曲强度 × 高度 × 控制点比例\n"
            "💡 验证目标: 相同偏移量 + 相同位置比例 → 相同曲线形态"
        )
        theory_label.setAlignment(Qt.AlignCenter)
        theory_label.setStyleSheet(
            "background-color: #E3F2FD; padding: 10px; "
            "border: 1px solid #2196F3; border-radius: 5px; margin: 10px;"
        )
        layout.addWidget(theory_label)
        
        # 实验组1: 偏移量 = 14.4px
        group1_layout = QVBoxLayout()
        group1_title = QLabel("🔬 实验组1: 目标偏移量 = 14.4像素")
        group1_title.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px;")
        group1_layout.addWidget(group1_title)
        
        group1_widgets = QHBoxLayout()
        
        # 组合1: 0.4 × 120 × 0.3 = 14.4
        widget1_1 = EquivalentCurveWidget(
            0.4, 0.3, 0.5,
            "组合A", "强度:0.4 比例:0.3"
        )
        
        # 组合2: 0.6 × 120 × 0.2 = 14.4
        widget1_2 = EquivalentCurveWidget(
            0.6, 0.2, 0.5,
            "组合B", "强度:0.6 比例:0.2"
        )
        
        # 组合3: 0.24 × 120 × 0.5 = 14.4
        widget1_3 = EquivalentCurveWidget(
            0.24, 0.5, 0.5,
            "组合C", "强度:0.24 比例:0.5"
        )
        
        # 组合4: 0.8 × 120 × 0.15 = 14.4
        widget1_4 = EquivalentCurveWidget(
            0.8, 0.15, 0.5,
            "组合D", "强度:0.8 比例:0.15"
        )
        
        group1_widgets.addWidget(widget1_1)
        group1_widgets.addWidget(widget1_2)
        group1_widgets.addWidget(widget1_3)
        group1_widgets.addWidget(widget1_4)
        
        group1_layout.addLayout(group1_widgets)
        layout.addLayout(group1_layout)
        
        # 实验组2: 偏移量 = 28.8px
        group2_layout = QVBoxLayout()
        group2_title = QLabel("🔬 实验组2: 目标偏移量 = 28.8像素")
        group2_title.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px;")
        group2_layout.addWidget(group2_title)
        
        group2_widgets = QHBoxLayout()
        
        # 组合1: 0.8 × 120 × 0.3 = 28.8
        widget2_1 = EquivalentCurveWidget(
            0.8, 0.3, 0.5,
            "组合A", "强度:0.8 比例:0.3"
        )
        
        # 组合2: 0.6 × 120 × 0.4 = 28.8
        widget2_2 = EquivalentCurveWidget(
            0.6, 0.4, 0.5,
            "组合B", "强度:0.6 比例:0.4"
        )
        
        # 组合3: 0.48 × 120 × 0.5 = 28.8
        widget2_3 = EquivalentCurveWidget(
            0.48, 0.5, 0.5,
            "组合C", "强度:0.48 比例:0.5"
        )
        
        # 组合4: 1.2 × 120 × 0.2 = 28.8
        widget2_4 = EquivalentCurveWidget(
            1.2, 0.2, 0.5,
            "组合D", "强度:1.2 比例:0.2"
        )
        
        group2_widgets.addWidget(widget2_1)
        group2_widgets.addWidget(widget2_2)
        group2_widgets.addWidget(widget2_3)
        group2_widgets.addWidget(widget2_4)
        
        group2_layout.addLayout(group2_widgets)
        layout.addLayout(group2_layout)
        
        # 对照组: 不同偏移量
        control_layout = QVBoxLayout()
        control_title = QLabel("🎯 对照组: 不同偏移量对比")
        control_title.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px;")
        control_layout.addWidget(control_title)
        
        control_widgets = QHBoxLayout()
        
        # 偏移量7.2px
        widget3_1 = EquivalentCurveWidget(
            0.2, 0.3, 0.5,
            "小偏移", "偏移:7.2px"
        )
        
        # 偏移量14.4px
        widget3_2 = EquivalentCurveWidget(
            0.4, 0.3, 0.5,
            "中偏移", "偏移:14.4px"
        )
        
        # 偏移量28.8px
        widget3_3 = EquivalentCurveWidget(
            0.8, 0.3, 0.5,
            "大偏移", "偏移:28.8px"
        )
        
        # 偏移量43.2px
        widget3_4 = EquivalentCurveWidget(
            1.2, 0.3, 0.5,
            "超大偏移", "偏移:43.2px"
        )
        
        control_widgets.addWidget(widget3_1)
        control_widgets.addWidget(widget3_2)
        control_widgets.addWidget(widget3_3)
        control_widgets.addWidget(widget3_4)
        
        control_layout.addLayout(control_widgets)
        layout.addLayout(control_layout)
        
        # 结论说明
        conclusion_label = QLabel(
            "📊 实验结论:\n"
            "✅ 实验组1: 四种不同参数组合，相同偏移量(14.4px) → 曲线形态完全一致\n"
            "✅ 实验组2: 四种不同参数组合，相同偏移量(28.8px) → 曲线形态完全一致\n"
            "✅ 对照组: 不同偏移量 → 明显不同的弯曲程度\n\n"
            "💡 验证结果: 您的理解完全正确！\n"
            "在位置比例固定的情况下，只要偏移量相同，无论弯曲强度和控制点比例如何组合，最终形态都完全一样！"
        )
        conclusion_label.setStyleSheet(
            "margin: 15px; padding: 15px; "
            "background-color: #E8F5E8; border: 1px solid #4CAF50; "
            "border-radius: 8px; font-size: 12px;"
        )
        layout.addWidget(conclusion_label)


def main():
    """应用程序入口点"""
    app = QApplication(sys.argv)
    
    # 创建等效偏移量演示窗口
    window = EquivalentOffsetWindow()
    window.show()
    
    # 运行应用程序
    sys.exit(app.exec())


if __name__ == "__main__":
    main()