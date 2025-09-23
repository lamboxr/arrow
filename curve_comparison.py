#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
弯曲效果对比程序
在一个窗口中显示多种弯曲参数的视觉效果
"""

import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QLabel
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
    'height': 150,         # 缩小尺寸以便在一个窗口显示多个
    'top_base': 15,
    'bottom_base': 250,
    'outline_width': 3,    # 增加线宽以提高可见度
    'left_offset': 100     # 缩小偏移量
}


class CurveWidget(QWidget):
    """单个弯曲梯形显示Widget"""
    
    def __init__(self, curve_intensity, control_point_ratio, title="", parent=None):
        super().__init__(parent)
        self.curve_intensity = curve_intensity
        self.control_point_ratio = control_point_ratio
        self.title = title
        
        # 设置固定尺寸
        self.setFixedSize(300, 200)
        self.setStyleSheet("background-color: #FFFFFF; border: 2px solid #333333;")
    
    def _create_trapezoid_geometry(self):
        """创建弯曲梯形的关键点坐标"""
        widget_width = self.width()
        widget_height = self.height()
        
        # 计算梯形在Widget中的居中位置
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
        top_color.setAlpha(100)  # 从完全透明改为部分可见
        gradient.setColorAt(0.0, top_color)
        
        middle_color = QColor(COLORS['middle'])
        middle_color.setAlpha(200)  # 增加中间颜色的不透明度
        gradient.setColorAt(0.5, middle_color)
        
        bottom_color = QColor(COLORS['bottom'])
        bottom_color.setAlpha(100)  # 从完全透明改为部分可见
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
            painter.drawText(10, 20, self.title)
            
            # 计算偏移量
            offset = self.curve_intensity * BASE_DIMENSIONS['height'] * self.control_point_ratio
            info_text = f"强度:{self.curve_intensity} 比例:{self.control_point_ratio}"
            painter.drawText(10, 35, info_text)
            painter.drawText(10, 50, f"偏移:{offset:.1f}px")
            
        except Exception as e:
            print(f"绘图错误: {e}")
        finally:
            painter.end()


class ComparisonWindow(QMainWindow):
    """对比窗口"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("弯曲效果对比 - 不同参数的视觉效果")
        self.setGeometry(100, 100, 1000, 800)
        
        # 创建中心Widget和布局
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QGridLayout(central_widget)
        
        # 添加标题
        title_label = QLabel("弯曲梯形参数效果对比")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; margin: 10px;")
        layout.addWidget(title_label, 0, 0, 1, 3)
        
        # 定义不同的参数组合
        curve_configs = [
            (0.1, 0.1, "极轻微弯曲"),
            (0.2, 0.2, "轻微弯曲"),
            (0.3, 0.3, "中等弯曲(当前)"),
            (0.5, 0.3, "增强弯曲强度"),
            (0.3, 0.5, "增强控制点比例"),
            (0.5, 0.5, "强烈弯曲"),
            (0.8, 0.4, "很强弯曲"),
            (1.0, 0.5, "极端弯曲"),
            (0.0, 0.0, "无弯曲(直线)")
        ]
        
        # 创建对比Widget
        row = 1
        col = 0
        for intensity, ratio, title in curve_configs:
            widget = CurveWidget(intensity, ratio, title)
            layout.addWidget(widget, row, col)
            
            col += 1
            if col >= 3:  # 每行3个
                col = 0
                row += 1
        
        # 添加说明文字
        info_label = QLabel(
            "参数说明:\n"
            "• 弯曲强度: 控制整体弯曲程度 (0.0-1.0)\n"
            "• 控制点比例: 微调弯曲效果 (0.0-0.5)\n"
            "• 偏移量 = 弯曲强度 × 梯形高度 × 控制点比例\n"
            "• 偏移量越大，向右凸起越明显"
        )
        info_label.setStyleSheet("margin: 10px; padding: 10px; background-color: #f0f0f0; border-radius: 5px;")
        layout.addWidget(info_label, row + 1, 0, 1, 3)


def main():
    """应用程序入口点"""
    app = QApplication(sys.argv)
    
    # 创建对比窗口
    window = ComparisonWindow()
    window.show()
    
    # 运行应用程序
    sys.exit(app.exec())


if __name__ == "__main__":
    main()