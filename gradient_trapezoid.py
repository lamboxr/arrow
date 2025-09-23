#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
渐变梯形绘制应用程序
使用PySide6实现具有特定渐变效果和轮廓样式的等腰梯形
"""

import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QLinearGradient, QPen, QPolygonF, QColor, QPainterPath
from PySide6.QtCore import QPointF


# 颜色定义
COLORS = {
    'top': '#B6B384',      # 顶部颜色
    'middle': '#FEFFAF',   # 中间颜色
    'bottom': '#B7B286',   # 底部颜色
    'outline': '#B7B286'   # 轮廓颜色
}

# 尺寸参数
DIMENSIONS = {
    'height': 300,
    'top_base': 30,
    'bottom_base': 500,
    'outline_width': 2
}

# 弯曲参数
CURVE_PARAMETERS = {
    'left_offset': 300,        # 上底左移距离（像素）
    'curve_intensity': 0.6,    # 弯曲强度系数
    'control_point_ratio': 0.4 # 控制点偏移比例
}


class TrapezoidWidget(QWidget):
    """自定义梯形Widget类"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        # 初始化尺寸参数
        self.trapezoid_height = DIMENSIONS['height']
        self.top_base = DIMENSIONS['top_base']
        self.bottom_base = DIMENSIONS['bottom_base']
        self.outline_width = DIMENSIONS['outline_width']
        
        # 初始化弯曲参数
        self.left_offset = CURVE_PARAMETERS['left_offset']
        self.curve_intensity = CURVE_PARAMETERS['curve_intensity']
        self.control_point_ratio = CURVE_PARAMETERS['control_point_ratio']
        
        # 设置Widget最小尺寸以容纳梯形
        self.setMinimumSize(self.bottom_base + 50, self.trapezoid_height + 50)
        
        # 设置Widget背景色
        self.setStyleSheet("background-color: #BDC5D5;")
        
        # 验证尺寸参数
        self._validate_dimensions()
    
    def _validate_dimensions(self):
        """验证梯形尺寸参数的有效性"""
        if self.trapezoid_height <= 0:
            raise ValueError(f"梯形高度必须为正数，当前值: {self.trapezoid_height}")
        if self.top_base <= 0:
            raise ValueError(f"上底长度必须为正数，当前值: {self.top_base}")
        if self.bottom_base <= 0:
            raise ValueError(f"下底长度必须为正数，当前值: {self.bottom_base}")
        if self.top_base >= self.bottom_base:
            raise ValueError(f"上底({self.top_base})必须小于下底({self.bottom_base})")
        if self.outline_width <= 0:
            raise ValueError(f"轮廓线宽度必须为正数，当前值: {self.outline_width}")
    
    def _create_trapezoid_polygon(self):
        """创建弯曲梯形的关键点坐标
        
        Returns:
            dict: 包含梯形关键点的字典
        """
        # 计算Widget中心点
        widget_width = self.width()
        widget_height = self.height()
        
        # 计算梯形在Widget中的居中位置
        center_x = widget_width / 2
        start_y = (widget_height - self.trapezoid_height) / 2
        
        # 计算弯曲后的上底位置（向左移动200像素）
        curved_center_x = center_x - self.left_offset
        
        # 计算上底的左右端点（弯曲后）
        top_left_x = curved_center_x - self.top_base / 2
        top_right_x = curved_center_x + self.top_base / 2
        top_y = start_y
        
        # 下底保持原位置不变
        bottom_left_x = center_x - self.bottom_base / 2
        bottom_right_x = center_x + self.bottom_base / 2
        bottom_y = start_y + self.trapezoid_height
        
        # 返回关键点字典
        return {
            'top_left': QPointF(top_left_x, top_y),
            'top_right': QPointF(top_right_x, top_y),
            'bottom_left': QPointF(bottom_left_x, bottom_y),
            'bottom_right': QPointF(bottom_right_x, bottom_y)
        }
    
    def _create_gradient(self):
        """创建渐变填充
        
        Returns:
            QLinearGradient: 配置好的线性渐变对象
        """
        # 计算梯形在Widget中的位置
        widget_height = self.height()
        start_y = (widget_height - self.trapezoid_height) / 2
        
        # 创建垂直线性渐变
        gradient = QLinearGradient(0, start_y, 0, start_y + self.trapezoid_height)
        
        # 设置渐变颜色点
        # 顶部：#B6B384，完全透明（alpha=0）
        top_color = QColor(COLORS['top'])
        top_color.setAlpha(0)  # 完全透明
        gradient.setColorAt(0.0, top_color)
        
        # 中间（50%高度）：#FEFFAF，50%透明（alpha=127）
        middle_color = QColor(COLORS['middle'])
        middle_color.setAlpha(127)  # 50%透明
        gradient.setColorAt(0.5, middle_color)
        
        # 底部：#B7B286，完全透明（alpha=0）
        bottom_color = QColor(COLORS['bottom'])
        bottom_color.setAlpha(0)  # 完全透明
        gradient.setColorAt(1.0, bottom_color)
        
        return gradient
    
    def _create_curved_path(self, start_point, end_point):
        """创建贝塞尔曲线路径
        
        Args:
            start_point (QPointF): 曲线起点
            end_point (QPointF): 曲线终点
            
        Returns:
            QPainterPath: 贝塞尔曲线路径
        """
        # 创建路径对象
        path = QPainterPath()
        
        # 移动到起点
        path.moveTo(start_point)
        
        # 计算控制点位置（实现向右凸起）
        # 控制点在直线中点的右侧
        mid_x = (start_point.x() + end_point.x()) / 2
        mid_y = (start_point.y() + end_point.y()) / 2
        
        # 计算向右的偏移量
        offset_x = self.curve_intensity * self.trapezoid_height * self.control_point_ratio
        
        # 控制点位置
        control_point = QPointF(mid_x + offset_x, mid_y)
        
        # 创建二次贝塞尔曲线
        path.quadTo(control_point, end_point)
        
        return path
    
    def _setup_outline_pen(self):
        """设置轮廓线样式
        
        Returns:
            QPen: 配置好的画笔对象
        """
        # 创建画笔
        pen = QPen()
        
        # 设置轮廓线颜色为#B7B286
        outline_color = QColor(COLORS['outline'])
        pen.setColor(outline_color)
        
        # 设置线宽为2像素
        pen.setWidth(self.outline_width)
        
        # 设置线条样式为实线
        pen.setStyle(Qt.SolidLine)
        
        # 设置线条端点样式
        pen.setCapStyle(Qt.RoundCap)
        
        # 设置线条连接样式
        pen.setJoinStyle(Qt.RoundJoin)
        
        return pen
    
    def _create_line_gradient(self, start_point, end_point):
        """为腰线创建渐变（支持曲线路径）
        
        Args:
            start_point (QPointF): 腰线起点
            end_point (QPointF): 腰线终点
            
        Returns:
            QLinearGradient: 沿腰线方向的渐变
        """
        # 对于曲线路径，我们仍然使用起点到终点的线性渐变
        # 这样渐变会沿着曲线的整体方向分布
        gradient = QLinearGradient(start_point, end_point)
        
        # 设置渐变颜色点
        # 起点（上端）：#B6B384，完全透明（alpha=0）
        top_color = QColor(COLORS['top'])
        top_color.setAlpha(0)  # 完全透明
        gradient.setColorAt(0.0, top_color)
        
        # 中间（50%）：#FEFFAF，50%透明（alpha=127）
        middle_color = QColor(COLORS['middle'])
        middle_color.setAlpha(127)  # 50%透明
        gradient.setColorAt(0.5, middle_color)
        
        # 终点（下端）：#B7B286，完全透明（alpha=0）
        bottom_color = QColor(COLORS['bottom'])
        bottom_color.setAlpha(0)  # 完全透明
        gradient.setColorAt(1.0, bottom_color)
        
        return gradient
    
    def _draw_trapezoid_outline(self, painter, geometry):
        """绘制弯曲梯形轮廓线（只绘制左右两条腰边，带渐变效果）
        
        Args:
            painter (QPainter): 画笔对象
            geometry (dict): 梯形几何关键点
        """
        # 获取梯形的关键点
        top_left = geometry['top_left']
        top_right = geometry['top_right']
        bottom_left = geometry['bottom_left']
        bottom_right = geometry['bottom_right']
        
        # 绘制左腰线（弯曲，带渐变）
        left_path = self._create_curved_path(top_left, bottom_left)
        left_gradient = self._create_line_gradient(top_left, bottom_left)
        left_pen = QPen()
        left_pen.setBrush(left_gradient)
        left_pen.setWidth(self.outline_width)
        left_pen.setCapStyle(Qt.RoundCap)
        painter.setPen(left_pen)
        painter.drawPath(left_path)
        
        # 绘制右腰线（弯曲，带渐变）
        right_path = self._create_curved_path(top_right, bottom_right)
        right_gradient = self._create_line_gradient(top_right, bottom_right)
        right_pen = QPen()
        right_pen.setBrush(right_gradient)
        right_pen.setWidth(self.outline_width)
        right_pen.setCapStyle(Qt.RoundCap)
        painter.setPen(right_pen)
        painter.drawPath(right_path)
    
    def paintEvent(self, event):
        """重写paintEvent方法实现弯曲梯形绘图
        
        Args:
            event: 绘图事件对象
        """
        # 创建画笔对象
        painter = QPainter(self)
        
        try:
            # 启用抗锯齿以获得更平滑的效果
            painter.setRenderHint(QPainter.Antialiasing, True)
            
            # 1. 创建弯曲梯形几何形状
            geometry = self._create_trapezoid_polygon()
            
            # 2. 绘制带渐变的弯曲腰线（只有左右两条腰边）
            self._draw_trapezoid_outline(painter, geometry)
            
        except Exception as e:
            # 错误处理：在控制台输出错误信息
            print(f"绘图过程中发生错误: {e}")
            
        finally:
            # 确保画笔对象被正确释放
            painter.end()


class MainWindow(QMainWindow):
    """主窗口类"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("渐变梯形绘制器")
        self.setGeometry(100, 100, 600, 400)
        
        # 设置主窗口背景色
        self.setStyleSheet("QMainWindow { background-color: #BDC5D5; }")
        
        # 创建并设置中心Widget
        self.trapezoid_widget = TrapezoidWidget()
        self.setCentralWidget(self.trapezoid_widget)


def main():
    """应用程序入口点"""
    app = QApplication(sys.argv)
    
    # 创建主窗口
    window = MainWindow()
    window.show()
    
    # 运行应用程序
    sys.exit(app.exec())


if __name__ == "__main__":
    main()