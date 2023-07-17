import sys
import queue
from typing import Tuple
from PyQt5.QtWidgets import (
    QApplication, 
    QWidget,
    QPushButton,
    QVBoxLayout
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

try:
    from . import resource_rc
except ImportError:
    import resource_rc

class DialogRight(QWidget):
    
    _instanceWidget: queue.Queue = queue.Queue(7)
    _instanceDel: queue.Queue = queue.Queue(7)
    _count: list = [0, 0, 0, 0, 0, 0, 0]
     
    def __new__(cls, *args, **kwargs) -> None:
        try:
            _index = cls._count.index(0)
        except ValueError:
            return
        cls._count[_index] = 1
        cls._instanceWidget.put(_index)
        cls._instanceDel.put(_index)
        return super(DialogRight, cls).__new__(cls)

    def __del__(self) -> None:
        DialogRight._count[DialogRight._instanceDel.get()] = 0
        
    def __init__(self, text: str ,title: str = "", flags: str ="success" or "warning" or "danger" ,_showTime: int = 3000, _dieTime: int = 500 ):
        super().__init__()
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint) 
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setAttribute(Qt.WA_TranslucentBackground, True) # 设置窗口背景透明
        self.title = title
        self.text = text
        self.flags = flags
        self.resize(240, 150)
        self.moveSizeW = 16   # 每个框的宽度偏移量
        self.moveSizeH = 10   # 每个框的高度偏移量
        self.moveSize = 0     # 框的初始高度偏移量
        self._dieTime = _dieTime
        self.moveDialog()
        self.showTime = QTimer(self)
        self.showTime.setSingleShot(True)  # 只触发一次
        self.showTime.start(_showTime)
        self.showTime.timeout.connect(self.disDialog)
        
        self.dieTime = QTimer(self)
        self.dieTime.setSingleShot(True)  # 只触发一次
        self.dieTime.start(_showTime + _dieTime + 50)
        self.dieTime.timeout.connect(self.closeDialog)
        self.show()
        
    def paintEvent(self, event: QPaintEvent) -> None:
        # 开始绘制       
        painter = QPainter(self) 
        painter.setRenderHints(QPainter.Antialiasing | QPainter.TextAntialiasing)
        # 自定义的绘画方法
        if self.flags in ["success", "warning", "danger"]:
            self.drawDialog(event, painter, self.flags)
        else:
            self.drawDialog(event, painter, "success")
        
    def drawDialog(self, event: QPaintEvent, painter: QPainter, flags: str) -> None:
        # 设置背景笔颜色
        painter.setPen(QColor(255, 255, 255))
        # 绘制背景
        painter.setBrush(QColor(255, 255, 255, 200))     
        painter.drawRoundedRect(event.rect(), 16.0, 16.0)
        # 画阴影
        painter.setPen(QColor('#d3d3d3'))
        painter.drawRoundedRect(event.rect(), 16.0, 16.0)
        # 画图标
        painter.drawPixmap(5, 5, 30, 30, QPixmap(f':/img/{flags}.png').scaled(30, 30, Qt.IgnoreAspectRatio, Qt.SmoothTransformation))
        # 设置笔 文字颜色
        font = QFont('Microsoft YaHei', 16)
        painter.setFont(font)
        painter.setPen(QColor(0, 0, 0))
        # 画 title
        painter.drawText(50, QFontMetrics(font).height(), self.title)
        # 设置笔 文字颜色
        font = QFont('Microsoft YaHei', 12)
        painter.setFont(font)
        # 画 text
        textWidth = self.width() - 60  # 字体框宽度
        textHight = self.height() - QFontMetrics(font).height() * 2 - 10 # 字体框高度
        text = self.prepare(self.text, textWidth, font)
        maxRow = textHight // QFontMetrics(font).height()
        if  text.count("\n") + 1 > maxRow:
            text = text.split("\n")
            textStart = text[:maxRow - 1]
            textEnd = text[maxRow]
            textStart = "\n".join(textStart)
            textEnd = textEnd[:-1] + "...."
            text = textStart + "\n" + textEnd
        painter.drawText(
            30, 
            QFontMetrics(font).height() * 2, 
            textWidth, 
            textHight, 
            Qt.AlignLeft,  
            text
        )
        
    def moveDialog(self) -> None:
        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height() - self.moveSize - (self.height() + self.moveSizeH) * (DialogRight._instanceWidget.get() + 1)
        animation = QPropertyAnimation(self, b"pos", self)
        animation.setStartValue(QPoint(w, h))
        animation.setEndValue(QPoint(w - self.width() - self.moveSizeW, h))
        animation.setDuration(1000)
        animation.setEasingCurve(QEasingCurve.OutCubic)
        animation.start()

    def disDialog(self) -> None:
        animation = QPropertyAnimation(self, b"windowOpacity", self)
        animation.setStartValue(1)
        animation.setEndValue(0)
        animation.setDuration(self._dieTime)
        animation.setEasingCurve(QEasingCurve.OutCubic)
        animation.start()
        
    def closeDialog(self) -> None:
        self.close()
        
    def prepare(self, text: str, maxLen: int ,font: QFont) -> str:
        # 整理长文本
        maxLen -= 20
        font = QFontMetrics(font)
        textLen = 0
        textNew = ""
        for x in text:
            textNew += x
            if x != "\n":
                textLen +=  font.width(x)
            else:
                textLen = 0
            if textLen >= maxLen:
                textLen = 0
                textNew += '\n'
        textNew = textNew.replace("\n\n","\n")        
        textNew = textNew.rstrip()
        return textNew

class DialogOver(QWidget):
    
    _instanceWidget: queue.Queue = queue.Queue(7)  # 存储实例化对象序号的队列，供paintEvent调用时判断位置
    _instanceDel: queue.Queue = queue.Queue(7)  # 存储实例化对象序号的队列, 供__del__调用时判断位置
    _count: list = [0, 0, 0, 0, 0, 0, 0]
     
    def __new__(cls, *args, **kwargs) -> None:
        try:
            _index = cls._count.index(0)
        except ValueError:
            return
        cls._count[_index] = 1
        cls._instanceWidget.put(_index)
        cls._instanceDel.put(_index)
        return super(DialogOver, cls).__new__(cls)

    def __del__(self) -> None:
        DialogOver._count[DialogOver._instanceDel.get()] = 0
        
    def __init__(self, parent: QWidget, text: str, title: str = "", flags: str ="success" or "warning" or "danger",
                _showTime: int = 3000, _dieTime: int = 300):
        super().__init__()
        # 窗口设置
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.WindowType.SubWindow) 
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setAttribute(Qt.WA_TranslucentBackground, True) # 设置窗口背景透明
        # 参数设置
        self.parent = parent
        self.title = title
        self.text = text
        self.flags = flags
        self._dieTime = _dieTime
        # 尺寸与偏移量设置
        self.setMinimumWidth(500)
        self.resize(self.parent.width() // 2, 40)
        self.moveSizeH = 6   # 每个窗口的高度偏移量, 窗口与窗口之间的间隙
        self.moveSize = 4     # 窗口的初始高度偏移量, 第一个窗口与父对象窗口上限的间隙
        # 进场动画
        self.moveDialog()
        # 展示时间计时， 结束开始消失
        self.showTime = QTimer(self)
        self.showTime.setSingleShot(True)  # 只触发一次
        self.showTime.start(_showTime)
        self.showTime.timeout.connect(self.disDialog)
        # 窗口结束时间计时， 结束释放对象
        self.dieTime = QTimer(self)
        self.dieTime.setSingleShot(True)  # 只触发一次
        self.dieTime.start(_showTime + _dieTime + 50)
        self.dieTime.timeout.connect(self.closeDialog)
        
        self.show()
        
    def paintEvent(self, event: QPaintEvent) -> None:
        # 开始绘制
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing | QPainter.TextAntialiasing)
        # 自定义的绘画方法
        if self.flags in ("success", "warning", "danger"):
            self.drawDialog(event, painter, self.flags)
        else:
            self.drawDialog(event, painter, "success")
        
    def drawDialog(self, event: QPaintEvent, painter: QPainter, flags: str) -> None:
        # 设置绘画颜色
        backgroundColor, borderColor, textColor = self.setColor(flags)
        
        titleFont = QFont('Microsoft YaHei', 12, QFont.Bold)  # 标题字体
        textFont = QFont('Microsoft YaHei', 12)  # 文字字体
        icoSize = 40 # 图标大小
        titleWidth = QFontMetrics(titleFont).width(self.title) + 10 # 图标宽度, 间隙 10px
        textMaxLen = self.width() - icoSize - titleWidth  # 计算空余空间下文字最大长度
        text, textWidth = self.prepare(self.text, textMaxLen, textFont) # 整理文字
        backgroundWidth = icoSize + titleWidth + textWidth # 背景填充的宽度
        backgroundHight = self.height() # 背景填充的高度
        backgroundX = (self.width() - backgroundWidth) // 2  # 背景填充的 x 坐标
        backgroundY = 0 # 背景填充的 y 坐标
        # 设置背景笔颜色 绘制背景
        painter.setPen(backgroundColor) # 设置背景填充时的笔颜色
        painter.setBrush(backgroundColor) # 设置背景填充时的填充颜色
        painter.drawRoundedRect(backgroundX, backgroundY, backgroundWidth, backgroundHight, 8.0, 8.0) 
        # 画阴影
        painter.setPen(borderColor) # 设置阴影笔颜色
        painter.drawRoundedRect(backgroundX, backgroundY, backgroundWidth, backgroundHight, 8.0, 8.0)
        # 画图标
        painter.drawPixmap(
            backgroundX + 5,
            backgroundY + 5,
            30,
            30,
            QPixmap(f':/img/{flags}.png').scaled(30, 30, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        )
        # 画 title 
        painter.setFont(titleFont) # 设置画笔字体
        painter.setPen(textColor) # 设置画笔颜色
        titleSizeMoveH = (backgroundHight - QFontMetrics(titleFont).height()) // 2 # 计算标题上方间隙距离
        painter.drawText(
            backgroundX + icoSize, 
            titleSizeMoveH,
            titleWidth,
            QFontMetrics(titleFont).height(),
            Qt.AlignLeft, 
            self.title
        )
        # 画 text 
        painter.setFont(textFont)
        painter.drawText(
            backgroundX + icoSize + titleWidth, 
            titleSizeMoveH, 
            textWidth, 
            QFontMetrics(textFont).height(), 
            Qt.AlignLeft,  
            text
        )
    
    def setColor(self, flags: str) -> Tuple[QColor, QColor, QColor]:
        if flags == "success":
            backgroundColor = QColor(240, 249, 235, 200)
            borderColor = QColor(227, 249, 214)
            textColor = QColor(0, 191, 0)
        elif flags == "warning":
            backgroundColor = QColor(253, 246, 236, 200)
            borderColor = QColor(241, 228, 208)
            textColor = QColor(241, 170, 62)
        elif flags == "danger":
            backgroundColor = QColor(254, 240, 240, 200)
            borderColor = QColor(239, 220, 219)
            textColor = QColor(245,108,108)
        else:
            backgroundColor = QColor(240, 249, 235, 200)
            borderColor = QColor(227, 249, 214)
            textColor = QColor(0, 191, 0)
            
        return backgroundColor, borderColor, textColor
    
    def moveDialog(self) -> None:
        x = self.parent.x() + (self.parent.width() // 2) - (self.width() // 2)
        y = self.parent.y() + self.moveSize + (DialogOver._instanceWidget.get() * (self.height() + self.moveSizeH))
        
        animation = QPropertyAnimation(self, b"pos", self)
        animation.setStartValue(QPoint(x + 100, y))
        animation.setEndValue(QPoint(x, y))
        animation.setDuration(1000)
        animation.setEasingCurve(QEasingCurve.OutCubic)
        animation.start()

    def disDialog(self) -> None:
        animation = QPropertyAnimation(self, b"windowOpacity", self)
        animation.setStartValue(1)
        animation.setEndValue(0)
        animation.setDuration(self._dieTime)
        animation.setEasingCurve(QEasingCurve.OutCubic)
        animation.start()
        
    def closeDialog(self) -> None:
        self.close()
        
    def prepare(self, text: str, maxLen: int ,font: QFont) -> str:
        # 整理长文本
        text = text.replace("\n","") 
        font = QFontMetrics(font)
        maxLen -= font.width("pyqt") # 字体的冗余长度
        textLen = 0
        textNew = ""
        for x in text:
            textNew += x
            textLen += font.width(x)
            if textLen >= maxLen:
                textNew += "..."
                textLen += font.width("...")
                break
            
        return textNew, textLen + 10

class Window(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setWindowTitle("Window")
        self.resize(500, 500)
        
        layout = QVBoxLayout(self)

        self.button1 = QPushButton("success", self)
        self.button2 = QPushButton("warning", self)
        self.button3 = QPushButton("danger", self)
        layout.addStretch(1)
        layout.addWidget(self.button1)
        layout.addWidget(self.button2)
        layout.addWidget(self.button3)
        
        self.button1.clicked.connect(self.but1)
        self.button2.clicked.connect(self.but2)
        self.button3.clicked.connect(self.but3)
        
        self.button1.setShortcut(Qt.Key_Q ) # 绑定Q
        self.button2.setShortcut(Qt.Key_W ) # 绑定W
        self.button3.setShortcut(Qt.Key_E ) # 绑定E
    
    def but1(self) -> None:
        self.resize(self.width() + 30, self.height() + 30)
        DialogOver(self, "我是success的类容", title="我是success", flags= "success")
        DialogRight("我是success的类容", title="我是success", flags= "success")
        self.activateWindow() # 将活动窗口设置回来
        
    def but2(self) -> None:
        self.resize(self.width() + 30, self.height() + 30)
        DialogOver(self, "我是warning的类容", title="我是warning", flags= "warning")
        DialogRight("我是warning的类容", title="我是warning", flags= "warning")
        self.activateWindow() # 将活动窗口设置回来
        
    def but3(self) -> None:
        self.resize(self.width() - 30, self.height() - 30)
        DialogOver(self, "我是danger,我没有标题", title="", flags= "danger")
        DialogRight("我是danger,我没有标题", title="", flags= "danger")
        self.activateWindow() # 将活动窗口设置回来
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = Window()
    demo.show()
    sys.exit(app.exec_())



