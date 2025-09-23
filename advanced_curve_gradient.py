#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
高级曲线渐变实现
演示多种适配贝塞尔曲线路径的渐变技术
"""

import sys
import math
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget
from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QPainter, QLinearGradient, QRadialGradient, QPen, QColor, QPainterPath


# 渐变颜色定义
GRADIENT_COLORS = {
    'top': '#B6B384',      # 顶部颜色
    'middle': '#FEFFAF',   # 中间颜色
    'bottom': '#B7B286',   # 底部颜色
    'outline': '#B7B286'   # 轮廓颜色
}


class AdvancedCurveGradientWidget(QWidget):
    """高级曲线渐变Widget - 演示多种渐变技术"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # 核心参数
        self.top_offset = -200
        self.position_ratio = 0.5
        self.curve_offset = 200
        
        # 显示参数
        self.trapezoid_height = 300
        self.trapezoid_top_width = 30
        self.trapezoid_bottom_width = 500
        self.line_width = 4
        
        # 设置窗口
        self.setFixedSize(900, 700)
        self.setStyleSheet("background-color: #F0F0F0;")
    
    def create_trapezoid_geometry(self):
        """创建梯形几何"""
        center_x = self.width() / 2
        start_y = 100  # 从顶部留出更多空间
        
        top_center_x = center_x + self.top_offset
        
        top_left_x = top_center_x - self.trapezoid_top_width / 2
        top_right_x = top_center_x + self.trapezoid_top_width / 2
        top_y = start_y
        
        bottom_left_x = center_x - self.trapezoid_bottom_width / 2
        bottom_right_x = center_x + self.trapezoid_bottom_width / 2
        bottom_y = start_y + self.trapezoid_height
        
        return {
            'top_left': QPointF(top_left_x, top_y),
            'top_right': QPointF(top_right_x, top_y),
            'bottom_left': QPointF(bottom_left_x, bottom_y),
            'bottom_right': QPointF(bottom_right_x, bottom_y)
        }
    
    def create_bezier_curve(self, start_point, end_point):
        """创建贝塞尔曲线"""
        path = QPainterPath()
        path.moveTo(start_point)
        
        base_x = start_point.x() + (end_point.x() - start_point.x()) * self.position_ratio
        base_y = start_point.y() + (end_point.y() - start_point.y()) * self.position_ratio
        control_point = QPointF(base_x + self.curve_offset, base_y)
        
        path.quadTo(control_point, end_point)
        
        return path, control_point
    
    def create_linear_gradient(self, start_point, end_point):
        """方法1: 标准线性渐变"""
        gradient = QLinearGradient(start_point, end_point)
        
        top_color = QColor(GRADIENT_COLORS['top'])
        top_color.setAlpha(0)
        gradient.setColorAt(0.0, top_color)
        
        middle_color = QColor(GRADIENT_COLORS['middle'])
        middle_color.setAlpha(127)
        gradient.setColorAt(0.5, middle_color)
        
        bottom_color = QColor(GRADIENT_COLORS['bottom'])
        bottom_color.setAlpha(0)
        gradient.setColorAt(1.0, bottom_color)
        
        return gradient
    
    def create_curve_adapted_linear_gradient(self, start_point, end_point, control_point):
        """方法2: 曲线适配线性渐变 - 考虑控制点影响"""
        # 计算曲线的"重心"方向
        curve_center_x = (start_point.x() + 2 * control_point.x() + end_point.x()) / 4
        curve_center_y = (start_point.y() + 2 * control_point.y() + end_point.y()) / 4
        
        # 使用曲线重心调整渐变方向
        adjusted_end_x = end_point.x() + (curve_center_x - (start_point.x() + end_point.x()) / 2) * 0.3
        adjusted_end_y = end_point.y() + (curve_center_y - (start_point.y() + end_point.y()) / 2) * 0.3
        adjusted_end = QPointF(adjusted_end_x, adjusted_end_y)
        
        gradient = QLinearGradient(start_point, adjusted_end)
        
        top_color = QColor(GRADIENT_COLORS['top'])
        top_color.setAlpha(0)
        gradient.setColorAt(0.0, top_color)
        
        middle_color = QColor(GRADIENT_COLORS['middle'])
        middle_color.setAlpha(127)
        gradient.setColorAt(0.5, middle_color)
        
        bottom_color = QColor(GRADIENT_COLORS['bottom'])
        bottom_color.setAlpha(0)
        gradient.setColorAt(1.0, bottom_color)
        
        return gradient
    
    def create_radial_gradient(self, start_point, end_point, control_point):
        """方法3: 径向渐变 - 以控制点为中心"""
        # 使用控制点作为径向渐变的中心
        center = control_point
        
        # 计算半径 - 从控制点到起点和终点的最大距离
        radius1 = math.sqrt((center.x() - start_point.x())**2 + (center.y() - start_point.y())**2)
        radius2 = math.sqrt((center.x() - end_point.x())**2 + (center.y() - end_point.y())**2)
        radius = max(radius1, radius2) * 1.2
        
        gradient = QRadialGradient(center, radius)
        
        # 中心最亮
        center_color = QColor(GRADIENT_COLORS['middle'])
        center_color.setAlpha(180)
        gradient.setColorAt(0.0, center_color)
        
        # 中间过渡
        mid_color = QColor(GRADIENT_COLORS['middle'])
        mid_color.setAlpha(100)
        gradient.setColorAt(0.6, mid_color)
        
        # 边缘透明
        edge_color = QColor(GRADIENT_COLORS['bottom'])
        edge_color.setAlpha(0)
        gradient.setColorAt(1.0, edge_color)
        
        return gradient
    
    def create_multi_point_gradient(self, start_point, end_point, control_point):
        """方法4: 多点线性渐变 - 沿曲线采样多个点"""
        # 在贝塞尔曲线上采样多个点来创建更精确的渐变
        # 这里简化为使用曲线中点
        t = 0.5  # 曲线参数
        curve_mid_x = (1-t)**2 * start_point.x() + 2*(1-t)*t * control_point.x() + t**2 * end_point.x()
        curve_mid_y = (1-t)**2 * start_point.y() + 2*(1-t)*t * control_point.y() + t**2 * end_point.y()
        curve_mid = QPointF(curve_mid_x, curve_mid_y)
        
        # 创建从起点到曲线中点的渐变方向
        gradient = QLinearGradient(start_point, curve_mid)
        gradient.setSpread(QLinearGradient.ReflectSpread)  # 反射扩展
        
        top_color = QColor(GRADIENT_COLORS['top'])
        top_color.setAlpha(0)
        gradient.setColorAt(0.0, top_color)
        
        middle_color = QColor(GRADIENT_COLORS['middle'])
        middle_color.setAlpha(150)
        gradient.setColorAt(0.5, middle_color)
        
        bottom_color = QColor(GRADIENT_COLORS['bottom'])
        bottom_color.setAlpha(0)
        gradient.setColorAt(1.0, bottom_color)
        
        return gradient
    
    def draw_curve_with_gradient(self, painter, start_point, end_point, gradient_method, y_offset, label):
        """绘制带指定渐变方法的曲线"""
        # 创建贝塞尔曲线
        path, control_point = self.create_bezier_curve(
            QPointF(start_point.x(), start_point.y() + y_offset),
            QPointF(end_point.x(), end_point.y() + y_offset)
        )
        
        # 根据方法创建渐变
        if gradient_method == "linear":
            gradient = self.create_linear_gradient(
                QPointF(start_point.x(), start_point.y() + y_offset),
                QPointF(end_point.x(), end_point.y() + y_offset)
            )
        elif gradient_method == "curve_adapted":
            gradient = self.create_curve_adapted_linear_gradient(
                QPointF(start_point.x(), start_point.y() + y_offset),
                QPointF(end_point.x(), end_point.y() + y_offset),
                control_point
            )
        elif gradient_method == "radial":
            gradient = self.create_radial_gradient(
                QPointF(start_point.x(), start_point.y() + y_offset),
                QPointF(end_point.x(), end_point.y() + y_offset),
                control_point
            )
        elif gradient_method == "multi_point":
            gradient = self.create_multi_point_gradient(
                QPointF(start_point.x(), start_point.y() + y_offset),
                QPointF(end_point.x(), end_point.y() + y_offset),
                control_point
            )
        
        # 绘制曲线
        pen = QPen()
        pen.setBrush(gradient)
        pen.setWidth(self.line_width)
        pen.setCapStyle(Qt.RoundCap)
        painter.setPen(pen)
        painter.drawPath(path)
        
        # 绘制标签
        painter.setPen(QColor("#333333"))
        painter.drawText(20, start_point.y() + y_offset - 10, label)
        
        return control_point
    
    def paintEvent(self, event):
        """绘制高级曲线渐变演示"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        
        try:
            # 背景
            painter.fillRect(self.rect(), QColor("#F0F0F0"))
            
            # 标题
            painter.setPen(QColor("#333333"))
            painter.drawText(20, 30, "高级曲线渐变技术演示")
            painter.drawText(20, 50, "=" * 50)
            
            # 创建基础几何
            geometry = self.create_trapezoid_geometry()
            
            # 演示不同的渐变方法
            methods = [
                ("linear", "方法1: 标准线性渐变"),
                ("curve_adapted", "方法2: 曲线适配线性渐变"),
                ("radial", "方法3: 径向渐变 (以控制点为中心)"),
                ("multi_point", "方法4: 多点线性渐变")
            ]
            
            y_spacing = 80
            for i, (method, label) in enumerate(methods):
                y_offset = i * y_spacing
                
                # 绘制左腰线
                left_control = self.draw_curve_with_gradient(
                    painter,
                    geometry['top_left'],
                    geometry['bottom_left'],
                    method,
                    y_offset,
                    f"{label} (左腰线)"
                )
                
                # 绘制右腰线
                right_control = self.draw_curve_with_gradient(
                    painter,
                    geometry['top_right'],
                    geometry['bottom_right'],
                    method,
                    y_offset,
                    f"{label} (右腰线)"
                )
                
                # 标记控制点
                painter.setPen(QPen(QColor("#FF0000"), 2))
                painter.setBrush(QColor("#FF0000"))
                painter.drawEllipse(left_control, 3, 3)
                painter.drawEllipse(right_control, 3, 3)
            
            # 参数信息
            painter.setPen(QColor("#666666"))
            painter.drawText(500, 100, f"核心参数:")
            painter.drawText(500, 120, f"• 上底平移: {self.top_offset:+.0f}px")
            painter.drawText(500, 140, f"• 控制点位置: {self.position_ratio:.2f}")
            painter.drawText(500, 160, f"• 横向偏移: {self.curve_offset:+.0f}px")
            
            painter.drawText(500, 200, "渐变颜色:")
            painter.drawText(500, 220, f"• 顶部: {GRADIENT_COLORS['top']} (透明)")
            painter.drawText(500, 240, f"• 中间: {GRADIENT_COLORS['middle']} (半透明)")
            painter.drawText(500, 260, f"• 底部: {GRADIENT_COLORS['bottom']} (透明)")
            
        except Exception as e:
            print(f"绘图错误: {e}")
        finally:
            painter.end()


class AdvancedCurveGradientWindow(QMainWindow):
    """高级曲线渐变主窗口"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("高级曲线渐变技术演示")
        self.setGeometry(100, 100, 950, 750)
        
        self.widget = AdvancedCurveGradientWidget()
        self.setCentralWidget(self.widget)


def main():
    """应用程序入口点"""
    app = QApplication(sys.argv)
    
    window = AdvancedCurveGradientWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()