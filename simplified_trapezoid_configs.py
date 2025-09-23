#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化的梯形参数配置方案对比
"""

# 方案1: 当前配置 (7个参数)
CURRENT_CONFIG = {
    # 基础参数
    'height': 300,
    'top_base': 30,
    'bottom_base': 500,
    'outline_width': 2,
    # 弯曲参数
    'left_offset': 300,
    'curve_intensity': 0.6,
    'control_point_ratio': 0.4
}

# 方案2: 最简配置 (5个参数)
MINIMAL_CONFIG = {
    'height': 300,
    'top_base': 30,
    'bottom_base': 500,
    'left_offset': 300,
    'curve_amount': 72  # 直接指定偏移像素 (0.6 × 300 × 0.4 = 72)
}

# 方案3: 直观配置 (6个参数)
INTUITIVE_CONFIG = {
    'height': 300,
    'top_base': 30,
    'bottom_base': 500,
    'outline_width': 2,
    'left_offset': 300,
    'curve_pixels': 72  # 直接像素值
}

# 方案4: 比例配置 (6个参数)
RATIO_CONFIG = {
    'height': 300,
    'top_base': 30,
    'bottom_base': 500,
    'outline_width': 2,
    'left_offset': 300,
    'curve_ratio': 0.24  # 相对于高度的比例 (72/300 = 0.24)
}

def analyze_configs():
    """分析不同配置方案"""
    
    configs = {
        "当前配置": CURRENT_CONFIG,
        "最简配置": MINIMAL_CONFIG,
        "直观配置": INTUITIVE_CONFIG,
        "比例配置": RATIO_CONFIG
    }
    
    print("🔍 梯形参数配置方案对比")
    print("=" * 50)
    
    for name, config in configs.items():
        print(f"\n📊 {name}:")
        print(f"   参数数量: {len(config)}")
        print(f"   参数列表: {list(config.keys())}")
        
        # 计算最终偏移量
        if 'curve_amount' in config:
            offset = config['curve_amount']
        elif 'curve_pixels' in config:
            offset = config['curve_pixels']
        elif 'curve_ratio' in config:
            offset = config['curve_ratio'] * config['height']
        else:
            # 当前方法
            offset = config.get('curve_intensity', 0) * config['height'] * config.get('control_point_ratio', 0)
        
        print(f"   最终偏移: {offset:.1f}像素")
        
        # 优缺点分析
        if name == "当前配置":
            print("   ✓ 灵活性高，可精细调节")
            print("   ✗ 参数较多，概念有重叠")
        elif name == "最简配置":
            print("   ✓ 参数最少，概念清晰")
            print("   ✗ 缺少线宽控制")
        elif name == "直观配置":
            print("   ✓ 直接像素值，易于理解")
            print("   ✓ 保留必要的控制参数")
        elif name == "比例配置":
            print("   ✓ 比例值适应不同尺寸")
            print("   ✓ 参数含义明确")
    
    print("\n💡 推荐方案:")
    print("• 初学者 → 最简配置")
    print("• 一般使用 → 直观配置") 
    print("• 高级用户 → 当前配置")
    print("• 响应式设计 → 比例配置")

if __name__ == "__main__":
    analyze_configs()