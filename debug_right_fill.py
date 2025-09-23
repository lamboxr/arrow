#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
调试版本 - 明确显示只填充右侧弓形区域
"""

import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget
from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QPainter, QLinearGradient, QPen, QColor, QPainterPath


# 渐变颜色定义
GRADIENT_COLORS = {
    'top': '#B6B384',      # 顶部颜色
    'middle': '#FEFFAF',   # 中间颜色
    'bottom': '#B7B286',   # 底部颜色
    'outline': '#B7B286'   # 轮廓颜色
}


class DebugRightFillWidget(QWidget):
    """调试右侧填充Widget"""
    
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
        self.line_width = 3
        
        # 设置窗口
        self.setFixedSize(800, 600)
        self.setStyleSheet("background-color: #F0F0F0;")
    
    def create_trapezoid_geometry(self):
        """创建梯形几何"""
        center_x = self.width() / 2
        start_y = (self.height() - self.trapezoid_height) / 2
        
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
    
    def create_straight_line_path(self, start_point, end_point):
        """创建直线路径"""
        path = QPainterPath()
        path.moveTo(start_point)
        path.lineTo(end_point)
        return path
    
    def create_right_bow_only_path(self, geometry):
        """
        创建ONLY右侧弓形区域填充路径
        明确只填充右腰线贝塞尔曲线与直线之间的区域
        """
        path = QPainterPath()
        
        # 从上右顶点开始
        path.moveTo(geometry['top_right'])
        
        # 1. 沿贝塞尔曲线到下右
        right_base_x = geometry['top_right'].x() + (geometry['bottom_right'].x() - geometry['top_right'].x()) * self.position_ratio
        right_base_y = geometry['top_right'].y() + (geometry['bottom_right'].y() - geometry['top_right'].y()) * self.position_ratio
        right_control_point = QPointF(right_base_x + self.curve_offset, right_base_y)
        path.quadTo(right_control_point, geometry['bottom_right'])
        
        # 2. 沿直线返回上右
        path.lineTo(geometry['top_right'])
        
        # 闭合路径
        path.closeSubpath()
        
        return path, right_control_point
    
    def create_line_gradient(self, start_point, end_point):
        """创建腰线渐变"""
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
    
    def paintEvent(self, event):
        """绘制调试版本 - 只填充右侧弓形"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        
        try:
            # 背景
            painter.fillRect(self.rect(), QColor("#F0F0F0"))
            
            # 创建几何
            geometry = self.create_trapezoid_geometry()
            
            # 1. 绘制右侧弓形填充（红色，明显标识）
            right_bow_path, right_control = self.create_right_bow_only_path(geometry)
            painter.setBrush(QColor("#FF6B6B"))  # 红色填充，明显标识
            painter.setPen(QPen(QColor("#FF0000"), 2))  # 红色边框
            painter.drawPath(right_bow_path)
            
            # 2. 绘制左腰线贝塞尔曲线（只是线条，不填充）
            left_path, left_control = self.create_bezier_curve(
                geometry['top_left'], 
                geometry['bottom_left']
            )
            left_gradient = self.create_line_gradient(
                geometry['top_left'], 
                geometry['bottom_left']
            )
            
            left_pen = QPen()
            left_pen.setBrush(left_gradient)
            left_pen.setWidth(self.line_width)
            left_pen.setCapStyle(Qt.RoundCap)
            painter.setPen(left_pen)
            painter.drawPath(left_path)
            
            # 3. 绘制右腰线贝塞尔曲线（只是线条，在填充之上）
            right_path, _ = self.create_bezier_curve(
                geometry['top_right'], 
                geometry['bottom_right']
            )
            right_gradient = self.create_line_gradient(
                geometry['top_right'], 
                geometry['bottom_right']
            )
            
            right_pen = QPen()
            right_pen.setBrush(right_gradient)
            right_pen.setWidth(self.line_width)
            right_pen.setCapStyle(Qt.RoundCap)
            painter.setPen(right_pen)
            painter.drawPath(right_path)
            
            # 4. 绘制直线腰线（虚线，对比）
            painter.setPen(QPen(QColor("#666666"), 1, Qt.DashLine))
            
            # 左腰直线
            left_straight = self.create_straight_line_path(
                geometry['top_left'], 
                geometry['bottom_left']
            )
            painter.drawPath(left_straight)
            
            # 右腰直线
            right_straight = self.create_straight_line_path(
                geometry['top_right'], 
                geometry['bottom_right']
            )
            painter.drawPath(right_straight)
            
            # 5. 标记关键点
            painter.setPen(QPen(QColor("#0000FF"), 2))
            painter.setBrush(QColor("#0000FF"))
            # 梯形顶点
            painter.drawEllipse(geometry['top_left'], 4, 4)
            painter.drawEllipse(geometry['top_right'], 4, 4)
            painter.drawEllipse(geometry['bottom_left'], 4, 4)
            painter.drawEllipse(geometry['bottom_right'], 4, 4)
            
            # 控制点
            painter.setPen(QPen(QColor("#00FF00"), 2))
            painter.setBrush(QColor("#00FF00"))
            painter.drawEllipse(left_control, 6, 6)
            painter.drawEllipse(right_control, 6, 6)
            
            # 6. 说明文字
            painter.setPen(QColor("#333333"))
            painter.drawText(20, 30, "调试版本 - 只填充右侧弓形区域")
            painter.drawText(20, 50, "=" * 45)
            
            painter.drawText(20, 80, "🔴 红色区域: 右侧弓形填充")
            painter.drawText(20, 100, "━━━ 实线: 贝塞尔曲线（带渐变）")
            painter.drawText(20, 120, "--- 虚线: 直线腰线（对比）")
            painter.drawText(20, 140, "🔵 蓝点: 梯形顶点")
            painter.drawText(20, 160, "🟢 绿点: 贝塞尔控制点")
            
            painter.drawText(20, 190, f"参数: 上底偏移{self.top_offset}px, 控制点{self.position_ratio}, 弯曲{self.curve_offset}px")
            
            painter.drawText(20, 220, "验证: 左侧应该没有填充，只有右侧有红色填充")
            
        except Exception as e:
            print(f"绘图错误: {e}")
        finally:
            painter.end()


class DebugRightFillWindow(QMainWindow):
    """调试右侧填充主窗口"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("调试版本 - 只填充右侧弓形区域")
        self.setGeometry(100, 100, 850, 650)
        
        self.widget = DebugRightFillWidget()
        self.setCentralWidget(self.widget)


def main():
    """应用程序入口点"""
    app = QApplication(sys.argv)
    
    window = DebugRightFillWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()