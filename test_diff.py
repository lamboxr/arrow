from PySide6.QtWidgets import QWidget, QApplication
from PySide6.QtGui import QPainter, QPen, QBrush, QLinearGradient, QPainterPath,QColor
from PySide6.QtCore import Qt, QPointF
import sys

class TestWidget(QWidget):
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # 创建相同的贝塞尔曲线路径（开放路径）
        path = QPainterPath()
        path.moveTo(50, 200)  # 起点
        path.quadTo(150, 50, 250, 200)  # 贝塞尔曲线
        
        # 创建渐变
        gradient = QLinearGradient(50, 50, 250, 200)
        start_color = QColor("#FF0000")
        start_color.setAlpha(12)  # 50%透明
        gradient.setColorAt(0, start_color)
        gradient.setColorAt(1, Qt.blue)
        
        # 第一种写法：绘制线条
        painter.save()  # 保存当前状态
        pen1 = QPen(QBrush(gradient), 5)
        painter.setPen(pen1)
        painter.drawPath(path)
        painter.restore()  # 恢复状态
        
        # 第二种写法：在下方绘制，对比效果
        painter.translate(0, 100)  # 下移100像素
        pen2 = QPen()
        pen2.setBrush(gradient)
        pen2.setWidth(5)
        painter.setPen(pen2)
        painter.drawPath(path)  # 同样只会绘制线条，不会填充

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = TestWidget()
    w.resize(300, 300)
    w.show()
    sys.exit(app.exec())