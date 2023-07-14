import sys
import queue
from typing import List
from PySide6.QtWidgets import (
    QApplication, 
    QWidget,
    QPushButton,
)
from PySide6.QtCore import (
    QPoint,
    Qt, 
    QTimer,
    QPropertyAnimation,
    QEasingCurve,
)
from PySide6.QtGui import (
    QPixmap,
    QFont, 
    QPainter, 
    QPaintEvent,
    QColor, 
    QFontMetrics, 
    )

try:
    from . import rc_icons
except ImportError:
    import rc_icons


class DialogRight(QWidget):
    
    _instanceWidget: queue.Queue = queue.Queue(7)
    _instanceDel: queue.Queue = queue.Queue(7)
    _instanceQueue: queue.Queue = queue.Queue(7)   #存储实例索引的队列，防止被回收
    _count: list = [0, 0, 0, 0, 0, 0, 0]
     
    def __new__(cls, *args, **kwargs) -> None:
        try:
            _index = cls._count.index(0)
        except ValueError:
            return
        cls._count[_index] = 1
        cls._instanceWidget.put(_index)
        cls._instanceDel.put(_index)
        instance = super(DialogRight, cls).__new__(cls)
        cls._instanceQueue.put(instance) # 强引用防止被回收
        return instance

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
        desktop = QApplication.instance().screens()[0].size()
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
        DialogRight._instanceQueue.get()  # 取出强索引, 主动激活python回收释放实例对象，调用__del__函数
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
                textLen +=  font.horizontalAdvance(x)
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
    _instanceQueue: queue.Queue = queue.Queue(7)   #存储实例索引的队列，防止被回收
    _count: list = [0, 0, 0, 0, 0, 0, 0]  # 记录每个位置是否有对象

    def __new__(cls, *args, **kwargs) -> None:
        try:
            _index = cls._count.index(0)  # 寻找可用位置，即_count中为0的索引
        except ValueError:
            return
        cls._count[_index] = 1  # 将对应位置置为1，表示该位置已被使用
        cls._instanceWidget.put(_index)  # 将可用位置的索引加入_instanceWidget队列
        cls._instanceDel.put(_index)  # 将可用位置的索引加入_instanceDel队列
        instance = super(DialogOver, cls).__new__(cls)
        cls._instanceQueue.put(instance) # 强引用防止被回收
        return instance

    def __del__(self) -> None:
        DialogOver._count[DialogOver._instanceDel.get()] = 0  # 将被删除对象的位置在_count中置为0，标记为空闲位置
        
    def __init__(self, text: str, title: str = "", flags: str = "success" or "warning" or "danger",
                 _showTime: int = 3000, _dieTime: int = 500):
        super().__init__()

        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        # self.setAttribute(Qt.WA_DeleteOnClose)  # pyside6 此函数没有用,因此要自己对自己进行强索引
        self.setAttribute(Qt.WA_TranslucentBackground, True)  # 设置窗口背景透明
        self.title = title
        self.text = text
        self.flags = flags
        self.resize(500, 40)
        self.moveSizeH = 6  # 每个框的高度偏移量
        self.moveSize = 6  # 框的初始高度偏移量
        self._dieTime = _dieTime
        self.moveDialog()
        self.showTime = QTimer(self)  # 定时器，控制显示时间
        self.showTime.setSingleShot(True)  # 只触发一次
        self.showTime.start(_showTime)
        self.showTime.timeout.connect(self.disDialog)  # 显示时间到达后调用disDialog方法

        self.dieTime = QTimer(self)  # 定时器，控制关闭时间
        self.dieTime.setSingleShot(True)  # 只触发一次
        self.dieTime.start(_showTime + _dieTime + 50)
        self.dieTime.timeout.connect(self.closeDialog)  # 关闭时间到达后调用closeDialog方法
        self.show()

    def paintEvent(self, event: QPaintEvent) -> None:
        # 绘制事件
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
        painter.setBrush(QColor(255, 255, 255, 240))
        painter.drawRoundedRect(event.rect(), 16.0, 16.0)
        # 画图标
        img = QPixmap(f':/img/{flags}.png').scaled(30, 30, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        painter.drawPixmap(5, 5, 30, 30, img)
        # 设置笔 文字颜色
        font = QFont('Microsoft YaHei', 12, QFont.Bold)
        painter.setFont(font)
        painter.setPen(QColor(0, 0, 0))
        # 画 title
        titleSizeMoveH = (self.height() - QFontMetrics(font).height()) // 2  # 计算标题在垂直方向上的位置
        titleWidth = QFontMetrics(font).horizontalAdvance(self.title)  # 计算标题的宽度
        painter.drawText(
            40,
            titleSizeMoveH,
            titleWidth,
            QFontMetrics(font).height(),
            Qt.AlignLeft,
            self.title
        )
        # 设置笔 文字颜色
        font = QFont('Microsoft YaHei', 12)
        painter.setFont(font)
        # 画 text
        textMaxLen = self.width() - 40 - titleWidth  # 计算文本的最大长度
        text, textWidth = self.prepare(self.text, textMaxLen, font)  # 调用prepare方法整理长文本
        painter.drawText(
            40 + titleWidth + 5,
            titleSizeMoveH,
            textWidth,
            QFontMetrics(font).height(),
            Qt.AlignLeft,
            text
        )

    def moveDialog(self) -> None:
        # desktop = QApplication.desktop().availableGeometry()
        desktop = QApplication.instance().screens()[0].size()

        w, h = desktop.width() // 2, self.moveSize + (self.height() + self.moveSizeH) * (DialogOver._instanceWidget.get())
        animation = QPropertyAnimation(self, b"pos", self)
        animation.setStartValue(QPoint(w, h))
        animation.setEndValue(QPoint((desktop.width() - self.width()) // 2, h))
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
        DialogOver._instanceQueue.get()  # 取出强索引, 主动激活python回收释放实例对象，调用__del__函数
        self.close()
    
    def prepare(self, text: str, maxLen: int, font: QFont) -> str:
        # 整理长文本
        text = text.replace("\n", "")
        maxLen -= 30  # 减去图标的宽度
        font = QFontMetrics(font)
        textLen = 0
        textNew = ""
        for x in text:
            textNew += x
            textLen += font.horizontalAdvance(x)  # 计算文本的宽度
            if textLen >= maxLen:
                textNew += "..."
                textLen += font.horizontalAdvance("...")  # 如果文本宽度超过最大长度，则加上省略号并跳出循环
                break
        return textNew, textLen
    


class Window(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        
        self.dialogList: List[DialogOver] = []
        self.setWindowTitle("Window")
        self.resize(450, 450)

        self.but = QPushButton(self)
        self.but.setText("生成一个消息框")
        self.but.resize(400, 400)
        self.but.clicked.connect(self.dialog)

    def dialog(self) -> None:
        dialog1 = DialogOver("我是内容", title="我是标题", flags="success")
        dialog2 = DialogRight("我是内容", title="我是标题", flags="success")
        self.activateWindow()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = Window()
    demo.show()
    sys.exit(app.exec())
