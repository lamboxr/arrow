#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
方案3: 分段填充
解决弓形区域错误填充问题 - 将填充区域分解为多个简单多边形
"""

import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget
from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QPainter, QLinearGradient, QPen, QColor, QPainterPath, QPolygonF


# 渐变颜色定义 (来自原始gradient_trapezoid.py)
GRADIENT_COLORS = {
    'top': '#B6B384',      # 顶部颜色
    'middle': '#FEFFAF',   # 中间颜色
    'bottom': '#B7B286',   # 底部颜色
    'outline': '#B7B286'   # 轮廓颜色
}


class Solution3Widget(QWidget):
    """方案3: 分段填充Widget"""
    
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
    
    def get_bezier_points_on_curve(self, start_point, end_point, num_points=10):
        """获取贝塞尔曲线上的采样点"""
        # 计算控制点
        base_x = start_point.x() + (end_point.x() - start_point.x()) * self.position_ratio
        base_y = start_point.y() + (end_point.y() - start_point.y()) * self.position_ratio
        control_point = QPointF(base_x + self.curve_offset, base_y)
        
        points = []
        for i in range(num_points + 1):
            t = i / num_points
            # 二次贝塞尔曲线公式: B(t) = (1-t)²P₀ + 2(1-t)tP₁ + t²P₂
            x = (1-t)**2 * start_point.x() + 2*(1-t)*t * control_point.x() + t**2 * end_point.x()
            y = (1-t)**2 * start_point.y() + 2*(1-t)*t * control_point.y() + t**2 * end_point.y()
            points.append(QPointF(x, y))
        
        return points
    
    def create_core_trapezoid_segment(self, geometry):
        """创建核心梯形段（不包含弓形区域）"""
        # 获取贝塞尔曲线上的点
        left_curve_points = self.get_bezier_points_on_curve(
            geometry['top_left'], geometry['bottom_left'], 20
        )
        right_curve_points = self.get_bezier_points_on_curve(
            geometry['top_right'], geometry['bottom_right'], 20
        )
        
        # 创建核心区域多边形
        polygon_points = []
        
        # 添加上底
        polygon_points.append(geometry['top_left'])
        polygon_points.append(geometry['top_right'])
        
        # 添加右侧贝塞尔曲线点（从上到下）
        for point in right_curve_points[1:]:  # 跳过第一个点（重复）
            polygon_points.append(point)
        
        # 添加下底（从右到左）
        polygon_points.append(geometry['bottom_left'])
        
        # 添加左侧贝塞尔曲线点（从下到上）
        for point in reversed(left_curve_points[:-1]):  # 跳过最后一个点（重复）
            polygon_points.append(point)
        
        return QPolygonF(polygon_points)
    
    def create_right_curved_segment(self, geometry):
        """创建右侧弯曲段（右侧弓形区域）"""
        # 获取右侧贝塞尔曲线上的点
        right_curve_points = self.get_bezier_points_on_curve(
            geometry['top_right'], geometry['bottom_right'], 20
        )
        
        # 创建右侧弓形多边形
        polygon_points = []
        
        # 添加直线边（从上到下）
        polygon_points.append(geometry['top_right'])
        polygon_points.append(geometry['bottom_right'])
        
        # 添加贝塞尔曲线边（从下到上）
        for point in reversed(right_curve_points[:-1]):  # 跳过最后一个点（重复）
            polygon_points.append(point)
        
        return QPolygonF(polygon_points)
    
    def create_segmented_fill_paths(self, geometry):
        """方案3: 分段填充 - 将填充区域分解为多个简单多边形"""
        segments = []
        
        # 段1: 核心梯形区域（排除所有弓形）
        core_segment = self.create_core_trapezoid_segment(geometry)
        segments.append(('core', core_segment))
        
        # 段2: 右侧弯曲段（右侧弓形区域，需要包含）
        right_segment = self.create_right_curved_segment(geometry)
        segments.append(('right_bow', right_segment))
        
        # 注意：不包含左侧弓形段，因为它应该被排除
        
        return segments
    
    def paintEvent(self, event):
        """绘制方案3: 分段填充"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        
        try:
            # 0. 绘制背景色
            painter.fillRect(self.rect(), QColor("#BDC5D5"))
            
            # 1. 创建梯形几何
            geometry = self.create_trapezoid_geometry()
            
            # 2. 方案3: 分段填充
            segments = self.create_segmented_fill_paths(geometry)
            
            painter.setBrush(QColor("#CBD900"))  # 设置填充颜色
            painter.setPen(Qt.NoPen)  # 不绘制边框
            
            # 绘制每个段
            for segment_name, segment_polygon in segments:
                painter.drawPolygon(segment_polygon)
            
            # 3. 绘制弯曲梯形的渐变腰线 (在填充之上)
            left_control, right_control = self.draw_curved_trapezoid(painter, geometry)
            
            # 4. 绘制方案信息
            painter.setPen(QColor("#333333"))
            painter.drawText(20, 30, "方案3: 分段填充")
            painter.drawText(20, 50, "=" * 20)
            
            painter.drawText(20, 80, f"参数1 - 上底平移量: {self.top_offset:+.0f} 像素")
            painter.drawText(20, 100, f"参数2 - 控制点位置比例: {self.position_ratio:.2f}")
            painter.drawText(20, 120, f"参数3 - 横向偏移量: {self.curve_offset:+.0f} 像素")
            
            painter.drawText(20, 150, "解决方案: 分段填充")
            painter.drawText(20, 170, f"• 段数: {len(segments)}")
            painter.drawText(20, 190, "• 段1: 核心梯形区域")
            painter.drawText(20, 210, "• 段2: 右侧弯曲段")
            painter.drawText(20, 230, "• 排除: 左侧弓形区域")
            
            painter.drawText(20, 260, "技术实现:")
            painter.drawText(20, 280, "• 贝塞尔曲线采样点")
            painter.drawText(20, 300, "• 多边形分解")
            painter.drawText(20, 320, "• 精确控制每个区域")
            
        except Exception as e:
            print(f"绘图错误: {e}")
        finally:
            painter.end()


class Solution3Window(QMainWindow):
    """方案3主窗口"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("方案3: 分段填充 - 解决弓形填充问题")
        self.setGeometry(100, 100, 750, 600)
        
        # 创建并设置中心Widget
        self.trapezoid_widget = Solution3Widget()
        self.setCentralWidget(self.trapezoid_widget)


def main():
    """应用程序入口点"""
    app = QApplication(sys.argv)
    
    # 创建主窗口
    window = Solution3Window()
    window.show()
    
    # 运行应用程序
    sys.exit(app.exec())


if __name__ == "__main__":
    main()