#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
正确实现与错误实现的对比分析
详细展示关键区别和技术要点
"""

import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget
from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QPainter, QPen, QColor, QPainterPath


class ImplementationComparisonWidget(QWidget):
    """实现方法对比Widget"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(1200, 800)
        self.setStyleSheet("background-color: #F0F0F0;")
    
    def create_correct_implementation(self, offset_x=0, offset_y=0):
        """
        ✅ 正确实现 (minimal_correct_fill.py的方法)
        """
        # 固定坐标 - 简单直接
        top_left = QPointF(200 + offset_x, 100 + offset_y)
        top_right = QPointF(250 + offset_x, 100 + offset_y)
        bottom_left = QPointF(150 + offset_x, 250 + offset_y)
        bottom_right = QPointF(300 + offset_x, 250 + offset_y)
        
        # 控制点计算 - 基于中点，统一向右偏移
        right_mid_x = (top_right.x() + bottom_right.x()) / 2
        right_mid_y = (top_right.y() + bottom_right.y()) / 2
        right_control = QPointF(right_mid_x + 70, right_mid_y)  # 固定偏移70
        
        left_mid_x = (top_left.x() + bottom_left.x()) / 2
        left_mid_y = (top_left.y() + bottom_left.y()) / 2
        left_control = QPointF(left_mid_x + 70, left_mid_y)    # 固定偏移70
        
        # 路径构建 - 严格顺序
        path = QPainterPath()
        path.moveTo(top_left)
        path.lineTo(top_right)                      # 上底
        path.quadTo(right_control, bottom_right)    # 右腰
        path.lineTo(bottom_left)                    # 下底
        path.quadTo(left_control, top_left)         # 左腰
        path.closeSubpath()
        
        return path, [top_left, top_right, bottom_left, bottom_right], [right_control, left_control]
    
    def create_wrong_implementation_v1(self, offset_x=0, offset_y=0):
        """
        ❌ 错误实现1 (基于我们之前的复杂参数化方法)
        问题：复杂的参数化计算 + position_ratio导致控制点位置不准确
        """
        # 复杂的几何计算
        center_x = 225 + offset_x
        start_y = 100 + offset_y
        top_offset = -25  # 上底左移
        
        top_center_x = center_x + top_offset
        top_left = QPointF(top_center_x - 15, start_y)
        top_right = QPointF(top_center_x + 15, start_y)
        bottom_left = QPointF(center_x - 75, start_y + 150)
        bottom_right = QPointF(center_x + 75, start_y + 150)
        
        # 错误的控制点计算 - 使用position_ratio
        position_ratio = 0.5
        curve_offset = 50
        
        # 右腰控制点 - 基于比例位置
        right_base_x = top_right.x() + (bottom_right.x() - top_right.x()) * position_ratio
        right_base_y = top_right.y() + (bottom_right.y() - top_right.y()) * position_ratio
        right_control = QPointF(right_base_x + curve_offset, right_base_y)
        
        # 左腰控制点 - 基于比例位置
        left_base_x = bottom_left.x() + (top_left.x() - bottom_left.x()) * position_ratio
        left_base_y = bottom_left.y() + (top_left.y() - bottom_left.y()) * position_ratio
        left_control = QPointF(left_base_x + curve_offset, left_base_y)
        
        # 路径构建
        path = QPainterPath()
        path.moveTo(top_left)
        path.lineTo(top_right)
        path.quadTo(right_control, bottom_right)
        path.lineTo(bottom_left)
        path.quadTo(left_control, top_left)
        path.closeSubpath()
        
        return path, [top_left, top_right, bottom_left, bottom_right], [right_control, left_control]
    
    def create_wrong_implementation_v2(self, offset_x=0, offset_y=0):
        """
        ❌ 错误实现2 (控制点方向不一致)
        问题：左右控制点偏移方向不一致
        """
        # 简单几何
        top_left = QPointF(200 + offset_x, 100 + offset_y)
        top_right = QPointF(250 + offset_x, 100 + offset_y)
        bottom_left = QPointF(150 + offset_x, 250 + offset_y)
        bottom_right = QPointF(300 + offset_x, 250 + offset_y)
        
        # 错误的控制点计算 - 方向不一致
        right_mid_x = (top_right.x() + bottom_right.x()) / 2
        right_mid_y = (top_right.y() + bottom_right.y()) / 2
        right_control = QPointF(right_mid_x + 70, right_mid_y)  # 向右偏移
        
        left_mid_x = (top_left.x() + bottom_left.x()) / 2
        left_mid_y = (top_left.y() + bottom_left.y()) / 2
        left_control = QPointF(left_mid_x - 70, left_mid_y)    # 向左偏移（错误！）
        
        # 路径构建
        path = QPainterPath()
        path.moveTo(top_left)
        path.lineTo(top_right)
        path.quadTo(right_control, bottom_right)
        path.lineTo(bottom_left)
        path.quadTo(left_control, top_left)
        path.closeSubpath()
        
        return path, [top_left, top_right, bottom_left, bottom_right], [right_control, left_control]
    
    def create_wrong_implementation_v3(self, offset_x=0, offset_y=0):
        """
        ❌ 错误实现3 (路径构建顺序错误)
        问题：不按正确顺序构建路径
        """
        # 正确几何和控制点
        top_left = QPointF(200 + offset_x, 100 + offset_y)
        top_right = QPointF(250 + offset_x, 100 + offset_y)
        bottom_left = QPointF(150 + offset_x, 250 + offset_y)
        bottom_right = QPointF(300 + offset_x, 250 + offset_y)
        
        right_mid_x = (top_right.x() + bottom_right.x()) / 2
        right_mid_y = (top_right.y() + bottom_right.y()) / 2
        right_control = QPointF(right_mid_x + 70, right_mid_y)
        
        left_mid_x = (top_left.x() + bottom_left.x()) / 2
        left_mid_y = (top_left.y() + bottom_left.y()) / 2
        left_control = QPointF(left_mid_x + 70, left_mid_y)
        
        # 错误的路径构建顺序
        path = QPainterPath()
        path.moveTo(top_left)
        path.quadTo(left_control, bottom_left)      # 先画左腰（错误顺序）
        path.lineTo(bottom_right)                   # 跨越连接
        path.quadTo(right_control, top_right)       # 再画右腰
        path.lineTo(top_left)                       # 回到起点
        path.closeSubpath()
        
        return path, [top_left, top_right, bottom_left, bottom_right], [right_control, left_control]
    
    def draw_implementation_comparison(self, painter, impl_func, title, color, x_offset, y_offset, error_points=None):
        """绘制实现对比"""
        painter.save()
        painter.translate(x_offset, y_offset)
        
        # 获取路径和点
        path, vertices, controls = impl_func()
        
        # 绘制填充
        painter.setBrush(QColor(color))
        painter.setPen(QPen(QColor("#333333"), 2))
        painter.drawPath(path)
        
        # 绘制顶点
        painter.setBrush(QColor("#FF0000"))
        painter.setPen(QPen(QColor("#FF0000"), 2))
        for vertex in vertices:
            painter.drawEllipse(vertex, 3, 3)
        
        # 绘制控制点
        painter.setBrush(QColor("#0000FF"))
        painter.setPen(QPen(QColor("#0000FF"), 2))
        for control in controls:
            painter.drawEllipse(control, 5, 5)
        
        # 标记错误点
        if error_points:
            painter.setBrush(QColor("#FF00FF"))
            painter.setPen(QPen(QColor("#FF00FF"), 3))
            for error_point in error_points:
                painter.drawEllipse(error_point, 8, 8)
        
        # 绘制标题
        painter.setPen(QColor("#333333"))
        painter.drawText(10, -10, title)
        
        painter.restore()
    
    def paintEvent(self, event):
        """绘制实现对比分析"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        
        try:
            # 背景
            painter.fillRect(self.rect(), QColor("#F0F0F0"))
            
            # 标题
            painter.setPen(QColor("#333333"))
            painter.drawText(20, 30, "正确实现 vs 错误实现 - 关键区别分析")
            painter.drawText(20, 50, "=" * 70)
            
            # 正确实现（左上）
            self.draw_implementation_comparison(
                painter, self.create_correct_implementation,
                "✅ 正确实现 (minimal_correct_fill.py)",
                "#90EE90", 50, 100
            )
            
            # 错误实现1（右上）
            self.draw_implementation_comparison(
                painter, self.create_wrong_implementation_v1,
                "❌ 错误实现1: 复杂参数化",
                "#FFB6C1", 400, 100
            )
            
            # 错误实现2（左下）
            _, _, controls_v2 = self.create_wrong_implementation_v2()
            self.draw_implementation_comparison(
                painter, self.create_wrong_implementation_v2,
                "❌ 错误实现2: 控制点方向不一致",
                "#FFD700", 50, 350,
                error_points=[controls_v2[1]]  # 标记错误的左控制点
            )
            
            # 错误实现3（右下）
            self.draw_implementation_comparison(
                painter, self.create_wrong_implementation_v3,
                "❌ 错误实现3: 路径构建顺序错误",
                "#DDA0DD", 400, 350
            )
            
            # 关键区别说明
            painter.setPen(QColor("#333333"))
            painter.drawText(50, 600, "关键区别分析:")
            
            painter.drawText(70, 630, "1. 控制点计算方法:")
            painter.drawText(90, 650, "✅ 正确: 基于中点 + 固定偏移量")
            painter.drawText(90, 670, "❌ 错误: 复杂的position_ratio计算")
            
            painter.drawText(70, 700, "2. 控制点偏移方向:")
            painter.drawText(90, 720, "✅ 正确: 两个控制点都向右偏移")
            painter.drawText(90, 740, "❌ 错误: 左右控制点偏移方向不一致")
            
            painter.drawText(450, 630, "3. 路径构建顺序:")
            painter.drawText(470, 650, "✅ 正确: 上底→右腰→下底→左腰")
            painter.drawText(470, 670, "❌ 错误: 随意顺序或跨越连接")
            
            painter.drawText(450, 700, "4. 代码复杂度:")
            painter.drawText(470, 720, "✅ 正确: 简单直接的固定坐标")
            painter.drawText(470, 740, "❌ 错误: 过度参数化和复杂计算")
            
            # 图例
            painter.drawText(800, 100, "图例:")
            painter.setBrush(QColor("#FF0000"))
            painter.drawEllipse(820, 120, 6, 6)
            painter.setPen(QColor("#333333"))
            painter.drawText(835, 128, "梯形顶点")
            
            painter.setBrush(QColor("#0000FF"))
            painter.drawEllipse(820, 140, 10, 10)
            painter.drawText(835, 148, "控制点")
            
            painter.setBrush(QColor("#FF00FF"))
            painter.drawEllipse(820, 160, 16, 16)
            painter.drawText(835, 168, "错误点")
            
        except Exception as e:
            print(f"绘图错误: {e}")
        finally:
            painter.end()


class ImplementationComparisonWindow(QMainWindow):
    """实现对比主窗口"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("正确实现 vs 错误实现 - 关键区别分析")
        self.setGeometry(100, 100, 1250, 850)
        
        self.widget = ImplementationComparisonWidget()
        self.setCentralWidget(self.widget)


def main():
    """应用程序入口点"""
    app = QApplication(sys.argv)
    
    window = ImplementationComparisonWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()