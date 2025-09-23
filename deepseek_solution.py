import sys
import math
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, 
                               QVBoxLayout, QSlider, QLabel)
from PySide6.QtCore import Qt, QPointF, QTimer
from PySide6.QtGui import QPainter, QPainterPath, QColor, QPen, QBrush

class ARGuidanceWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.turn_offset = 0.0  # -1.0 到 1.0，负数为左转，正数为右转
        self.curve_intensity = 0.0  # 曲线强度
        self.setMinimumSize(800, 600)
        
    def set_turn_parameters(self, offset, intensity):
        """设置转向参数
        offset: 转向偏移量 (-1.0 到 1.0)
        intensity: 曲线强度 (0.0 到 1.0)
        """
        self.turn_offset = max(-1.0, min(1.0, offset))
        self.curve_intensity = max(0.0, min(1.0, intensity))
        self.update()
    
    def cubic_bezier(self, p0, p1, p2, p3, t):
        """计算三次贝塞尔曲线上的点"""
        u = 1 - t
        return (u**3 * p0 + 3 * u**2 * t * p1 + 
                3 * u * t**2 * p2 + t**3 * p3)
    
    def create_guidance_path(self):
        """创建引导区域路径 - 解决填充问题的关键"""
        width = self.width()
        height = self.height()
        
        # 梯形基本参数
        bottom_width = width * 0.8
        top_width = width * 0.4
        bottom_y = height * 0.9
        top_y = height * 0.4
        
        # 计算转向偏移
        max_offset = width * 0.3
        offset_x = self.turn_offset * max_offset
        
        # 底部点（固定）
        bottom_left = QPointF((width - bottom_width) / 2, bottom_y)
        bottom_right = QPointF((width + bottom_width) / 2, bottom_y)
        
        # 顶部点（根据转向偏移）
        top_center_x = width / 2 + offset_x
        top_left = QPointF(top_center_x - top_width / 2, top_y)
        top_right = QPointF(top_center_x + top_width / 2, top_y)
        
        path = QPainterPath()
        
        # 方法1：使用QPainterPath的贝塞尔曲线直接构建封闭区域
        # 这样可以避免弓形区域问题
        
        # 从底部左侧开始
        path.moveTo(bottom_left)
        
        # 右侧曲线
        if self.curve_intensity > 0:
            # 贝塞尔曲线控制点
            control1_right = QPointF(
                bottom_right.x() - self.curve_intensity * 100 * abs(self.turn_offset),
                bottom_right.y() - (top_y - bottom_y) * 0.3
            )
            control2_right = QPointF(
                top_right.x() - self.curve_intensity * 50 * abs(self.turn_offset),
                top_right.y() + (top_y - bottom_y) * 0.3
            )
            path.cubicTo(control1_right, control2_right, top_right)
        else:
            path.lineTo(top_right)
        
        # 顶部线
        path.lineTo(top_left)
        
        # 左侧曲线
        if self.curve_intensity > 0:
            control2_left = QPointF(
                top_left.x() + self.curve_intensity * 50 * abs(self.turn_offset),
                top_left.y() + (top_y - bottom_y) * 0.3
            )
            control1_left = QPointF(
                bottom_left.x() + self.curve_intensity * 100 * abs(self.turn_offset),
                bottom_left.y() - (top_y - bottom_y) * 0.3
            )
            path.cubicTo(control2_left, control1_left, bottom_left)
        else:
            path.lineTo(bottom_left)
        
        # 封闭路径
        path.closeSubpath()
        
        return path
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # 绘制背景（模拟道路）
        self.draw_road_background(painter)
        
        # 绘制引导区域
        self.draw_guidance_area(painter)
        
        # 绘制车道线等辅助元素
        self.draw_lane_markers(painter)
    
    def draw_road_background(self, painter):
        """绘制道路背景"""
        # 道路颜色
        road_color = QColor(50, 50, 50)
        painter.fillRect(self.rect(), road_color)
        
        # 中心线
        pen = QPen(QColor(255, 255, 255), 2, Qt.DashLine)
        painter.setPen(pen)
        center_y = self.height() * 0.7
        painter.drawLine(0, center_y, self.width(), center_y)
    
    def draw_guidance_area(self, painter):
        """绘制引导区域 - 使用路径填充避免弓形区域问题"""
        guidance_path = self.create_guidance_path()
        
        # 半透明填充
        fill_color = QColor(0, 150, 255, 100)  # 蓝色半透明
        painter.fillPath(guidance_path, QBrush(fill_color))
        
        # 边界线
        border_pen = QPen(QColor(255, 255, 0), 3)  # 黄色边界
        painter.setPen(border_pen)
        painter.drawPath(guidance_path)
    
    def draw_lane_markers(self, painter):
        """绘制车道标记"""
        pen = QPen(QColor(255, 255, 255), 2)
        painter.setPen(pen)
        
        width = self.width()
        height = self.height()
        
        # 车道边界
        lane_width = width * 0.3
        left_lane_x = width * 0.2
        right_lane_x = width * 0.8
        
        # 绘制虚线车道线
        dash_pattern = [10, 5]
        pen.setDashPattern(dash_pattern)
        painter.setPen(pen)
        
        for y in range(int(height * 0.1), int(height * 0.9), 20):
            painter.drawLine(left_lane_x, y, left_lane_x, y + 10)
            painter.drawLine(right_lane_x, y, right_lane_x, y + 10)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AR导航引导线演示")
        self.setGeometry(100, 100, 1000, 700)
        
        # 中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # AR引导显示区域
        self.ar_widget = ARGuidanceWidget()
        layout.addWidget(self.ar_widget)
        
        # 控制面板
        self.setup_controls(layout)
        
        # 自动演示定时器
        self.demo_timer = QTimer()
        self.demo_timer.timeout.connect(self.auto_demo)
        self.demo_timer.start(50)  # 20 FPS
        self.demo_progress = 0
        
    def setup_controls(self, layout):
        """设置控制滑块"""
        # 转向控制
        turn_layout = QVBoxLayout()
        turn_label = QLabel("转向控制: -1.0(左转) ←→ 1.0(右转)")
        turn_layout.addWidget(turn_label)
        
        self.turn_slider = QSlider(Qt.Horizontal)
        self.turn_slider.setRange(-100, 100)
        self.turn_slider.setValue(0)
        self.turn_slider.valueChanged.connect(self.on_slider_change)
        turn_layout.addWidget(self.turn_slider)
        
        # 曲线强度控制
        curve_layout = QVBoxLayout()
        curve_label = QLabel("曲线强度: 0.0(直线) ←→ 1.0(最大曲率)")
        curve_layout.addWidget(curve_label)
        
        self.curve_slider = QSlider(Qt.Horizontal)
        self.curve_slider.setRange(0, 100)
        self.curve_slider.setValue(50)
        self.curve_slider.valueChanged.connect(self.on_slider_change)
        curve_layout.addWidget(self.curve_slider)
        
        layout.addLayout(turn_layout)
        layout.addLayout(curve_layout)
    
    def on_slider_change(self):
        """滑块变化回调"""
        turn_value = self.turn_slider.value() / 100.0
        curve_value = self.curve_slider.value() / 100.0
        self.ar_widget.set_turn_parameters(turn_value, curve_value)
    
    def auto_demo(self):
        """自动演示"""
        self.demo_progress += 0.01
        if self.demo_progress > 2 * math.pi:
            self.demo_progress = 0
        
        # 正弦波模拟转向变化
        turn_value = math.sin(self.demo_progress)
        curve_value = abs(math.sin(self.demo_progress * 2)) * 0.8 + 0.2
        
        self.turn_slider.setValue(int(turn_value * 100))
        self.curve_slider.setValue(int(curve_value * 100))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())