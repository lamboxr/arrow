#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
梯形几何计算测试
"""

import sys
import unittest
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QPointF, Qt
from PySide6.QtGui import QColor

# 导入我们的梯形Widget
from gradient_trapezoid import TrapezoidWidget


class TestTrapezoidGeometry(unittest.TestCase):
    """测试梯形几何计算"""
    
    @classmethod
    def setUpClass(cls):
        """设置测试环境"""
        cls.app = QApplication(sys.argv)
    
    def setUp(self):
        """每个测试前的设置"""
        self.widget = TrapezoidWidget()
        # 设置固定尺寸以便测试
        self.widget.resize(600, 400)
    
    def test_trapezoid_polygon_creation(self):
        """测试弯曲梯形几何创建"""
        geometry = self.widget._create_trapezoid_polygon()
        
        # 验证返回字典有4个关键点
        expected_keys = ['top_left', 'top_right', 'bottom_left', 'bottom_right']
        self.assertEqual(set(geometry.keys()), set(expected_keys), "应该有4个关键点")
        
        # 获取顶点坐标
        top_left = geometry['top_left']
        top_right = geometry['top_right']
        bottom_left = geometry['bottom_left']
        bottom_right = geometry['bottom_right']
        
        # 验证上底长度
        top_width = abs(top_right.x() - top_left.x())
        self.assertAlmostEqual(top_width, 30, places=1, msg="上底长度应为30像素")
        
        # 验证下底长度
        bottom_width = abs(bottom_right.x() - bottom_left.x())
        self.assertAlmostEqual(bottom_width, 500, places=1, msg="下底长度应为500像素")
        
        # 验证梯形高度
        height = abs(bottom_left.y() - top_left.y())
        self.assertAlmostEqual(height, 300, places=1, msg="梯形高度应为300像素")
        
        # 验证上底和下底的y坐标相同
        self.assertAlmostEqual(top_left.y(), top_right.y(), places=1, msg="上底两点y坐标应相同")
        self.assertAlmostEqual(bottom_left.y(), bottom_right.y(), places=1, msg="下底两点y坐标应相同")
        
        # 验证上底向左偏移200像素
        widget_center_x = self.widget.width() / 2
        top_center_x = (top_left.x() + top_right.x()) / 2
        expected_offset = widget_center_x - 200
        self.assertAlmostEqual(top_center_x, expected_offset, places=1, msg="上底应向左偏移200像素")
        
        print("弯曲梯形关键点坐标:")
        print(f"  上底左: ({top_left.x():.1f}, {top_left.y():.1f})")
        print(f"  上底右: ({top_right.x():.1f}, {top_right.y():.1f})")
        print(f"  下底左: ({bottom_left.x():.1f}, {bottom_left.y():.1f})")
        print(f"  下底右: ({bottom_right.x():.1f}, {bottom_right.y():.1f})")
        print(f"  上底中心偏移: {widget_center_x - top_center_x:.1f}像素")
    
    def test_trapezoid_symmetry(self):
        """测试弯曲梯形的对称性"""
        geometry = self.widget._create_trapezoid_polygon()
        
        # 获取关键点
        top_left = geometry['top_left']
        top_right = geometry['top_right']
        bottom_left = geometry['bottom_left']
        bottom_right = geometry['bottom_right']
        
        # 计算原始中心线x坐标
        original_center_x = self.widget.width() / 2
        
        # 验证上底关于其自身中心对称（虽然整体左移了）
        top_center_x = (top_left.x() + top_right.x()) / 2
        top_left_distance = abs(top_left.x() - top_center_x)
        top_right_distance = abs(top_right.x() - top_center_x)
        self.assertAlmostEqual(top_left_distance, top_right_distance, places=1, 
                              msg="上底应关于其自身中心对称")
        
        # 验证下底关于原始中心线对称
        bottom_left_distance = abs(bottom_left.x() - original_center_x)
        bottom_right_distance = abs(bottom_right.x() - original_center_x)
        self.assertAlmostEqual(bottom_left_distance, bottom_right_distance, places=1,
                              msg="下底应关于原始中心线对称")
    
    def test_gradient_creation(self):
        """测试渐变创建"""
        gradient = self.widget._create_gradient()
        
        # 验证渐变类型
        self.assertIsNotNone(gradient, "渐变对象不应为None")
        
        # 获取渐变的颜色停止点
        stops = gradient.stops()
        
        # 验证有3个颜色停止点
        self.assertEqual(len(stops), 3, "应该有3个渐变颜色点")
        
        # 验证颜色停止点位置
        positions = [stop[0] for stop in stops]
        expected_positions = [0.0, 0.5, 1.0]
        
        for i, (actual, expected) in enumerate(zip(positions, expected_positions)):
            self.assertAlmostEqual(actual, expected, places=2, 
                                 msg=f"颜色停止点{i+1}位置应为{expected}")
        
        # 验证颜色值
        colors = [stop[1] for stop in stops]
        
        # 顶部颜色：#B6B384，完全透明
        top_color = colors[0]
        self.assertEqual(top_color.name().upper(), "#B6B384", "顶部颜色应为#B6B384")
        self.assertEqual(top_color.alpha(), 0, "顶部颜色应完全透明")
        
        # 中间颜色：#FEFFAF，50%透明
        middle_color = colors[1]
        self.assertEqual(middle_color.name().upper(), "#FEFFAF", "中间颜色应为#FEFFAF")
        self.assertEqual(middle_color.alpha(), 127, "中间颜色应为50%透明")
        
        # 底部颜色：#B7B286，完全透明
        bottom_color = colors[2]
        self.assertEqual(bottom_color.name().upper(), "#B7B286", "底部颜色应为#B7B286")
        self.assertEqual(bottom_color.alpha(), 0, "底部颜色应完全透明")
        
        print("渐变颜色设置:")
        for i, (pos, color) in enumerate(stops):
            print(f"  停止点{i+1}: 位置{pos}, 颜色{color.name()}, 透明度{color.alpha()}")
    
    def test_line_gradient_creation(self):
        """测试腰线渐变创建"""
        # 创建测试用的起点和终点
        start_point = QPointF(100, 50)
        end_point = QPointF(50, 350)
        
        gradient = self.widget._create_line_gradient(start_point, end_point)
        
        # 验证渐变对象
        self.assertIsNotNone(gradient, "腰线渐变对象不应为None")
        
        # 获取渐变的颜色停止点
        stops = gradient.stops()
        
        # 验证有3个颜色停止点
        self.assertEqual(len(stops), 3, "腰线渐变应该有3个颜色点")
        
        # 验证颜色停止点位置
        positions = [stop[0] for stop in stops]
        expected_positions = [0.0, 0.5, 1.0]
        
        for i, (actual, expected) in enumerate(zip(positions, expected_positions)):
            self.assertAlmostEqual(actual, expected, places=2, 
                                 msg=f"腰线渐变颜色停止点{i+1}位置应为{expected}")
        
        # 验证颜色值和透明度
        colors = [stop[1] for stop in stops]
        
        # 起点颜色：#B6B384，完全透明
        start_color = colors[0]
        self.assertEqual(start_color.name().upper(), "#B6B384", "起点颜色应为#B6B384")
        self.assertEqual(start_color.alpha(), 0, "起点颜色应完全透明")
        
        # 中间颜色：#FEFFAF，50%透明
        middle_color = colors[1]
        self.assertEqual(middle_color.name().upper(), "#FEFFAF", "中间颜色应为#FEFFAF")
        self.assertEqual(middle_color.alpha(), 127, "中间颜色应为50%透明")
        
        # 终点颜色：#B7B286，完全透明
        end_color = colors[2]
        self.assertEqual(end_color.name().upper(), "#B7B286", "终点颜色应为#B7B286")
        self.assertEqual(end_color.alpha(), 0, "终点颜色应完全透明")
        
        print("腰线渐变颜色设置:")
        for i, (pos, color) in enumerate(stops):
            print(f"  停止点{i+1}: 位置{pos}, 颜色{color.name()}, 透明度{color.alpha()}")
    
    def test_curved_path_creation(self):
        """测试贝塞尔曲线路径创建"""
        # 创建测试用的起点和终点
        start_point = QPointF(100, 50)
        end_point = QPointF(50, 350)
        
        path = self.widget._create_curved_path(start_point, end_point)
        
        # 验证路径对象
        self.assertIsNotNone(path, "贝塞尔曲线路径不应为None")
        
        # 验证路径不为空
        self.assertFalse(path.isEmpty(), "贝塞尔曲线路径不应为空")
        
        # 验证路径的起点
        path_start = path.pointAtPercent(0.0)
        self.assertAlmostEqual(path_start.x(), start_point.x(), places=1, msg="路径起点X坐标应正确")
        self.assertAlmostEqual(path_start.y(), start_point.y(), places=1, msg="路径起点Y坐标应正确")
        
        # 验证路径的终点
        path_end = path.pointAtPercent(1.0)
        self.assertAlmostEqual(path_end.x(), end_point.x(), places=1, msg="路径终点X坐标应正确")
        self.assertAlmostEqual(path_end.y(), end_point.y(), places=1, msg="路径终点Y坐标应正确")
        
        # 验证路径中点的弯曲效果（应该向右偏移）
        path_mid = path.pointAtPercent(0.5)
        straight_mid_x = (start_point.x() + end_point.x()) / 2
        self.assertGreater(path_mid.x(), straight_mid_x, "路径中点应向右弯曲")
        
        print(f"贝塞尔曲线路径:")
        print(f"  起点: ({path_start.x():.1f}, {path_start.y():.1f})")
        print(f"  中点: ({path_mid.x():.1f}, {path_mid.y():.1f}) (直线中点X: {straight_mid_x:.1f})")
        print(f"  终点: ({path_end.x():.1f}, {path_end.y():.1f})")
        print(f"  向右偏移: {path_mid.x() - straight_mid_x:.1f}像素")


if __name__ == "__main__":
    unittest.main()