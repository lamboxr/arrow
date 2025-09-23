#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
弯曲效果对照组对比程序
每组两个示例，只改变单一参数，清晰展示参数影响
"""

import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                               QHBoxLayout, QLabel, QFrame)
from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QPainter, QLinearGradient, QPen, QColor, QPainterPath


# 颜色定义
COLORS = {
    'top': '#B6B384',      # 顶部颜色
    'middle': '#FEFFAF',   # 中间颜色
    'bottom': '#B7B286',   # 底部颜色
    'outline': '#B7B286'   # 轮廓颜色
}

# 基础尺寸参数
BASE_DIMENSIONS = {
    'height': 120,         # 进一步缩小以适应对照组布局
    'top_base': 12,
    'bottom_base': 200,
    'outline_width': 3,
    'left_offset': 80
}


class CurveWidget(QWidget):
    """单个弯曲梯形显示Widget"""
    
    def __init__(self, curve_intensity, control_point_ratio, title="", subtitle="", parent=None):
        super().__init__(parent)
        self.curve_intensity = curve_intensity
        self.control_point_ratio = control_point_ratio
        self.title = title
        self.subtitle = subtitle
        
        # 设置固定尺寸
        self.setFixedSize(250, 180)
        self.setStyleSheet("background-color: #FFFFFF; border: 2px solid #333333; margin: 2px;")
    
    def _create_trapezoid_geometry(self):
        """创建弯曲梯形的关键点坐标"""
        widget_width = self.width()
        widget_height = self.height()
        
        # 计算梯形在Widget中的居中位置
        center_x = widget_width / 2
        start_y = (widget_height - BASE_DIMENSIONS['height']) / 2 + 20  # 留出标题空间
        
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
        """创建贝塞尔曲线路径"""
        path = QPainterPath()
        path.moveTo(start_point)
        
        # 计算控制点位置
        mid_x = (start_point.x() + end_point.x()) / 2
        mid_y = (start_point.y() + end_point.y()) / 2
        
        # 计算向右的偏移量
        offset_x = self.curve_intensity * BASE_DIMENSIONS['height'] * self.control_point_ratio
        
        # 控制点位置
        control_point = QPointF(mid_x + offset_x, mid_y)
        
        # 创建二次贝塞尔曲线
        path.quadTo(control_point, end_point)
        
        return path
    
    def _create_line_gradient(self, start_point, end_point):
        """创建渐变（增强可见度）"""
        gradient = QLinearGradient(start_point, end_point)
        
        # 设置渐变颜色点（增加透明度以提高可见度）
        top_color = QColor(COLORS['top'])
        top_color.setAlpha(120)
        gradient.setColorAt(0.0, top_color)
        
        middle_color = QColor(COLORS['middle'])
        middle_color.setAlpha(220)
        gradient.setColorAt(0.5, middle_color)
        
        bottom_color = QColor(COLORS['bottom'])
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
            left_pen.setWidth(BASE_DIMENSIONS['outline_width'])
            left_pen.setCapStyle(Qt.RoundCap)
            painter.setPen(left_pen)
            painter.drawPath(left_path)
            
            # 绘制右腰线
            right_path = self._create_curved_path(geometry['top_right'], geometry['bottom_right'])
            right_gradient = self._create_line_gradient(geometry['top_right'], geometry['bottom_right'])
            right_pen = QPen()
            right_pen.setBrush(right_gradient)
            right_pen.setWidth(BASE_DIMENSIONS['outline_width'])
            right_pen.setCapStyle(Qt.RoundCap)
            painter.setPen(right_pen)
            painter.drawPath(right_path)
            
            # 绘制标题和参数信息
            painter.setPen(QColor("#333333"))
            painter.drawText(5, 15, self.title)
            painter.drawText(5, 30, self.subtitle)
            
            # 计算偏移量
            offset = self.curve_intensity * BASE_DIMENSIONS['height'] * self.control_point_ratio
            painter.drawText(5, 170, f"偏移:{offset:.1f}px")
            
        except Exception as e:
            print(f"绘图错误: {e}")
        finally:
            painter.end()


class ComparisonGroup(QWidget):
    """对照组Widget"""
    
    def __init__(self, group_title, config1, config2, parent=None):
        super().__init__(parent)
        self.setStyleSheet("margin: 5px;")
        
        # 创建布局
        layout = QVBoxLayout(self)
        
        # 添加组标题
        title_label = QLabel(group_title)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet(
            "font-size: 14px; font-weight: bold; "
            "background-color: #E8E8E8; padding: 5px; "
            "border: 1px solid #CCCCCC; margin-bottom: 5px;"
        )
        layout.addWidget(title_label)
        
        # 创建水平布局放置两个对比Widget
        h_layout = QHBoxLayout()
        
        # 创建两个对比Widget
        widget1 = CurveWidget(
            config1['intensity'], 
            config1['ratio'], 
            config1['title'],
            config1['subtitle']
        )
        widget2 = CurveWidget(
            config2['intensity'], 
            config2['ratio'], 
            config2['title'],
            config2['subtitle']
        )
        
        h_layout.addWidget(widget1)
        h_layout.addWidget(widget2)
        
        layout.addLayout(h_layout)


class ControlledComparisonWindow(QMainWindow):
    """对照组对比窗口"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("弯曲参数对照组对比 - 单参数影响分析")
        self.setGeometry(100, 100, 1200, 900)
        
        # 创建中心Widget和布局
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # 添加主标题
        main_title = QLabel("弯曲梯形参数对照组对比")
        main_title.setAlignment(Qt.AlignCenter)
        main_title.setStyleSheet("font-size: 20px; font-weight: bold; margin: 15px;")
        layout.addWidget(main_title)
        
        # 创建水平布局放置对照组
        groups_layout = QHBoxLayout()
        
        # 对照组1: 弯曲强度对比（控制点比例固定为0.3）
        group1 = ComparisonGroup(
            "对照组1: 弯曲强度影响\n(控制点比例固定0.3)",
            {
                'intensity': 0.2, 'ratio': 0.3,
                'title': '弱弯曲强度', 'subtitle': '强度:0.2 比例:0.3'
            },
            {
                'intensity': 0.6, 'ratio': 0.3,
                'title': '强弯曲强度', 'subtitle': '强度:0.6 比例:0.3'
            }
        )
        
        # 对照组2: 控制点比例对比（弯曲强度固定为0.4）
        group2 = ComparisonGroup(
            "对照组2: 控制点比例影响\n(弯曲强度固定0.4)",
            {
                'intensity': 0.4, 'ratio': 0.2,
                'title': '小控制点比例', 'subtitle': '强度:0.4 比例:0.2'
            },
            {
                'intensity': 0.4, 'ratio': 0.5,
                'title': '大控制点比例', 'subtitle': '强度:0.4 比例:0.5'
            }
        )
        
        groups_layout.addWidget(group1)
        groups_layout.addWidget(group2)
        layout.addLayout(groups_layout)
        
        # 第二行对照组
        groups_layout2 = QHBoxLayout()
        
        # 对照组3: 极端对比（从最小到最大）
        group3 = ComparisonGroup(
            "对照组3: 极端效果对比\n(最小 vs 最大)",
            {
                'intensity': 0.1, 'ratio': 0.1,
                'title': '最小弯曲', 'subtitle': '强度:0.1 比例:0.1'
            },
            {
                'intensity': 1.0, 'ratio': 0.5,
                'title': '最大弯曲', 'subtitle': '强度:1.0 比例:0.5'
            }
        )
        
        # 对照组4: 等效果对比（不同参数组合产生相似效果）
        group4 = ComparisonGroup(
            "对照组4: 等效果对比\n(不同参数相似效果)",
            {
                'intensity': 0.5, 'ratio': 0.3,
                'title': '高强度低比例', 'subtitle': '强度:0.5 比例:0.3'
            },
            {
                'intensity': 0.3, 'ratio': 0.5,
                'title': '低强度高比例', 'subtitle': '强度:0.3 比例:0.5'
            }
        )
        
        groups_layout2.addWidget(group3)
        groups_layout2.addWidget(group4)
        layout.addLayout(groups_layout2)
        
        # 添加说明文字
        info_label = QLabel(
            "📊 对照组分析说明:\n"
            "• 对照组1: 展示弯曲强度的影响（比例固定）\n"
            "• 对照组2: 展示控制点比例的影响（强度固定）\n"
            "• 对照组3: 展示参数的极端效果差异\n"
            "• 对照组4: 展示不同参数组合可产生相似效果\n\n"
            "💡 观察要点: 注意每组中两个梯形的弯曲程度差异"
        )
        info_label.setStyleSheet(
            "margin: 15px; padding: 15px; "
            "background-color: #F5F5F5; border: 1px solid #DDDDDD; "
            "border-radius: 8px; font-size: 12px;"
        )
        layout.addWidget(info_label)


def main():
    """应用程序入口点"""
    app = QApplication(sys.argv)
    
    # 创建对照组对比窗口
    window = ControlledComparisonWindow()
    window.show()
    
    # 运行应用程序
    sys.exit(app.exec())


if __name__ == "__main__":
    main()