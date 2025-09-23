#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
路径构建顺序对比测试
验证不同的路径构建顺序对填充结果的影响
"""

import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget
from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QPainter, QPen, QColor, QPainterPath


class PathOrderComparisonWidget(QWidget):
    """路径构建顺序对比Widget"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(1000, 700)
        self.setStyleSheet("background-color: #F0F0F0;")
    
    def get_common_geometry(self, offset_x=0, offset_y=0):
        """获取通用的梯形几何参数"""
        # 所有测试使用相同的几何参数，只是偏移位置
        top_left = QPointF(100 + offset_x, 80 + offset_y)
        top_right = QPointF(150 + offset_x, 80 + offset_y)
        bottom_left = QPointF(50 + offset_x, 180 + offset_y)
        bottom_right = QPointF(200 + offset_x, 180 + offset_y)
        
        # 控制点（都向右偏移，保持一致性）
        right_mid_x = (top_right.x() + bottom_right.x()) / 2
        right_mid_y = (top_right.y() + bottom_right.y()) / 2
        right_control = QPointF(right_mid_x + 40, right_mid_y)
        
        left_mid_x = (top_left.x() + bottom_left.x()) / 2
        left_mid_y = (top_left.y() + bottom_left.y()) / 2
        left_control = QPointF(left_mid_x + 40, left_mid_y)
        
        return {
            'vertices': [top_left, top_right, bottom_left, bottom_right],
            'controls': [right_control, left_control],
            'top_left': top_left,
            'top_right': top_right,
            'bottom_left': bottom_left,
            'bottom_right': bottom_right,
            'right_control': right_control,
            'left_control': left_control
        }
    
    def create_correct_order_path(self, geom):
        """
        正确顺序：上底→右腰→下底→左腰
        这是我们验证正确的构建顺序
        """
        path = QPainterPath()
        
        # 起点：上底左
        path.moveTo(geom['top_left'])
        
        # 1. 上底（直线）：上底左 → 上底右
        path.lineTo(geom['top_right'])
        
        # 2. 右腰（贝塞尔曲线）：上底右 → 下底右
        path.quadTo(geom['right_control'], geom['bottom_right'])
        
        # 3. 下底（直线）：下底右 → 下底左
        path.lineTo(geom['bottom_left'])
        
        # 4. 左腰（贝塞尔曲线）：下底左 → 上底左
        path.quadTo(geom['left_control'], geom['top_left'])
        
        path.closeSubpath()
        return path
    
    def create_reverse_order_path(self, geom):
        """
        反向顺序：上底→左腰→下底→右腰
        测试反向构建的效果
        """
        path = QPainterPath()
        
        # 起点：上底左
        path.moveTo(geom['top_left'])
        
        # 1. 上底（直线）：上底左 → 上底右
        path.lineTo(geom['top_right'])
        
        # 2. 左腰（贝塞尔曲线）：上底右 → 下底左（跨越式连接）
        path.quadTo(geom['left_control'], geom['bottom_left'])
        
        # 3. 下底（直线）：下底左 → 下底右
        path.lineTo(geom['bottom_right'])
        
        # 4. 右腰（贝塞尔曲线）：下底右 → 上底左（跨越式连接）
        path.quadTo(geom['right_control'], geom['top_left'])
        
        path.closeSubpath()
        return path
    
    def create_clockwise_order_path(self, geom):
        """
        顺时针顺序：上底→右腰→下底→左腰（但方向相反）
        测试顺时针构建的效果
        """
        path = QPainterPath()
        
        # 起点：上底右（从右开始）
        path.moveTo(geom['top_right'])
        
        # 1. 上底（直线）：上底右 → 上底左（反向）
        path.lineTo(geom['top_left'])
        
        # 2. 左腰（贝塞尔曲线）：上底左 → 下底左
        path.quadTo(geom['left_control'], geom['bottom_left'])
        
        # 3. 下底（直线）：下底左 → 下底右
        path.lineTo(geom['bottom_right'])
        
        # 4. 右腰（贝塞尔曲线）：下底右 → 上底右
        path.quadTo(geom['right_control'], geom['top_right'])
        
        path.closeSubpath()
        return path
    
    def create_random_order_path(self, geom):
        """
        随机顺序：左腰→上底→右腰→下底
        测试完全随机顺序的效果
        """
        path = QPainterPath()
        
        # 起点：上底左
        path.moveTo(geom['top_left'])
        
        # 1. 左腰（贝塞尔曲线）：上底左 → 下底左
        path.quadTo(geom['left_control'], geom['bottom_left'])
        
        # 2. 上底（直线）：下底左 → 上底右（跨越式连接）
        path.lineTo(geom['top_right'])
        
        # 3. 右腰（贝塞尔曲线）：上底右 → 下底右
        path.quadTo(geom['right_control'], geom['bottom_right'])
        
        # 4. 下底（直线）：下底右 → 上底左（跨越式连接）
        path.lineTo(geom['top_left'])
        
        path.closeSubpath()
        return path
    
    def draw_trapezoid_with_info(self, painter, geom, path, title, color, x_offset, y_offset):
        """绘制梯形并添加信息标注"""
        painter.save()
        
        # 偏移坐标系
        painter.translate(x_offset, y_offset)
        
        # 绘制填充
        painter.setBrush(QColor(color))
        painter.setPen(QPen(QColor("#333333"), 2))
        painter.drawPath(path)
        
        # 绘制顶点
        painter.setBrush(QColor("#FF0000"))
        painter.setPen(QPen(QColor("#FF0000"), 2))
        for vertex in geom['vertices']:
            painter.drawEllipse(vertex, 3, 3)
        
        # 绘制控制点
        painter.setBrush(QColor("#0000FF"))
        painter.setPen(QPen(QColor("#0000FF"), 2))
        for control in geom['controls']:
            painter.drawEllipse(control, 4, 4)
        
        # 绘制标题
        painter.setPen(QColor("#333333"))
        painter.drawText(20, -10, title)
        
        painter.restore()
    
    def paintEvent(self, event):
        """绘制路径构建顺序对比"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        
        try:
            # 背景
            painter.fillRect(self.rect(), QColor("#F0F0F0"))
            
            # 标题
            painter.setPen(QColor("#333333"))
            painter.drawText(20, 30, "路径构建顺序对填充结果的影响对比")
            painter.drawText(20, 50, "=" * 60)
            
            # 测试1：正确顺序（左上）
            geom1 = self.get_common_geometry()
            path1 = self.create_correct_order_path(geom1)
            self.draw_trapezoid_with_info(
                painter, geom1, path1, 
                "✅ 正确顺序：上底→右腰→下底→左腰", 
                "#90EE90", 0, 100
            )
            
            # 测试2：反向顺序（右上）
            geom2 = self.get_common_geometry()
            path2 = self.create_reverse_order_path(geom2)
            self.draw_trapezoid_with_info(
                painter, geom2, path2, 
                "❌ 反向顺序：上底→左腰→下底→右腰", 
                "#FFB6C1", 400, 100
            )
            
            # 测试3：顺时针顺序（左下）
            geom3 = self.get_common_geometry()
            path3 = self.create_clockwise_order_path(geom3)
            self.draw_trapezoid_with_info(
                painter, geom3, path3, 
                "🔄 顺时针：上底(反)→左腰→下底→右腰", 
                "#FFD700", 0, 350
            )
            
            # 测试4：随机顺序（右下）
            geom4 = self.get_common_geometry()
            path4 = self.create_random_order_path(geom4)
            self.draw_trapezoid_with_info(
                painter, geom4, path4, 
                "🎲 随机顺序：左腰→上底→右腰→下底", 
                "#DDA0DD", 400, 350
            )
            
            # 说明文字
            painter.setPen(QColor("#333333"))
            painter.drawText(20, 580, "观察要点:")
            painter.drawText(20, 600, "🔴 红点: 梯形顶点    🔵 蓝点: 贝塞尔控制点")
            painter.drawText(20, 620, "• 注意不同构建顺序产生的填充区域差异")
            painter.drawText(20, 640, "• 观察是否出现自相交、意外填充或填充缺失")
            painter.drawText(20, 660, "• 所有测试使用相同的顶点和控制点坐标")
            
            # 技术说明
            painter.drawText(600, 580, "技术分析:")
            painter.drawText(600, 600, "• 路径构建顺序影响Qt的填充算法")
            painter.drawText(600, 620, "• 跨越式连接可能导致路径自相交")
            painter.drawText(600, 640, "• 正确顺序确保路径的简单性")
            painter.drawText(600, 660, "• 简单路径 = 可预测的填充结果")
            
        except Exception as e:
            print(f"绘图错误: {e}")
        finally:
            painter.end()


class PathOrderComparisonWindow(QMainWindow):
    """路径构建顺序对比主窗口"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("路径构建顺序对填充结果的影响对比")
        self.setGeometry(100, 100, 1050, 750)
        
        self.widget = PathOrderComparisonWidget()
        self.setCentralWidget(self.widget)


def main():
    """应用程序入口点"""
    app = QApplication(sys.argv)
    
    window = PathOrderComparisonWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()