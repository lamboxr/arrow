#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
贝塞尔曲线控制点详细解释
可视化展示控制点的作用和位置
"""

import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget
from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QPainter, QPen, QColor, QPainterPath


class ControlPointExplanationWidget(QWidget):
    """控制点解释Widget"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(800, 600)
        self.setStyleSheet("background-color: #F0F0F0;")
    
    def paintEvent(self, event):
        """绘制控制点解释图"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        
        try:
            # 背景
            painter.fillRect(self.rect(), QColor("#F0F0F0"))
            
            # 标题
            painter.setPen(QColor("#333333"))
            painter.drawText(20, 30, "贝塞尔曲线控制点详细解释")
            painter.drawText(20, 50, "=" * 40)
            
            # ========== 第一部分：单个贝塞尔曲线演示 ==========
            painter.drawText(20, 80, "1. 单个贝塞尔曲线的构成:")
            
            # 定义一条简单的贝塞尔曲线
            start_point = QPointF(100, 120)      # 起点
            end_point = QPointF(100, 220)        # 终点
            control_point = QPointF(180, 170)    # 控制点（向右偏移）
            
            # 绘制贝塞尔曲线
            curve_path = QPainterPath()
            curve_path.moveTo(start_point)
            curve_path.quadTo(control_point, end_point)
            
            painter.setPen(QPen(QColor("#FF6B6B"), 3))
            painter.drawPath(curve_path)
            
            # 绘制直线（对比）
            straight_path = QPainterPath()
            straight_path.moveTo(start_point)
            straight_path.lineTo(end_point)
            
            painter.setPen(QPen(QColor("#666666"), 1, Qt.DashLine))
            painter.drawPath(straight_path)
            
            # 绘制控制线（辅助线）
            painter.setPen(QPen(QColor("#0000FF"), 1, Qt.DotLine))
            painter.drawLine(start_point, control_point)
            painter.drawLine(control_point, end_point)
            
            # 标记点
            painter.setBrush(QColor("#00AA00"))
            painter.setPen(QPen(QColor("#00AA00"), 2))
            painter.drawEllipse(start_point, 6, 6)
            painter.drawEllipse(end_point, 6, 6)
            
            painter.setBrush(QColor("#0000FF"))
            painter.setPen(QPen(QColor("#0000FF"), 2))
            painter.drawEllipse(control_point, 8, 8)
            
            # 标注
            painter.setPen(QColor("#333333"))
            painter.drawText(start_point.x() - 30, start_point.y() - 10, "起点")
            painter.drawText(end_point.x() - 30, end_point.y() + 20, "终点")
            painter.drawText(control_point.x() + 10, control_point.y() - 10, "控制点")
            painter.drawText(120, 140, "━━━ 贝塞尔曲线")
            painter.drawText(120, 155, "--- 直线（对比）")
            painter.drawText(120, 170, "··· 控制线")
            
            # ========== 第二部分：梯形中的两个控制点 ==========
            painter.drawText(20, 280, "2. 弯曲梯形中的两个控制点:")
            
            # 梯形顶点
            top_left = QPointF(400, 320)
            top_right = QPointF(450, 320)
            bottom_left = QPointF(350, 420)
            bottom_right = QPointF(500, 420)
            
            # 计算控制点
            # 右腰控制点
            right_mid_x = (top_right.x() + bottom_right.x()) / 2
            right_mid_y = (top_right.y() + bottom_right.y()) / 2
            right_control = QPointF(right_mid_x + 50, right_mid_y)
            
            # 左腰控制点
            left_mid_x = (top_left.x() + bottom_left.x()) / 2
            left_mid_y = (top_left.y() + bottom_left.y()) / 2
            left_control = QPointF(left_mid_x + 50, left_mid_y)
            
            # 绘制梯形轮廓（直线版本，对比用）
            straight_trapezoid = QPainterPath()
            straight_trapezoid.moveTo(top_left)
            straight_trapezoid.lineTo(top_right)
            straight_trapezoid.lineTo(bottom_right)
            straight_trapezoid.lineTo(bottom_left)
            straight_trapezoid.lineTo(top_left)
            
            painter.setPen(QPen(QColor("#CCCCCC"), 1, Qt.DashLine))
            painter.drawPath(straight_trapezoid)
            
            # 绘制弯曲梯形
            curved_trapezoid = QPainterPath()
            curved_trapezoid.moveTo(top_left)
            curved_trapezoid.lineTo(top_right)                          # 上底
            curved_trapezoid.quadTo(right_control, bottom_right)        # 右腰（贝塞尔曲线）
            curved_trapezoid.lineTo(bottom_left)                        # 下底
            curved_trapezoid.quadTo(left_control, top_left)             # 左腰（贝塞尔曲线）
            curved_trapezoid.closeSubpath()
            
            painter.setBrush(QColor("#90EE90"))
            painter.setPen(QPen(QColor("#00AA00"), 2))
            painter.drawPath(curved_trapezoid)
            
            # 绘制控制线
            painter.setPen(QPen(QColor("#0000FF"), 1, Qt.DotLine))
            painter.drawLine(top_right, right_control)
            painter.drawLine(right_control, bottom_right)
            painter.drawLine(top_left, left_control)
            painter.drawLine(left_control, bottom_left)
            
            # 标记梯形顶点
            painter.setBrush(QColor("#FF0000"))
            painter.setPen(QPen(QColor("#FF0000"), 2))
            painter.drawEllipse(top_left, 4, 4)
            painter.drawEllipse(top_right, 4, 4)
            painter.drawEllipse(bottom_left, 4, 4)
            painter.drawEllipse(bottom_right, 4, 4)
            
            # 标记控制点
            painter.setBrush(QColor("#0000FF"))
            painter.setPen(QPen(QColor("#0000FF"), 2))
            painter.drawEllipse(right_control, 8, 8)
            painter.drawEllipse(left_control, 8, 8)
            
            # 标注
            painter.setPen(QColor("#333333"))
            painter.drawText(top_left.x() - 40, top_left.y() - 10, "上底左")
            painter.drawText(top_right.x() + 10, top_right.y() - 10, "上底右")
            painter.drawText(bottom_left.x() - 40, bottom_left.y() + 20, "下底左")
            painter.drawText(bottom_right.x() + 10, bottom_right.y() + 20, "下底右")
            
            painter.drawText(right_control.x() + 10, right_control.y() - 10, "right_control")
            painter.drawText(left_control.x() + 10, left_control.y() + 20, "left_control")
            
            # ========== 第三部分：控制点的作用解释 ==========
            painter.drawText(20, 480, "3. 控制点的作用:")
            painter.drawText(40, 500, "• right_control: 控制右腰线的弯曲方向和程度")
            painter.drawText(40, 520, "• left_control: 控制左腰线的弯曲方向和程度")
            painter.drawText(40, 540, "• 控制点不在曲线上，但决定曲线形状")
            painter.drawText(40, 560, "• 控制点越远离直线，曲线弯曲越明显")
            
            painter.drawText(400, 480, "4. 关键发现:")
            painter.drawText(420, 500, "• 两个控制点都向右偏移（一致性）")
            painter.drawText(420, 520, "• 这确保了填充算法的正确性")
            painter.drawText(420, 540, "• 避免了路径自相交问题")
            
        except Exception as e:
            print(f"绘图错误: {e}")
        finally:
            painter.end()


class ControlPointExplanationWindow(QMainWindow):
    """控制点解释主窗口"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("贝塞尔曲线控制点详细解释")
        self.setGeometry(100, 100, 850, 650)
        
        self.widget = ControlPointExplanationWidget()
        self.setCentralWidget(self.widget)


def main():
    """应用程序入口点"""
    app = QApplication(sys.argv)
    
    window = ControlPointExplanationWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()