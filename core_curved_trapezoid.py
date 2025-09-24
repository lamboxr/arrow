#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
核心弯曲梯形程序
使用最核心的3个参数描绘弯曲梯形，集成渐变腰线功能
"""

import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget
from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QPainter, QLinearGradient, QPen, QColor, QPainterPath


# 渐变颜色定义 (来自原始gradient_trapezoid.py)
GRADIENT_COLORS = {
    'top': '#B6B384',      # 顶部颜色
    'middle': '#FEFFAF',   # 中间颜色
    'bottom': '#B7B286',   # 底部颜色
    'outline': '#B7B286'   # 轮廓颜色
}


class CoreCurvedTrapezoidWidget(QWidget):
    """核心弯曲梯形Widget - 使用3个核心参数"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # 核心参数1: 上底平移量 (像素) - 负值向左
        self.top_offset = -200
        
        # 核心参数2: 控制点位置比例 (0.0-1.0)
        self.position_ratio = 0.5
        
        # 核心参数3: 横向偏移量 (像素) - 正值向右
        self.curve_offset = 200
        
        # 固定的显示参数 (不影响曲线形状)
        self.trapezoid_height = 300
        self.trapezoid_top_width = 30
        self.trapezoid_bottom_width = 500
        self.line_width = 3
        
        # 设置窗口
        self.setFixedSize(700, 500)
        self.setStyleSheet("background-color: #94D8F6;")
    
    def create_trapezoid_geometry(self):
        """创建梯形几何 - 基于核心参数"""
        # 计算基础位置
        center_x = self.width() / 2
        start_y = (self.height() - self.trapezoid_height) / 2
        
        # 核心参数1: 上底平移量
        top_center_x = center_x + self.top_offset
        
        # 计算梯形顶点
        top_left_x = top_center_x - self.trapezoid_top_width / 2
        top_right_x = top_center_x + self.trapezoid_top_width / 2
        top_y = start_y
        
        # 下底保持居中
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
        """创建贝塞尔曲线 - 基于核心参数2和3"""
        path = QPainterPath()
        path.moveTo(start_point)
        
        # 核心参数2: 控制点位置比例
        base_x = start_point.x() + (end_point.x() - start_point.x()) * self.position_ratio
        base_y = start_point.y() + (end_point.y() - start_point.y()) * self.position_ratio
        
        # 核心参数3: 横向偏移量
        control_point = QPointF(base_x + self.curve_offset, base_y)
        
        # 创建二次贝塞尔曲线
        path.quadTo(control_point, end_point)
        
        return path, control_point
    
    def create_line_gradient(self, start_point, end_point):
        """创建腰线渐变 (来自gradient_trapezoid.py)"""
        # 创建沿腰线方向的线性渐变
        gradient = QLinearGradient(start_point, end_point)
        
        # 设置渐变颜色点
        # 起点（上端）：#B6B384，完全透明（alpha=0）
        top_color = QColor(GRADIENT_COLORS['top'])
        top_color.setAlpha(0)  # 完全透明
        gradient.setColorAt(0.0, top_color)
        
        # 中间（50%）：#FEFFAF，50%透明（alpha=127）
        middle_color = QColor(GRADIENT_COLORS['middle'])
        middle_color.setAlpha(127)  # 50%透明
        gradient.setColorAt(0.5, middle_color)
        
        # 终点（下端）：#B7B286，完全透明（alpha=0）
        bottom_color = QColor(GRADIENT_COLORS['bottom'])
        bottom_color.setAlpha(0)  # 完全透明
        gradient.setColorAt(1.0, bottom_color)
        
        return gradient
    
    def draw_curved_trapezoid(self, painter, geometry):
        """绘制弯曲梯形的渐变腰线"""
        # 绘制左腰线（弯曲，带渐变）
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
        
        # 绘制右腰线（弯曲，带渐变）
        right_path, right_control = self.create_bezier_curve(
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
        
        return left_control, right_control
    
    def create_filled_trapezoid_path(self, geometry):
        """创建正确的梯形填充路径 - 只填充直线梯形区域，排除弓形"""
        path = QPainterPath()
        
        # 从上底左端点开始
        path.moveTo(geometry['top_left'])
        
        # 绘制上底 (直线)
        path.lineTo(geometry['top_right'])
        
        # 绘制右腰线 (直线，不是贝塞尔曲线)
        path.lineTo(geometry['bottom_right'])
        
        # 绘制下底 (直线)
        path.lineTo(geometry['bottom_left'])
        
        # 绘制左腰线 (直线，不是贝塞尔曲线)
        path.lineTo(geometry['top_left'])
        
        # 闭合路径
        path.closeSubpath()
        
        return path
    
    def paintEvent(self, event):
        """绘制核心弯曲梯形"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        
        try:
            # 0. 绘制背景色
            painter.fillRect(self.rect(), QColor("#BDC5D5"))
            
            # 1. 创建梯形几何
            geometry = self.create_trapezoid_geometry()
            
            # 2. 绘制填充的弯曲梯形
            filled_path = self.create_filled_trapezoid_path(geometry)
            painter.setBrush(QColor("#CBD900"))  # 设置填充颜色
            painter.setPen(Qt.NoPen)  # 不绘制边框
            painter.drawPath(filled_path)
            
            # 3. 绘制弯曲梯形的渐变腰线 (在填充之上)
            left_control, right_control = self.draw_curved_trapezoid(painter, geometry)
            
            # 4. 绘制参数信息
            painter.setPen(QColor("#333333"))
            painter.drawText(20, 30, "核心弯曲梯形 - 3参数控制 + 颜色填充")
            painter.drawText(20, 50, "=" * 40)
            
            painter.drawText(20, 80, f"参数1 - 上底平移量: {self.top_offset:+.0f} 像素")
            painter.drawText(20, 100, f"参数2 - 控制点位置比例: {self.position_ratio:.2f}")
            painter.drawText(20, 120, f"参数3 - 横向偏移量: {self.curve_offset:+.0f} 像素")
            
            painter.drawText(20, 150, "填充颜色: #CBD900")
            painter.drawText(20, 170, "渐变腰线特性:")
            painter.drawText(20, 190, f"• 顶部: {GRADIENT_COLORS['top']} (完全透明)")
            painter.drawText(20, 210, f"• 中间: {GRADIENT_COLORS['middle']} (50%透明)")
            painter.drawText(20, 230, f"• 底部: {GRADIENT_COLORS['bottom']} (完全透明)")
            
            # 5. 绘制关键点标记 (可选，用于调试)
            if True:  # 显示关键点
                # 梯形顶点
                painter.setPen(QPen(QColor("#FF0000"), 2))
                painter.setBrush(QColor("#FF0000"))
                painter.drawEllipse(geometry['top_left'], 4, 4)
                painter.drawEllipse(geometry['top_right'], 4, 4)
                painter.drawEllipse(geometry['bottom_left'], 4, 4)
                painter.drawEllipse(geometry['bottom_right'], 4, 4)
                
                # 控制点
                painter.setPen(QPen(QColor("#0000FF"), 2))
                painter.setBrush(QColor("#0000FF"))
                painter.drawEllipse(left_control, 6, 6)
                painter.drawEllipse(right_control, 6, 6)
                
                # 标注
                painter.setPen(QColor("#333333"))
                painter.drawText(geometry['top_left'].x() - 30, geometry['top_left'].y() - 10, "上左")
                painter.drawText(geometry['top_right'].x() + 10, geometry['top_right'].y() - 10, "上右")
                painter.drawText(geometry['bottom_left'].x() - 30, geometry['bottom_left'].y() + 20, "下左")
                painter.drawText(geometry['bottom_right'].x() + 10, geometry['bottom_right'].y() + 20, "下右")
                painter.drawText(left_control.x() - 30, left_control.y() - 10, "左控制点")
                painter.drawText(right_control.x() + 10, right_control.y() - 10, "右控制点")
            
        except Exception as e:
            print(f"绘图错误: {e}")
        finally:
            painter.end()


class CoreCurvedTrapezoidWindow(QMainWindow):
    """核心弯曲梯形主窗口"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("核心弯曲梯形 - 3参数 + 渐变腰线")
        self.setGeometry(100, 100, 750, 600)
        
        # 创建并设置中心Widget
        self.trapezoid_widget = CoreCurvedTrapezoidWidget()
        self.setCentralWidget(self.trapezoid_widget)


def main():
    """应用程序入口点"""
    app = QApplication(sys.argv)
    
    # 创建主窗口
    window = CoreCurvedTrapezoidWindow()
    window.show()
    
    # 运行应用程序
    sys.exit(app.exec())


if __name__ == "__main__":
    main()