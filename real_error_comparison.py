#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
真实错误对比 - 展示实际会产生错误填充的实现
"""

import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget
from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QPainter, QPen, QColor, QPainterPath


class RealErrorComparisonWidget(QWidget):
    """真实错误对比Widget"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(1000, 700)
        self.setStyleSheet("background-color: #F0F0F0;")
    
    def create_correct_implementation(self, offset_x=0, offset_y=0):
        """✅ 正确实现"""
        top_left = QPointF(100 + offset_x, 80 + offset_y)
        top_right = QPointF(150 + offset_x, 80 + offset_y)
        bottom_left = QPointF(50 + offset_x, 180 + offset_y)
        bottom_right = QPointF(200 + offset_x, 180 + offset_y)
        
        # 关键：两个控制点都向右偏移
        right_mid_x = (top_right.x() + bottom_right.x()) / 2
        right_mid_y = (top_right.y() + bottom_right.y()) / 2
        right_control = QPointF(right_mid_x + 40, right_mid_y)
        
        left_mid_x = (top_left.x() + bottom_left.x()) / 2
        left_mid_y = (top_left.y() + bottom_left.y()) / 2
        left_control = QPointF(left_mid_x + 40, left_mid_y)  # 也向右
        
        path = QPainterPath()
        path.moveTo(top_left)
        path.lineTo(top_right)
        path.quadTo(right_control, bottom_right)
        path.lineTo(bottom_left)
        path.quadTo(left_control, top_left)
        path.closeSubpath()
        
        return path, [top_left, top_right, bottom_left, bottom_right], [right_control, left_control]
    
    def create_opposite_direction_error(self, offset_x=0, offset_y=0):
        """❌ 真实错误：控制点方向相反"""
        top_left = QPointF(100 + offset_x, 80 + offset_y)
        top_right = QPointF(150 + offset_x, 80 + offset_y)
        bottom_left = QPointF(50 + offset_x, 180 + offset_y)
        bottom_right = QPointF(200 + offset_x, 180 + offset_y)
        
        # 错误：控制点方向相反
        right_mid_x = (top_right.x() + bottom_right.x()) / 2
        right_mid_y = (top_right.y() + bottom_right.y()) / 2
        right_control = QPointF(right_mid_x + 40, right_mid_y)  # 向右
        
        left_mid_x = (top_left.x() + bottom_left.x()) / 2
        left_mid_y = (top_left.y() + bottom_left.y()) / 2
        left_control = QPointF(left_mid_x - 40, left_mid_y)    # 向左（错误！）
        
        path = QPainterPath()
        path.moveTo(top_left)
        path.lineTo(top_right)
        path.quadTo(right_control, bottom_right)
        path.lineTo(bottom_left)
        path.quadTo(left_control, top_left)
        path.closeSubpath()
        
        return path, [top_left, top_right, bottom_left, bottom_right], [right_control, left_control]
    
    def create_extreme_offset_error(self, offset_x=0, offset_y=0):
        """❌ 真实错误：极端偏移量导致自相交"""
        top_left = QPointF(100 + offset_x, 80 + offset_y)
        top_right = QPointF(150 + offset_x, 80 + offset_y)
        bottom_left = QPointF(50 + offset_x, 180 + offset_y)
        bottom_right = QPointF(200 + offset_x, 180 + offset_y)
        
        # 错误：极端偏移量
        right_mid_x = (top_right.x() + bottom_right.x()) / 2
        right_mid_y = (top_right.y() + bottom_right.y()) / 2
        right_control = QPointF(right_mid_x + 150, right_mid_y)  # 极端向右偏移
        
        left_mid_x = (top_left.x() + bottom_left.x()) / 2
        left_mid_y = (top_left.y() + bottom_left.y()) / 2
        left_control = QPointF(left_mid_x + 150, left_mid_y)     # 极端向右偏移
        
        path = QPainterPath()
        path.moveTo(top_left)
        path.lineTo(top_right)
        path.quadTo(right_control, bottom_right)
        path.lineTo(bottom_left)
        path.quadTo(left_control, top_left)
        path.closeSubpath()
        
        return path, [top_left, top_right, bottom_left, bottom_right], [right_control, left_control]
    
    def create_wrong_order_error(self, offset_x=0, offset_y=0):
        """❌ 真实错误：路径构建顺序错误导致自相交"""
        top_left = QPointF(100 + offset_x, 80 + offset_y)
        top_right = QPointF(150 + offset_x, 80 + offset_y)
        bottom_left = QPointF(50 + offset_x, 180 + offset_y)
        bottom_right = QPointF(200 + offset_x, 180 + offset_y)
        
        # 正确的控制点
        right_mid_x = (top_right.x() + bottom_right.x()) / 2
        right_mid_y = (top_right.y() + bottom_right.y()) / 2
        right_control = QPointF(right_mid_x + 40, right_mid_y)
        
        left_mid_x = (top_left.x() + bottom_left.x()) / 2
        left_mid_y = (top_left.y() + bottom_left.y()) / 2
        left_control = QPointF(left_mid_x + 40, left_mid_y)
        
        # 错误：构建顺序导致路径交叉
        path = QPainterPath()
        path.moveTo(top_left)
        path.quadTo(left_control, bottom_left)      # 先画左腰
        path.lineTo(top_right)                      # 跨越到上底右（交叉！）
        path.quadTo(right_control, bottom_right)    # 画右腰
        path.lineTo(top_left)                       # 跨越回起点（交叉！）
        path.closeSubpath()
        
        return path, [top_left, top_right, bottom_left, bottom_right], [right_control, left_control]
    
    def create_complex_self_intersection(self, offset_x=0, offset_y=0):
        """❌ 真实错误：复杂自相交路径"""
        top_left = QPointF(100 + offset_x, 80 + offset_y)
        top_right = QPointF(150 + offset_x, 80 + offset_y)
        bottom_left = QPointF(50 + offset_x, 180 + offset_y)
        bottom_right = QPointF(200 + offset_x, 180 + offset_y)
        
        # 故意创建会导致复杂自相交的控制点
        right_control = QPointF(top_left.x() - 50, (top_right.y() + bottom_right.y()) / 2)  # 控制点在左侧
        left_control = QPointF(bottom_right.x() + 50, (top_left.y() + bottom_left.y()) / 2)  # 控制点在右侧
        
        path = QPainterPath()
        path.moveTo(top_left)
        path.lineTo(top_right)
        path.quadTo(right_control, bottom_right)
        path.lineTo(bottom_left)
        path.quadTo(left_control, top_left)
        path.closeSubpath()
        
        return path, [top_left, top_right, bottom_left, bottom_right], [right_control, left_control]
    
    def draw_comparison_item(self, painter, impl_func, title, x_offset, y_offset, is_correct=False):
        """绘制对比项"""
        painter.save()
        painter.translate(x_offset, y_offset)
        
        # 获取路径和点
        path, vertices, controls = impl_func()
        
        # 选择颜色
        if is_correct:
            fill_color = "#90EE90"  # 浅绿色
            border_color = "#00AA00"
        else:
            fill_color = "#FFB6C1"  # 浅红色
            border_color = "#FF0000"
        
        # 绘制填充
        painter.setBrush(QColor(fill_color))
        painter.setPen(QPen(QColor(border_color), 2))
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
        """绘制真实错误对比"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        
        try:
            # 背景
            painter.fillRect(self.rect(), QColor("#F0F0F0"))
            
            # 标题
            painter.setPen(QColor("#333333"))
            painter.drawText(20, 30, "真实错误填充对比 - 展示实际会产生错误的实现")
            painter.drawText(20, 50, "=" * 70)
            
            # 正确实现（左上）
            self.draw_comparison_item(
                painter, self.create_correct_implementation,
                "✅ 正确实现", 50, 100, is_correct=True
            )
            
            # 错误实现1（右上）
            self.draw_comparison_item(
                painter, self.create_opposite_direction_error,
                "❌ 控制点方向相反", 350, 100
            )
            
            # 错误实现2（左中）
            self.draw_comparison_item(
                painter, self.create_extreme_offset_error,
                "❌ 极端偏移量", 50, 280
            )
            
            # 错误实现3（右中）
            self.draw_comparison_item(
                painter, self.create_wrong_order_error,
                "❌ 路径构建顺序错误", 350, 280
            )
            
            # 错误实现4（中下）
            self.draw_comparison_item(
                painter, self.create_complex_self_intersection,
                "❌ 复杂自相交", 200, 460
            )
            
            # 说明文字
            painter.setPen(QColor("#333333"))
            painter.drawText(650, 120, "观察要点:")
            painter.drawText(670, 140, "• 填充区域的差异")
            painter.drawText(670, 160, "• 是否出现意外填充")
            painter.drawText(670, 180, "• 路径是否自相交")
            
            painter.drawText(650, 220, "图例:")
            painter.drawText(670, 240, "🔴 红点: 梯形顶点")
            painter.drawText(670, 260, "🔵 蓝点: 控制点")
            painter.drawText(670, 280, "··· 蓝线: 控制线")
            
            painter.drawText(650, 320, "错误类型:")
            painter.drawText(670, 340, "1. 控制点方向不一致")
            painter.drawText(670, 360, "2. 偏移量过大")
            painter.drawText(670, 380, "3. 路径构建顺序错误")
            painter.drawText(670, 400, "4. 控制点位置错误")
            
        except Exception as e:
            print(f"绘图错误: {e}")
        finally:
            painter.end()


class RealErrorComparisonWindow(QMainWindow):
    """真实错误对比主窗口"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("真实错误填充对比")
        self.setGeometry(100, 100, 1050, 750)
        
        self.widget = RealErrorComparisonWidget()
        self.setCentralWidget(self.widget)


def main():
    """应用程序入口点"""
    app = QApplication(sys.argv)
    
    window = RealErrorComparisonWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()