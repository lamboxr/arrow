#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
船舶转向引导系统
使用贝塞尔曲线梯形表示转弯程度和方向
"""

import sys
import math
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                               QHBoxLayout, QLabel, QSlider, QComboBox)
from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QPainter, QLinearGradient, QPen, QColor, QPainterPath


class ShipSteeringWidget(QWidget):
    """船舶转向引导Widget"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # 船舶转向参数 (最优化配置)
        self.rudder_angle = 0        # 舵角 (-30° 到 +30°)
        self.turn_intensity = 1.0    # 转弯强度 (0.0 到 2.0)
        self.ship_speed = 10         # 船速 (节)
        
        # 固定的显示参数
        self.display_width = 400
        self.display_height = 300
        self.trapezoid_height = 200
        self.trapezoid_top = 20
        self.trapezoid_bottom = 200
        
        self.setFixedSize(500, 400)
        self.setStyleSheet("background-color: #001122; border: 2px solid #336699;")  # 海洋色调
    
    def set_steering_parameters(self, rudder_angle, turn_intensity, ship_speed):
        """设置船舶转向参数"""
        self.rudder_angle = rudder_angle
        self.turn_intensity = turn_intensity
        self.ship_speed = ship_speed
        self.update()
    
    def calculate_turn_parameters(self):
        """根据船舶参数计算转弯参数"""
        # 1. 计算转向偏移 (基于舵角和船速)
        # 物理原理：
        # - 舵角越大，转向意图越强
        # - 船速越快，转弯半径越大，转向越困难
        # - 高速时相同舵角产生的弯曲效果应该更小
        max_offset = 150  # 最大偏移像素
        
        # 舵角影响 (-30° 到 +30° 映射到 -1.0 到 +1.0)
        angle_factor = self.rudder_angle / 30.0
        
        # 船速影响 (速度越快，转弯越困难，偏移量应该降低)
        # 使用反比关系：速度越快，转向能力越弱
        speed_factor = 10.0 / self.ship_speed  # 反比关系，速度快时因子小
        
        # 转弯强度影响
        intensity_factor = self.turn_intensity
        
        # 最终偏移计算
        lateral_offset = angle_factor * max_offset * intensity_factor
        curve_offset = abs(angle_factor) * speed_factor * intensity_factor * 50
        
        return lateral_offset, curve_offset
    
    def create_ship_trapezoid(self):
        """创建船舶转向梯形"""
        lateral_offset, curve_offset = self.calculate_turn_parameters()
        
        # 计算梯形基础位置
        center_x = self.width() / 2
        start_y = (self.height() - self.trapezoid_height) / 2
        
        # 上底位置 (根据舵角偏移)
        top_center_x = center_x + lateral_offset
        top_left_x = top_center_x - self.trapezoid_top / 2
        top_right_x = top_center_x + self.trapezoid_top / 2
        top_y = start_y
        
        # 下底位置 (保持居中，代表船舶当前位置)
        bottom_left_x = center_x - self.trapezoid_bottom / 2
        bottom_right_x = center_x + self.trapezoid_bottom / 2
        bottom_y = start_y + self.trapezoid_height
        
        return {
            'top_left': QPointF(top_left_x, top_y),
            'top_right': QPointF(top_right_x, top_y),
            'bottom_left': QPointF(bottom_left_x, bottom_y),
            'bottom_right': QPointF(bottom_right_x, bottom_y),
            'curve_offset': curve_offset
        }
    
    def create_steering_curve(self, start_point, end_point, curve_offset):
        """创建转向曲线"""
        path = QPainterPath()
        path.moveTo(start_point)
        
        # 计算控制点
        mid_x = (start_point.x() + end_point.x()) / 2
        mid_y = (start_point.y() + end_point.y()) / 2
        
        # 根据转向方向确定控制点偏移方向
        # 颠倒偏移量正负值：右舵 → 向左弯曲，左舵 → 向右弯曲
        if self.rudder_angle > 0:  # 右舵 → 向左弯曲
            control_point = QPointF(mid_x - curve_offset, mid_y)
        elif self.rudder_angle < 0:  # 左舵 → 向右弯曲
            control_point = QPointF(mid_x + curve_offset, mid_y)
        else:  # 直航
            control_point = QPointF(mid_x, mid_y)
        
        path.quadTo(control_point, end_point)
        return path
    
    def get_steering_gradient(self, start_point, end_point):
        """获取转向强度渐变"""
        gradient = QLinearGradient(start_point, end_point)
        
        # 根据转向紧急程度调整颜色
        urgency = abs(self.rudder_angle) / 30.0  # 0.0 到 1.0
        
        if urgency < 0.3:  # 轻微转向 - 绿色
            top_color = QColor("#00FF88")
            middle_color = QColor("#88FFAA") 
            bottom_color = QColor("#00FF88")
        elif urgency < 0.7:  # 中等转向 - 黄色
            top_color = QColor("#FFAA00")
            middle_color = QColor("#FFDD88")
            bottom_color = QColor("#FFAA00")
        else:  # 急转 - 红色
            top_color = QColor("#FF4444")
            middle_color = QColor("#FF8888")
            bottom_color = QColor("#FF4444")
        
        # 设置透明度
        top_color.setAlpha(150)
        middle_color.setAlpha(220)
        bottom_color.setAlpha(150)
        
        gradient.setColorAt(0.0, top_color)
        gradient.setColorAt(0.5, middle_color)
        gradient.setColorAt(1.0, bottom_color)
        
        return gradient
    
    def paintEvent(self, event):
        """绘制船舶转向引导"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        
        try:
            # 创建船舶转向梯形
            trapezoid = self.create_ship_trapezoid()
            
            # 绘制左舷转向线
            left_path = self.create_steering_curve(
                trapezoid['top_left'], 
                trapezoid['bottom_left'], 
                trapezoid['curve_offset']
            )
            left_gradient = self.get_steering_gradient(
                trapezoid['top_left'], 
                trapezoid['bottom_left']
            )
            
            left_pen = QPen()
            left_pen.setBrush(left_gradient)
            left_pen.setWidth(4)
            left_pen.setCapStyle(Qt.RoundCap)
            painter.setPen(left_pen)
            painter.drawPath(left_path)
            
            # 绘制右舷转向线
            right_path = self.create_steering_curve(
                trapezoid['top_right'], 
                trapezoid['bottom_right'], 
                trapezoid['curve_offset']
            )
            right_gradient = self.get_steering_gradient(
                trapezoid['top_right'], 
                trapezoid['bottom_right']
            )
            
            right_pen = QPen()
            right_pen.setBrush(right_gradient)
            right_pen.setWidth(4)
            right_pen.setCapStyle(Qt.RoundCap)
            painter.setPen(right_pen)
            painter.drawPath(right_path)
            
            # 绘制船舶位置指示器 (下底中心)
            ship_center = QPointF(self.width() / 2, 
                                (self.height() + self.trapezoid_height) / 2)
            painter.setPen(QPen(QColor("#FFFFFF"), 3))
            painter.setBrush(QColor("#FFFF00"))
            painter.drawEllipse(ship_center, 8, 8)
            
            # 绘制转向信息
            painter.setPen(QColor("#FFFFFF"))
            painter.drawText(10, 30, f"舵角: {self.rudder_angle:+.1f}°")
            painter.drawText(10, 50, f"转弯强度: {self.turn_intensity:.1f}")
            painter.drawText(10, 70, f"船速: {self.ship_speed:.1f} 节")
            
            # 转向方向指示
            if abs(self.rudder_angle) > 1:
                direction = "右转" if self.rudder_angle > 0 else "左转"
                urgency = "急转" if abs(self.rudder_angle) > 20 else "缓转"
                painter.drawText(10, 100, f"转向: {direction} ({urgency})")
            else:
                painter.drawText(10, 100, "转向: 直航")
            
            # 绘制转弯半径估算
            if abs(self.rudder_angle) > 1:
                # 简化的转弯半径计算 (实际应用中需要更复杂的船舶动力学模型)
                turn_radius = (self.ship_speed * 10) / abs(self.rudder_angle)
                painter.drawText(10, 120, f"转弯半径: ~{turn_radius:.0f}m")
            
        except Exception as e:
            print(f"绘图错误: {e}")
        finally:
            painter.end()


class ShipSteeringWindow(QMainWindow):
    """船舶转向引导主窗口"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("船舶转向引导系统 - 贝塞尔曲线转向指示")
        self.setGeometry(100, 100, 800, 600)
        
        # 创建中心Widget和布局
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # 添加标题
        title = QLabel("🚢 船舶转向引导系统")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold; margin: 10px; color: #003366;")
        layout.addWidget(title)
        
        # 创建转向显示Widget
        self.steering_widget = ShipSteeringWidget()
        layout.addWidget(self.steering_widget)
        
        # 创建控制面板
        controls_layout = QHBoxLayout()
        
        # 舵角控制
        rudder_layout = QVBoxLayout()
        rudder_layout.addWidget(QLabel("舵角 (°):"))
        self.rudder_slider = QSlider(Qt.Horizontal)
        self.rudder_slider.setRange(-300, 300)  # -30.0° 到 +30.0°
        self.rudder_slider.setValue(0)
        self.rudder_label = QLabel("0.0°")
        rudder_layout.addWidget(self.rudder_slider)
        rudder_layout.addWidget(self.rudder_label)
        controls_layout.addLayout(rudder_layout)
        
        # 转弯强度控制
        intensity_layout = QVBoxLayout()
        intensity_layout.addWidget(QLabel("转弯强度:"))
        self.intensity_slider = QSlider(Qt.Horizontal)
        self.intensity_slider.setRange(0, 200)  # 0.0 到 2.0
        self.intensity_slider.setValue(100)
        self.intensity_label = QLabel("1.0")
        intensity_layout.addWidget(self.intensity_slider)
        intensity_layout.addWidget(self.intensity_label)
        controls_layout.addLayout(intensity_layout)
        
        # 船速控制
        speed_layout = QVBoxLayout()
        speed_layout.addWidget(QLabel("船速 (节):"))
        self.speed_slider = QSlider(Qt.Horizontal)
        self.speed_slider.setRange(1, 30)  # 1到30节
        self.speed_slider.setValue(10)
        self.speed_label = QLabel("10 节")
        speed_layout.addWidget(self.speed_slider)
        speed_layout.addWidget(self.speed_label)
        controls_layout.addLayout(speed_layout)
        
        layout.addLayout(controls_layout)
        
        # 连接事件
        self.rudder_slider.valueChanged.connect(self.update_steering)
        self.intensity_slider.valueChanged.connect(self.update_steering)
        self.speed_slider.valueChanged.connect(self.update_steering)
        
        # 添加说明
        info_text = """
🚢 船舶转向引导系统说明:

📐 参数配置 (仅3个核心参数):
• 舵角 (-30° 到 +30°): 控制转向方向和程度
• 转弯强度 (0.0 到 2.0): 控制转弯的紧急程度
• 船速 (1 到 30节): 影响转弯半径和响应

🎯 视觉指示:
• 绿色: 轻微转向 (舵角 < 9°)
• 黄色: 中等转向 (舵角 9° - 21°)  
• 红色: 急转 (舵角 > 21°)
• 弯曲程度: 反映转弯的紧急程度和船舶响应

⚓ 应用优势:
• 参数最少: 只需3个核心参数
• 直观显示: 贝塞尔曲线直观表示转向轨迹
• 实时响应: 参数变化立即反映在视觉上
• 符合直觉: 弯曲方向和程度符合船员的操作直觉

💡 实际应用:
• 船桥导航显示
• 自动驾驶系统界面
• 船舶操纵训练模拟器
• 港口引航辅助系统
        """
        
        info_label = QLabel(info_text)
        info_label.setStyleSheet(
            "margin: 10px; padding: 10px; "
            "background-color: #F0F8FF; border: 1px solid #B0C4DE; "
            "border-radius: 5px; font-size: 9px;"
        )
        layout.addWidget(info_label)
    
    def update_steering(self):
        """更新转向参数"""
        rudder_angle = self.rudder_slider.value() / 10.0  # 转换为度数
        turn_intensity = self.intensity_slider.value() / 100.0
        ship_speed = self.speed_slider.value()
        
        # 更新标签
        self.rudder_label.setText(f"{rudder_angle:+.1f}°")
        self.intensity_label.setText(f"{turn_intensity:.1f}")
        self.speed_label.setText(f"{ship_speed} 节")
        
        # 更新显示
        self.steering_widget.set_steering_parameters(rudder_angle, turn_intensity, ship_speed)


def main():
    """应用程序入口点"""
    app = QApplication(sys.argv)
    
    # 创建船舶转向引导窗口
    window = ShipSteeringWindow()
    window.show()
    
    # 运行应用程序
    sys.exit(app.exec())


if __name__ == "__main__":
    main()