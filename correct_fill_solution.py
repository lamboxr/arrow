#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
正确的填充解决方案
明确展示：只填充直线梯形区域，不填充弓形区域
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


class CorrectFillWidget(QWidget):
    """正确填充演示Widget"""
    
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
        self.setFixedSize(800, 600)
        self.setStyleSheet("background-color: #F5F5F5;")
    
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
    
    def create_correct_fill_path(self, geometry):
        """正确的填充路径 - 只填充直线梯形，排除弓形区域"""
        path = QPainterPath()
        
        # 从上底左端点开始
        path.moveTo(geometry['top_left'])
        
        # 1. 上底 (直线)
        path.lineTo(geometry['top_right'])
        
        # 2. 右腰线 (直线，不是贝塞尔曲线)
        path.lineTo(geometry['bottom_right'])
        
        # 3. 下底 (直线)
        path.lineTo(geometry['bottom_left'])
        
        # 4. 左腰线 (直线，不是贝塞尔曲线)
        path.lineTo(geometry['top_left'])
        
        # 闭合路径
        path.closeSubpath()
        
        return path
    
    def create_wrong_fill_path(self, geometry):
        """错误的填充路径 - 使用贝塞尔曲线作为边界（包含弓形）"""
        path = QPainterPath()
        
        # 从上底左端点开始
        path.moveTo(geometry['top_left'])
        
        # 1. 上底 (直线)
        path.lineTo(geometry['top_right'])
        
        # 2. 右腰线 (贝塞尔曲线)
        right_base_x = geometry['top_right'].x() + (geometry['bottom_right'].x() - geometry['top_right'].x()) * self.position_ratio
        right_base_y = geometry['top_right'].y() + (geometry['bottom_right'].y() - geometry['top_right'].y()) * self.position_ratio
        right_control = QPointF(right_base_x + self.curve_offset, right_base_y)
        path.quadTo(right_control, geometry['bottom_right'])
        
        # 3. 下底 (直线)
        path.lineTo(geometry['bottom_left'])
        
        # 4. 左腰线 (贝塞尔曲线)
        left_base_x = geometry['top_left'].x() + (geometry['bottom_left'].x() - geometry['top_left'].x()) * self.position_ratio
        left_base_y = geometry['top_left'].y() + (geometry['bottom_left'].y() - geometry['top_left'].y()) * self.position_ratio
        left_control = QPointF(left_base_x + self.curve_offset, left_base_y)
        path.quadTo(left_control, geometry['top_left'])
        
        # 闭合路径
        path.closeSubpath()
        
        return path
    
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
    
    def draw_curved_lines(self, painter, geometry):
        """绘制弯曲的腰线"""
        # 左腰线（弯曲）
        left_path, left_control = self.create_bezier_curve(
            geometry['top_left'], 
            geometry['bottom_left']
        )
        left_gradient = self.create_line_gradient(
            geometry['top_left'], 
            geometry['bottom_left']
        )
        
        pen = QPen()
        pen.setBrush(left_gradient)
        pen.setWidth(self.line_width)
        pen.setCapStyle(Qt.RoundCap)
        painter.setPen(pen)
        painter.drawPath(left_path)
        
        # 右腰线（弯曲）
        right_path, right_control = self.create_bezier_curve(
            geometry['top_right'], 
            geometry['bottom_right']
        )
        right_gradient = self.create_line_gradient(
            geometry['top_right'], 
            geometry['bottom_right']
        )
        
        pen.setBrush(right_gradient)
        painter.setPen(pen)
        painter.drawPath(right_path)
        
        return left_control, right_control
    
    def draw_straight_lines(self, painter, geometry, color, width=2, style=Qt.DashLine):
        """绘制直线腰线（用于对比）"""
        pen = QPen(QColor(color), width, style)
        painter.setPen(pen)
        
        # 左腰线（直线）
        left_straight = self.create_straight_line_path(
            geometry['top_left'], 
            geometry['bottom_left']
        )
        painter.drawPath(left_straight)
        
        # 右腰线（直线）
        right_straight = self.create_straight_line_path(
            geometry['top_right'], 
            geometry['bottom_right']
        )
        painter.drawPath(right_straight)
    
    def paintEvent(self, event):
        """绘制正确填充演示"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        
        try:
            # 背景
            painter.fillRect(self.rect(), QColor("#F5F5F5"))
            
            # 创建几何
            geometry = self.create_trapezoid_geometry()
            
            # 1. 绘制正确的填充区域（直线梯形）
            correct_fill = self.create_correct_fill_path(geometry)
            painter.setBrush(QColor("#90EE90"))  # 浅绿色 - 正确区域
            painter.setPen(Qt.NoPen)
            painter.drawPath(correct_fill)
            
            # 2. 绘制错误填充区域的轮廓（仅轮廓，不填充）
            wrong_fill = self.create_wrong_fill_path(geometry)
            painter.setBrush(Qt.NoBrush)
            painter.setPen(QPen(QColor("#FF6B6B"), 2, Qt.DashLine))  # 红色虚线 - 错误边界
            painter.drawPath(wrong_fill)
            
            # 3. 绘制直线腰线（虚线，显示正确的填充边界）
            self.draw_straight_lines(painter, geometry, "#006400", 2, Qt.DashLine)
            
            # 4. 绘制弯曲腰线（实线，显示实际的视觉效果）
            left_control, right_control = self.draw_curved_lines(painter, geometry)
            
            # 5. 标记关键点
            painter.setPen(QPen(QColor("#FF0000"), 2))
            painter.setBrush(QColor("#FF0000"))
            # 梯形顶点
            painter.drawEllipse(geometry['top_left'], 4, 4)
            painter.drawEllipse(geometry['top_right'], 4, 4)
            painter.drawEllipse(geometry['bottom_left'], 4, 4)
            painter.drawEllipse(geometry['bottom_right'], 4, 4)
            
            # 控制点
            painter.setPen(QPen(QColor("#0000FF"), 2))
            painter.setBrush(QColor("#0000FF"))
            painter.drawEllipse(left_control, 6, 6)
            painter.drawEllipse(right_control, 6, 6)
            
            # 6. 绘制说明文字
            painter.setPen(QColor("#333333"))
            painter.drawText(20, 30, "正确的弯曲梯形填充方案")
            painter.drawText(20, 50, "=" * 40)
            
            painter.drawText(20, 80, "✓ 浅绿色区域: 正确的填充区域（直线梯形）")
            painter.drawText(20, 100, "✗ 红色虚线: 错误的填充边界（包含弓形）")
            painter.drawText(20, 120, "--- 绿色虚线: 正确的填充边界（直线）")
            painter.drawText(20, 140, "━━━ 渐变实线: 视觉效果线（弯曲）")
            
            painter.drawText(20, 170, "关键理解:")
            painter.drawText(20, 190, "• 填充区域 = 直线梯形（排除弓形）")
            painter.drawText(20, 210, "• 视觉效果 = 弯曲腰线（覆盖在填充之上）")
            painter.drawText(20, 230, "• 弓形区域 = 弯曲线与直线之间的区域（不填充）")
            
            painter.drawText(20, 260, f"参数: 上底偏移{self.top_offset}px, 控制点{self.position_ratio}, 弯曲{self.curve_offset}px")
            
        except Exception as e:
            print(f"绘图错误: {e}")
        finally:
            painter.end()


class CorrectFillWindow(QMainWindow):
    """正确填充主窗口"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("正确的弯曲梯形填充方案 - 排除弓形区域")
        self.setGeometry(100, 100, 850, 650)
        
        self.widget = CorrectFillWidget()
        self.setCentralWidget(self.widget)


def main():
    """应用程序入口点"""
    app = QApplication(sys.argv)
    
    window = CorrectFillWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()