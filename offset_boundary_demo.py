#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
偏移量边界演示程序
展示偏移量的理论范围和实际限制
"""

import sys
import math
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                               QHBoxLayout, QLabel, QSlider, QCheckBox)
from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QPainter, QLinearGradient, QPen, QColor, QPainterPath


class OffsetBoundaryWidget(QWidget):
    """偏移量边界演示Widget"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # 控制参数
        self.offset_multiplier = 1.0    # 偏移量倍数 (可以很大)
        self.show_extreme = False       # 是否显示极端情况
        
        self.setFixedSize(900, 600)
        self.setStyleSheet("background-color: #FFFFFF; border: 2px solid #333333;")
    
    def set_parameters(self, offset_multiplier, show_extreme):
        """设置参数并重绘"""
        self.offset_multiplier = offset_multiplier
        self.show_extreme = show_extreme
        self.update()
    
    def paintEvent(self, event):
        """绘制偏移量边界演示"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        
        try:
            # 定义基本参数
            widget_width = self.width()
            widget_height = self.height()
            
            # 基础线段
            start_point = QPointF(150, 150)
            end_point = QPointF(250, 450)
            
            # 计算中点
            mid_x = (start_point.x() + end_point.x()) / 2
            mid_y = (start_point.y() + end_point.y()) / 2
            mid_point = QPointF(mid_x, mid_y)
            
            # 计算不同偏移量的控制点
            base_offset = 50  # 基础偏移量
            
            offsets = []
            if self.show_extreme:
                # 显示极端情况
                offsets = [
                    0,                                    # 无偏移
                    base_offset * 0.5,                   # 小偏移
                    base_offset * 1.0,                   # 正常偏移
                    base_offset * 2.0,                   # 大偏移
                    base_offset * 5.0,                   # 很大偏移
                    base_offset * self.offset_multiplier  # 用户控制的偏移
                ]
            else:
                # 只显示用户控制的偏移
                offsets = [base_offset * self.offset_multiplier]
            
            colors = ["#999999", "#4ECDC4", "#45B7D1", "#FF9F43", "#FF6B6B", "#8E44AD"]
            
            # 1. 绘制Widget边界
            painter.setPen(QPen(QColor("#FF0000"), 2, Qt.DashLine))
            painter.drawRect(10, 10, widget_width-20, widget_height-20)
            painter.drawText(15, 30, "Widget边界")
            
            # 2. 绘制直线参考
            painter.setPen(QPen(QColor("#CCCCCC"), 2, Qt.DashLine))
            painter.drawLine(start_point, end_point)
            
            # 3. 绘制不同偏移量的曲线
            for i, offset in enumerate(offsets):
                if i >= len(colors):
                    color = colors[-1]
                else:
                    color = colors[i]
                
                # 计算控制点
                control_point = QPointF(mid_x + offset, mid_y)
                
                # 检查控制点是否超出边界
                out_of_bounds = (control_point.x() < 0 or 
                               control_point.x() > widget_width or
                               control_point.y() < 0 or 
                               control_point.y() > widget_height)
                
                # 绘制贝塞尔曲线
                path = QPainterPath()
                path.moveTo(start_point)
                path.quadTo(control_point, end_point)
                
                line_style = Qt.DashLine if out_of_bounds else Qt.SolidLine
                painter.setPen(QPen(QColor(color), 3, line_style))
                painter.drawPath(path)
                
                # 绘制控制点
                if control_point.x() >= 0 and control_point.x() <= widget_width:
                    painter.setPen(QPen(QColor(color), 2))
                    painter.setBrush(QColor(color))
                    painter.drawEllipse(control_point, 6, 6)
                    
                    # 标注偏移量
                    painter.setPen(QColor("#333333"))
                    painter.drawText(control_point.x() + 10, control_point.y(), f"{offset:.0f}px")
            
            # 4. 绘制关键点
            painter.setPen(QPen(QColor("#000000"), 2))
            painter.setBrush(QColor("#000000"))
            painter.drawEllipse(start_point, 8, 8)
            painter.drawEllipse(end_point, 8, 8)
            painter.drawEllipse(mid_point, 6, 6)
            
            # 标注
            painter.drawText(start_point.x() - 30, start_point.y() - 10, "起点")
            painter.drawText(end_point.x() - 30, end_point.y() + 20, "终点")
            painter.drawText(mid_point.x() - 30, mid_point.y() - 10, "中点")
            
            # 5. 绘制信息面板
            info_x = 400
            painter.setPen(QColor("#333333"))
            painter.drawText(info_x, 50, "偏移量边界分析")
            painter.drawText(info_x, 70, "=" * 40)
            
            current_offset = base_offset * self.offset_multiplier
            painter.drawText(info_x, 100, f"当前偏移量: {current_offset:.1f} 像素")
            painter.drawText(info_x, 120, f"偏移倍数: {self.offset_multiplier:.1f}")
            
            # 边界检查
            control_x = mid_x + current_offset
            painter.drawText(info_x, 150, "边界检查:")
            
            if control_x < 0:
                painter.setPen(QColor("#FF0000"))
                painter.drawText(info_x, 170, "❌ 控制点超出左边界")
            elif control_x > widget_width:
                painter.setPen(QColor("#FF0000"))
                painter.drawText(info_x, 170, "❌ 控制点超出右边界")
            else:
                painter.setPen(QColor("#00AA00"))
                painter.drawText(info_x, 170, "✅ 控制点在边界内")
            
            painter.setPen(QColor("#333333"))
            
            # 理论限制
            painter.drawText(info_x, 200, "理论边界:")
            painter.drawText(info_x, 220, f"• 左边界: {-mid_x:.0f} 像素")
            painter.drawText(info_x, 240, f"• 右边界: {widget_width - mid_x:.0f} 像素")
            
            # 实际建议
            painter.drawText(info_x, 270, "实际建议范围:")
            line_length = math.sqrt((end_point.x() - start_point.x())**2 + 
                                  (end_point.y() - start_point.y())**2)
            suggested_max = line_length * 0.5
            painter.drawText(info_x, 290, f"• 建议最大: {suggested_max:.0f} 像素")
            painter.drawText(info_x, 310, f"  (线段长度的50%)")
            
            # 视觉效果分析
            painter.drawText(info_x, 340, "视觉效果:")
            if current_offset == 0:
                painter.drawText(info_x, 360, "• 直线 (无弯曲)")
            elif current_offset < 25:
                painter.drawText(info_x, 360, "• 轻微弯曲")
            elif current_offset < 100:
                painter.drawText(info_x, 360, "• 适中弯曲")
            elif current_offset < 200:
                painter.drawText(info_x, 360, "• 明显弯曲")
            elif current_offset < 400:
                painter.drawText(info_x, 360, "• 强烈弯曲")
            else:
                painter.setPen(QColor("#FF6B6B"))
                painter.drawText(info_x, 360, "• 极端弯曲 (可能失真)")
            
            painter.setPen(QColor("#333333"))
            
            # 数学极限
            painter.drawText(info_x, 400, "数学极限:")
            painter.drawText(info_x, 420, "• 理论上: 无限大")
            painter.drawText(info_x, 440, "• 实际上: 受Widget尺寸限制")
            painter.drawText(info_x, 460, "• 视觉上: 过大会失去意义")
            
            # 性能考虑
            painter.drawText(info_x, 490, "性能考虑:")
            if current_offset > 1000:
                painter.setPen(QColor("#FF6B6B"))
                painter.drawText(info_x, 510, "• 超大偏移可能影响渲染性能")
            else:
                painter.setPen(QColor("#00AA00"))
                painter.drawText(info_x, 510, "• 当前偏移量性能良好")
            
        except Exception as e:
            print(f"绘图错误: {e}")
        finally:
            painter.end()


class OffsetBoundaryWindow(QMainWindow):
    """偏移量边界演示窗口"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("偏移量边界分析 - 理论范围 vs 实际限制")
        self.setGeometry(100, 100, 1000, 800)
        
        # 创建中心Widget和布局
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # 添加标题
        title = QLabel("偏移量的边界分析")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold; margin: 10px;")
        layout.addWidget(title)
        
        # 创建演示Widget
        self.demo_widget = OffsetBoundaryWidget()
        layout.addWidget(self.demo_widget)
        
        # 创建控制面板
        controls_layout = QHBoxLayout()
        
        # 偏移倍数滑块
        multiplier_layout = QVBoxLayout()
        multiplier_layout.addWidget(QLabel("偏移倍数:"))
        self.multiplier_slider = QSlider(Qt.Horizontal)
        self.multiplier_slider.setRange(0, 2000)  # 0到20倍
        self.multiplier_slider.setValue(100)      # 默认1倍
        self.multiplier_label = QLabel("1.0")
        multiplier_layout.addWidget(self.multiplier_slider)
        multiplier_layout.addWidget(self.multiplier_label)
        controls_layout.addLayout(multiplier_layout)
        
        # 显示极端情况复选框
        self.extreme_checkbox = QCheckBox("显示多种偏移量对比")
        self.extreme_checkbox.setChecked(False)
        controls_layout.addWidget(self.extreme_checkbox)
        
        layout.addLayout(controls_layout)
        
        # 连接事件
        self.multiplier_slider.valueChanged.connect(self.update_parameters)
        self.extreme_checkbox.toggled.connect(self.update_parameters)
        
        # 添加详细说明
        info_text = """
📏 偏移量边界分析:

🔢 理论范围:
• 数学上: 偏移量可以是任意实数 (-∞ 到 +∞)
• 计算上: 受浮点数精度限制 (约 ±10^308)

🖥️ 实际限制:
• Widget边界: 控制点超出显示区域会被裁剪
• 视觉意义: 过大偏移失去弯曲的视觉意义
• 性能影响: 极大偏移可能影响渲染性能

💡 建议范围:
• 轻微弯曲: 0.1 - 0.5 倍线段长度
• 适中弯曲: 0.5 - 1.0 倍线段长度  
• 强烈弯曲: 1.0 - 2.0 倍线段长度
• 极端效果: 2.0+ 倍线段长度 (谨慎使用)

⚠️ 注意事项:
• 负偏移会产生向左弯曲
• 零偏移等于直线
• 过大偏移可能产生意外的视觉效果
        """
        
        info_label = QLabel(info_text)
        info_label.setStyleSheet(
            "margin: 10px; padding: 10px; "
            "background-color: #F8F9FA; border: 1px solid #DEE2E6; "
            "border-radius: 5px; font-size: 10px;"
        )
        layout.addWidget(info_label)
    
    def update_parameters(self):
        """更新参数并重绘"""
        multiplier = self.multiplier_slider.value() / 100.0
        show_extreme = self.extreme_checkbox.isChecked()
        
        # 更新标签
        self.multiplier_label.setText(f"{multiplier:.1f}")
        
        # 更新演示Widget
        self.demo_widget.set_parameters(multiplier, show_extreme)


def main():
    """应用程序入口点"""
    app = QApplication(sys.argv)
    
    # 创建演示窗口
    window = OffsetBoundaryWindow()
    window.show()
    
    # 运行应用程序
    sys.exit(app.exec())


if __name__ == "__main__":
    main()