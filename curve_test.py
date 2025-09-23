#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
弯曲参数效果测试
"""

def calculate_curve_offset(curve_intensity, control_point_ratio, height=300):
    """计算控制点偏移量"""
    return curve_intensity * height * control_point_ratio

# 测试不同参数组合
test_cases = [
    # (curve_intensity, control_point_ratio, 描述)
    (0.1, 0.1, "极轻微弯曲"),
    (0.2, 0.2, "轻微弯曲"),
    (0.3, 0.3, "当前设置 - 中等弯曲"),
    (0.5, 0.3, "增强弯曲强度"),
    (0.3, 0.5, "增强控制点比例"),
    (0.5, 0.5, "强烈弯曲"),
    (0.8, 0.4, "很强弯曲"),
    (1.0, 0.5, "极端弯曲"),
]

print("弯曲参数效果对比:")
print("=" * 60)
print(f"{'弯曲强度':<8} {'控制点比例':<10} {'偏移量(px)':<10} {'描述'}")
print("-" * 60)

for intensity, ratio, desc in test_cases:
    offset = calculate_curve_offset(intensity, ratio)
    print(f"{intensity:<8} {ratio:<10} {offset:<10.1f} {desc}")

print("\n参数关系说明:")
print("1. 弯曲强度 × 控制点比例 = 综合弯曲效果")
print("2. 两个参数都影响最终的控制点偏移量")
print("3. 弯曲强度是主要参数，控制点比例是微调参数")
print("4. 偏移量越大，弯曲越明显")