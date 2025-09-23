#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
方案2: 路径减法运算
解决弓形区域错误填充问题 - 创建完整梯形路径，然后减去弓形区域
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


class Solution2Widget(QWidget):
    """方案2: 路径减法运算Widget"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # 核心参数1: 上底平移量 (像素) - 负值向左
        self.top_offset = -200
        
        # 核心参数2: 控制点位置比例 (0.0-1.0)
        self.position_ratio = 0.5
        
        # 核心参数3: 横向偏移量 (像素) - 正值向右
        self.curve_offset = 50
        
        # 固定的显示参数 (不影响曲线形状)
        self.trapezoid_height = 300
        self.trapezoid_top_width = 30
        self.trapezoid_bottom_width = 500
        self.line_width = 3
        
        # 设置窗口
        self.setFixedSize(700, 500)
        self.setStyleSheet("background-color: #BDC5D5;")
    
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
    
    def create_full_trapezoid_path(self, geometry):
        """创建完整的梯形路径（包含弓形区域）"""
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
    
    def create_left_bow_path(self, geometry):
        """创建左侧弓形区域路径（需要被减去的部分）"""
        path = QPainterPath()
        
        # 左侧弓形：原始直线腰线与贝塞尔曲线之间的区域
        
        # 从上底左端点开始
        path.moveTo(geometry['top_left'])
        
        # 沿直线到下底左端点
        path.lineTo(geometry['bottom_left'])
        
        # 沿贝塞尔曲线回到上底左端点
        left_base_x = geometry['top_left'].x() + (geometry['bottom_left'].x() - geometry['top_left'].x()) * self.position_ratio
        left_base_y = geometry['top_left'].y() + (geometry['bottom_left'].y() - geometry['top_left'].y()) * self.position_ratio
        left_control_point = QPointF(left_base_x + self.curve_offset, left_base_y)
        
        # 注意：这里需要反向绘制贝塞尔曲线
        path.quadTo(left_control_point, geometry['top_left'])
        
        # 闭合路径
        path.closeSubpath()
        
        return path
    
    def create_right_bow_path(self, geometry):
        """创建右侧弓形区域路径（保留的部分，不减去）"""
        path = QPainterPath()
        
        # 右侧弓形：原始直线腰线与贝塞尔曲线之间的区域
        
        # 从上底右端点开始
        path.moveTo(geometry['top_right'])
        
        # 沿直线到下底右端点
        path.lineTo(geometry['bottom_right'])
        
        # 沿贝塞尔曲线回到上底右端点
        right_base_x = geometry['top_right'].x() + (geometry['bottom_right'].x() - geometry['top_right'].x()) * self.position_ratio
        right_base_y = geometry['top_right'].y() + (geometry['bottom_right'].y() - geometry['top_right'].y()) * self.position_ratio
        right_control_point = QPointF(right_base_x + self.curve_offset, right_base_y)
        
        # 注意：这里需要反向绘制贝塞尔曲线
        path.quadTo(right_control_point, geometry['top_right'])
        
        # 闭合路径
        path.closeSubpath()
        
        return path
    
    def create_path_subtraction_fill(self, geometry):
        """方案2: 路径减法运算 - 完整梯形减去左侧弓形"""
        # 创建完整梯形路径
        full_trapezoid = self.create_full_trapezoid_path(geometry)
        
        # 创建左侧弓形路径
        left_bow = self.create_left_bow_path(geometry)
        
        # 执行路径减法运算
        # 注意：QPainterPath的减法运算使用 subtracted() 方法
        result_path = full_trapezoid.subtracted(left_bow)
        
        return result_path
    
    def paintEvent(self, event):
        """绘制方案2: 路径减法运算"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        
        try:
            # 0. 绘制背景色
            painter.fillRect(self.rect(), QColor("#BDC5D5"))
            
            # 1. 创建梯形几何
            geometry = self.create_trapezoid_geometry()
            
            # 2. 方案2: 路径减法运算填充
            filled_path = self.create_path_subtraction_fill(geometry)
            painter.setBrush(QColor("#CBD900"))  # 设置填充颜色
            painter.setPen(Qt.NoPen)  # 不绘制边框
            painter.drawPath(filled_path)
            
            # 3. 绘制弯曲梯形的渐变腰线 (在填充之上)
            left_control, right_control = self.draw_curved_trapezoid(painter, geometry)
            
            # 4. 绘制方案信息
            painter.setPen(QColor("#333333"))
            painter.drawText(20, 30, "方案2: 路径减法运算")
            painter.drawText(20, 50, "=" * 25)
            
            painter.drawText(20, 80, f"参数1 - 上底平移量: {self.top_offset:+.0f} 像素")
            painter.drawText(20, 100, f"参数2 - 控制点位置比例: {self.position_ratio:.2f}")
            painter.drawText(20, 120, f"参数3 - 横向偏移量: {self.curve_offset:+.0f} 像素")
            
            painter.drawText(20, 150, "解决方案: 路径布尔运算")
            painter.drawText(20, 170, "• 步骤1: 创建完整直线梯形")
            painter.drawText(20, 190, "• 步骤2: 创建左侧弓形区域")
            painter.drawText(20, 210, "• 步骤3: 执行减法运算")
            painter.drawText(20, 230, "• 结果: 完整梯形 - 左侧弓形")
            painter.drawText(20, 250, "• 保留: 右侧弓形区域")
            
            # 5. 显示调试信息（可选）
            painter.drawText(20, 280, "技术实现:")
            painter.drawText(20, 300, "• QPainterPath.subtracted() 方法")
            painter.drawText(20, 320, "• 布尔路径运算")
            
        except Exception as e:
            print(f"绘图错误: {e}")
        finally:
            painter.end()


class Solution2Window(QMainWindow):
    """方案2主窗口"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("方案2: 路径减法运算 - 解决弓形填充问题")
        self.setGeometry(100, 100, 750, 600)
        
        # 创建并设置中心Widget
        self.trapezoid_widget = Solution2Widget()
        self.setCentralWidget(self.trapezoid_widget)


def main():
    """应用程序入口点"""
    app = QApplication(sys.argv)
    
    # 创建主窗口
    window = Solution2Window()
    window.show()
    
    # 运行应用程序
    sys.exit(app.exec())


if __name__ == "__main__":
    main()