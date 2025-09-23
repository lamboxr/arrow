#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Qt贝塞尔曲线填充特性测试
验证PySide6处理贝塞尔曲线填充的行为
"""

import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget
from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QPainter, QPen, QColor, QPainterPath


class BezierFillTestWidget(QWidget):
    """贝塞尔曲线填充测试Widget"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(800, 600)
        self.setStyleSheet("background-color: #F0F0F0;")
    
    def create_simple_bow_path(self, start_x, start_y, end_x, end_y, control_offset):
        """创建简单的弓形路径"""
        path = QPainterPath()
        
        start_point = QPointF(start_x, start_y)
        end_point = QPointF(end_x, end_y)
        
        # 控制点在中点右侧偏移
        mid_x = (start_x + end_x) / 2
        mid_y = (start_y + end_y) / 2
        control_point = QPointF(mid_x + control_offset, mid_y)
        
        path.moveTo(start_point)
        path.quadTo(control_point, end_point)
        path.lineTo(start_point)  # 直线返回
        path.closeSubpath()
        
        return path, control_point
    
    def paintEvent(self, event):
        """绘制贝塞尔曲线填充测试"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        
        try:
            # 背景
            painter.fillRect(self.rect(), QColor("#F0F0F0"))
            
            # 测试1: 简单右弯弓形 - 小偏移
            path1, control1 = self.create_simple_bow_path(100, 100, 100, 200, 30)
            painter.setBrush(QColor("#FF6B6B"))
            painter.setPen(QPen(QColor("#FF0000"), 2))
            painter.drawPath(path1)
            
            # 测试2: 简单右弯弓形 - 大偏移
            path2, control2 = self.create_simple_bow_path(200, 100, 200, 200, 100)
            painter.setBrush(QColor("#90EE90"))
            painter.setPen(QPen(QColor("#00AA00"), 2))
            painter.drawPath(path2)
            
            # 测试3: 左弯弓形 - 负偏移
            path3, control3 = self.create_simple_bow_path(300, 100, 300, 200, -50)
            painter.setBrush(QColor("#6B9BFF"))
            painter.setPen(QPen(QColor("#0000FF"), 2))
            painter.drawPath(path3)
            
            # 测试4: 不同填充规则
            path4, control4 = self.create_simple_bow_path(400, 100, 400, 200, 80)
            path4.setFillRule(Qt.OddEvenFill)  # 奇偶填充规则
            painter.setBrush(QColor("#FFB66B"))
            painter.setPen(QPen(QColor("#FF8800"), 2))
            painter.drawPath(path4)
            
            path5, control5 = self.create_simple_bow_path(500, 100, 500, 200, 80)
            path5.setFillRule(Qt.WindingFill)  # 缠绕填充规则
            painter.setBrush(QColor("#B66BFF"))
            painter.setPen(QPen(QColor("#8800FF"), 2))
            painter.drawPath(path5)
            
            # 标记控制点
            painter.setBrush(QColor("#000000"))
            painter.setPen(QPen(QColor("#000000"), 2))
            for control in [control1, control2, control3, control4, control5]:
                painter.drawEllipse(control, 4, 4)
            
            # 说明文字
            painter.setPen(QColor("#333333"))
            painter.drawText(20, 30, "Qt贝塞尔曲线填充特性测试")
            painter.drawText(20, 50, "=" * 40)
            
            painter.drawText(80, 250, "小偏移\n(30px)")
            painter.drawText(180, 250, "大偏移\n(100px)")
            painter.drawText(280, 250, "左弯\n(-50px)")
            painter.drawText(380, 250, "奇偶填充\n(80px)")
            painter.drawText(480, 250, "缠绕填充\n(80px)")
            
            # 测试6: 复杂路径 - 模拟我们的梯形情况
            painter.drawText(20, 320, "复杂路径测试 - 模拟梯形情况:")
            
            # 创建类似我们梯形的路径
            complex_path = QPainterPath()
            
            # 上底
            complex_path.moveTo(QPointF(100, 350))
            complex_path.lineTo(QPointF(130, 350))
            
            # 右腰 - 贝塞尔曲线
            right_control = QPointF(180, 400)
            complex_path.quadTo(right_control, QPointF(200, 450))
            
            # 下底
            complex_path.lineTo(QPointF(50, 450))
            
            # 左腰 - 贝塞尔曲线
            left_control = QPointF(100, 400)
            complex_path.quadTo(left_control, QPointF(100, 350))
            
            complex_path.closeSubpath()
            
            painter.setBrush(QColor("#FFFF6B"))
            painter.setPen(QPen(QColor("#FFAA00"), 2))
            painter.drawPath(complex_path)
            
            # 标记控制点
            painter.setBrush(QColor("#FF0000"))
            painter.drawEllipse(right_control, 4, 4)
            painter.drawEllipse(left_control, 4, 4)
            
            painter.setPen(QColor("#333333"))
            painter.drawText(20, 480, "观察: 复杂路径是否产生意外填充?")
            painter.drawText(20, 500, "• 黄色区域应该只在路径内部")
            painter.drawText(20, 520, "• 红点标记贝塞尔控制点")
            painter.drawText(20, 540, "• 检查是否有超出预期的填充区域")
            
        except Exception as e:
            print(f"绘图错误: {e}")
        finally:
            painter.end()


class BezierFillTestWindow(QMainWindow):
    """贝塞尔曲线填充测试主窗口"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Qt贝塞尔曲线填充特性测试")
        self.setGeometry(100, 100, 850, 650)
        
        self.widget = BezierFillTestWidget()
        self.setCentralWidget(self.widget)


def main():
    """应用程序入口点"""
    app = QApplication(sys.argv)
    
    window = BezierFillTestWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()