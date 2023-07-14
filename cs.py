import sys
import queue
from PyQt5.QtWidgets import (
    QApplication, 
    QWidget,
    QPushButton,
)
from PyQt5.QtCore import (
    QPoint,
    Qt, 
    QTimer,
    QPropertyAnimation,
    QEasingCurve,
)
from PyQt5.QtGui import (
    QPixmap,
    QFont, 
    QPainter, 
    QPaintEvent,
    QColor, 
    QFontMetrics, 
    )

from Dialog.Dialog import DialogOver, DialogRight


class Window(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setWindowTitle("Window")
        self.resize(210, 210)
        
        self.but = QPushButton(self)
        self.but.setText("生成一个消息框")
        self.but.resize(200, 200)
        self.but.clicked.connect(self.dialog)
        
    def dialog(self) -> None:
        DialogOver("我是内容", title="我是标题", flags= "danger")
        DialogRight("我是内容", title="我是标题", flags= "danger")
        self.activateWindow() # 将活动窗口设置回来
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = Window()
    demo.show()
    sys.exit(app.exec_())