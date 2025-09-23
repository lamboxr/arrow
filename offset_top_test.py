#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
上底偏移测试 - 基于minimal_correct_fill.py
仅仅水平移动上底，观察填充效果的变化
"""

import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget
from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QPainter, QPen, QColor, QPainterPath


class OffsetTopTestWidget(QWidget):
    """上底偏移测试Widget"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(800, 600)
        self.setStyleSheet("background-color: #F0F0F0;")
    
    def create_original_trapezoid(self, offset_x=0, offset_y=0):
        """
        原始梯形 - 与minimal_correct_fill.py完全相同
        """
        path = QPainterPath()
        
        # 原始坐标（与minimal_correct_fill.py相同）
        top_left = QPointF(200 + offset_x, 100 + offset_y)
        top_right = QPointF(250 + offset_x, 100 + offset_y)
        bottom_left = QPointF(150 + offset_x, 250 + offset_y)
        bottom_right = QPointF(300 + offset_x, 250 + offset_y)
        
        # 控制点计算（与原版相同）
        right_mid_x = (top_right.x() + bottom_right.x()) / 2
        right_mid_y = (top_right.y() + bottom_right.y()) / 2
        right_control = QPointF(right_mid_x + 70, right_mid_y)
        
        left_mid_x = (top_left.x() + bottom_left.x()) / 2
        left_mid_y = (top_left.y() + bottom_left.y()) / 2
        left_control = QPointF(left_mid_x + 70, left_mid_y)
        
        # 路径构建（与原版相同）
        path.moveTo(top_left)
        path.lineTo(top_right)
        path.quadTo(right_control, bottom_right)
        path.lineTo(bottom_left)
        path.quadTo(left_control, top_left)
        path.closeSubpath()
        
        return path, [top_left, top_right, bottom_left, bottom_right], [right_control, left_control]
    
    def create_offset_top_trapezoid(self, top_offset, offset_x=0, offset_y=0):
        """
        上底偏移梯形 - 只移动上底，其他保持不变
        
        Args:
            top_offset: 上底水平偏移量（正值向右，负值向左）
        """
        path = QPainterPath()
        
        # 上底坐标 - 添加水平偏移
        top_left = QPointF(200 + top_offset + offset_x, 100 + offset_y)      # 上底左偏移
        top_right = QPointF(250 + top_offset + offset_x, 100 + offset_y)     # 上底右偏移
        
        # 下底坐标 - 保持不变
        bottom_left = QPointF(150 + offset_x, 250 + offset_y)    # 下底左不变
        bottom_right = QPointF(300 + offset_x, 250 + offset_y)   # 下底右不变
        
        # 控制点计算 - 基于新的顶点位置
        right_mid_x = (top_right.x() + bottom_right.x()) / 2
        right_mid_y = (top_right.y() + bottom_right.y()) / 2
        right_control = QPointF(right_mid_x + 70, right_mid_y)
        
        left_mid_x = (top_left.x() + bottom_left.x()) / 2
        left_mid_y = (top_left.y() + bottom_left.y()) / 2
        left_control = QPointF(left_mid_x + 70, left_mid_y)
        
        # 路径构建 - 相同顺序
        path.moveTo(top_left)
        path.lineTo(top_right)
        path.quadTo(right_control, bottom_right)
        path.lineTo(bottom_left)
        path.quadTo(left_control, top_left)
        path.closeSubpath()
        
        return path, [top_left, top_right, bottom_left, bottom_right], [right_control, left_control]
    
    def draw_trapezoid_comparison(self, painter, impl_func, title, color, x_offset, y_offset):
        """绘制梯形对比"""
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
            painter.drawEllipse(vertex, 4, 4)
        
        # 绘制控制点
        painter.setBrush(QColor("#0000FF"))
        painter.setPen(QPen(QColor("#0000FF"), 2))
        for control in controls:
            painter.drawEllipse(control, 6, 6)
        
        # 绘制控制线（辅助线）
        painter.setPen(QPen(QColor("#0000FF"), 1, Qt.DotLine))
        if len(controls) >= 2 and len(vertices) >= 4:
            # 右腰控制线
            painter.drawLine(vertices[1], controls[0])  # top_right -> right_control
            painter.drawLine(controls[0], vertices[3])  # right_control -> bottom_right
            
            # 左腰控制线
            painter.drawLine(vertices[2], controls[1])  # bottom_left -> left_control
            painter.drawLine(controls[1], vertices[0])  # left_control -> top_left
        
        # 绘制标题
        painter.setPen(QColor("#333333"))
        painter.drawText(10, -15, title)
        
        painter.restore()
    
    def paintEvent(self, event):
        """绘制上底偏移测试对比"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        
        try:
            # 背景
            painter.fillRect(self.rect(), QColor("#F0F0F0"))
            
            # 标题
            painter.setPen(QColor("#333333"))
            painter.drawText(20, 30, "上底偏移对填充效果的影响测试")
            painter.drawText(20, 50, "=" * 50)
            
            # 原始梯形（左上）
            self.draw_trapezoid_comparison(
                painter, lambda: self.create_original_trapezoid(-150, -50),
                "原始梯形（上底居中）", "#90EE90", 50, 100
            )
            
            # 上底左移（右上）
            self.draw_trapezoid_comparison(
                painter, lambda: self.create_offset_top_trapezoid(-50, -150, -50),
                "上底左移 -50px", "#FFD700", 400, 100
            )
            
            # 上底右移（左下）
            self.draw_trapezoid_comparison(
                painter, lambda: self.create_offset_top_trapezoid(+50, -150, -50),
                "上底右移 +50px", "#87CEEB", 50, 350
            )
            
            # 上底大幅左移（右下）
            self.draw_trapezoid_comparison(
                painter, lambda: self.create_offset_top_trapezoid(-100, -150, -50),
                "上底大幅左移 -100px", "#FFB6C1", 400, 350
            )
            
            # 说明文字
            painter.setPen(QColor("#333333"))
            painter.drawText(20, 550, "观察要点:")
            painter.drawText(40, 570, "• 填充区域形状的变化    • 控制点位置的变化    • 是否出现填充错误")
            
        except Exception as e:
            print(f"绘图错误: {e}")
        finally:
            painter.end()


class OffsetTopTestWindow(QMainWindow):
    """上底偏移测试主窗口"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("上底偏移对填充效果的影响测试")
        self.setGeometry(100, 100, 850, 650)
        
        self.widget = OffsetTopTestWidget()
        self.setCentralWidget(self.widget)


def main():
    """应用程序入口点"""
    app = QApplication(sys.argv)
    
    window = OffsetTopTestWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()