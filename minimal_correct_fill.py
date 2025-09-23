#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最小化正确填充实现
基于qt_bezier_fill_test.py中验证正确的填充逻辑
"""

import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget
from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QPainter, QPen, QColor, QPainterPath


class MinimalCorrectFillWidget(QWidget):
    """最小化正确填充Widget"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(600, 400)
        self.setStyleSheet("background-color: #F0F0F0;")
    
    def create_correct_trapezoid_fill(self):
        """
        创建正确的弯曲梯形填充路径
        
        核心技术要点:
        1. 使用QPainterPath构建封闭路径
        2. 两条腰线都使用二次贝塞尔曲线(quadTo)
        3. 关键：两个控制点都向右偏移，确保一致的弯曲方向
        4. 严格按照：上底→右腰→下底→左腰的顺序构建路径
        
        Returns:
            tuple: (路径对象, 顶点列表, 控制点列表)
        """
        path = QPainterPath()
        
        # ========== 第一步：定义梯形的四个顶点 ==========
        # 坐标系：左上角为原点，X轴向右，Y轴向下
        top_left = QPointF(200, 100)      # 上底左端点
        top_right = QPointF(250, 100)     # 上底右端点  
        bottom_left = QPointF(150, 250)   # 下底左端点
        bottom_right = QPointF(300, 250)  # 下底右端点
        
        # ========== 第二步：计算贝塞尔曲线控制点 ==========
        # 关键发现：两个控制点都必须向右偏移，保持一致的弯曲方向
        # 这是避免填充错误的核心要素
        
        # 右腰控制点：位于右腰线中点右侧
        # 计算：右腰中点 + 向右偏移量
        right_mid_x = (top_right.x() + bottom_right.x()) / 2  # 右腰中点X
        right_mid_y = (top_right.y() + bottom_right.y()) / 2  # 右腰中点Y
        right_control = QPointF(right_mid_x + 70, right_mid_y)  # 向右偏移70像素
        
        # 左腰控制点：位于左腰线中点右侧（注意：也是向右偏移！）
        # 计算：左腰中点 + 向右偏移量
        left_mid_x = (top_left.x() + bottom_left.x()) / 2   # 左腰中点X
        left_mid_y = (top_left.y() + bottom_left.y()) / 2   # 左腰中点Y  
        left_control = QPointF(left_mid_x + 70, left_mid_y)   # 向右偏移70像素
        
        # ========== 第三步：按顺序构建QPainterPath ==========
        # 路径构建顺序至关重要，必须形成正确的封闭图形
        
        # 起点：从上底左端点开始
        path.moveTo(top_left)
        
        # 1. 绘制上底边（直线段）
        # 从上底左端点 → 上底右端点
        path.lineTo(top_right)
        
        # 2. 绘制右腰边（二次贝塞尔曲线）
        # 从上底右端点 → 通过右控制点 → 下底右端点
        # quadTo(控制点, 终点) 创建二次贝塞尔曲线
        path.quadTo(right_control, bottom_right)
        
        # 3. 绘制下底边（直线段）
        # 从下底右端点 → 下底左端点
        path.lineTo(bottom_left)
        
        # 4. 绘制左腰边（二次贝塞尔曲线）
        # 从下底左端点 → 通过左控制点 → 上底左端点
        # 注意：这里回到起点，形成封闭图形
        path.quadTo(left_control, top_left)
        
        # ========== 第四步：闭合路径 ==========
        # 确保路径正确闭合，启用填充算法
        path.closeSubpath()
        
        # 返回路径对象和关键点坐标（用于调试和可视化）
        vertices = [top_left, top_right, bottom_left, bottom_right]
        controls = [right_control, left_control]
        
        return path, vertices, controls
    
    def paintEvent(self, event):
        """绘制最小化正确填充"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        
        try:
            # 背景
            painter.fillRect(self.rect(), QColor("#F0F0F0"))
            
            # 创建并绘制正确的梯形填充
            trapezoid_path, vertices, controls = self.create_correct_trapezoid_fill()
            
            # 填充梯形
            painter.setBrush(QColor("#90EE90"))  # 浅绿色
            painter.setPen(QPen(QColor("#00AA00"), 2))
            painter.drawPath(trapezoid_path)
            
            # 标记顶点
            painter.setBrush(QColor("#FF0000"))
            painter.setPen(QPen(QColor("#FF0000"), 2))
            for vertex in vertices:
                painter.drawEllipse(vertex, 4, 4)
            
            # 标记控制点
            painter.setBrush(QColor("#0000FF"))
            painter.setPen(QPen(QColor("#0000FF"), 2))
            for control in controls:
                painter.drawEllipse(control, 6, 6)
            
            # 说明文字
            painter.setPen(QColor("#333333"))
            painter.drawText(20, 30, "最小化正确填充实现")
            painter.drawText(20, 50, "=" * 30)
            
            painter.drawText(20, 80, "🟢 绿色区域: 梯形填充")
            painter.drawText(20, 100, "🔴 红点: 梯形顶点")
            painter.drawText(20, 120, "🔵 蓝点: 贝塞尔控制点")
            
            painter.drawText(20, 150, "关键特征:")
            painter.drawText(20, 170, "• 两条腰线都使用贝塞尔曲线")
            painter.drawText(20, 190, "• 两个控制点都向右偏移")
            painter.drawText(20, 210, "• 使用quadTo()方法")
            painter.drawText(20, 230, "• 路径正确闭合")
            
            painter.drawText(20, 260, "观察: 填充是否正确？")
            painter.drawText(20, 280, "• 是否只填充了预期区域？")
            painter.drawText(20, 300, "• 是否有意外的填充？")
            
        except Exception as e:
            print(f"绘图错误: {e}")
        finally:
            painter.end()


class MinimalCorrectFillWindow(QMainWindow):
    """最小化正确填充主窗口"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("最小化正确填充实现")
        self.setGeometry(100, 100, 650, 450)
        
        self.widget = MinimalCorrectFillWidget()
        self.setCentralWidget(self.widget)


def main():
    """应用程序入口点"""
    app = QApplication(sys.argv)
    
    window = MinimalCorrectFillWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()