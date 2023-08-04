import queue
from typing import Tuple, Optional, TYPE_CHECKING
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import (
    QPoint,
    Qt, 
    QTimer,
    QPropertyAnimation,
    QEasingCurve
)
from PySide6.QtGui import (
    QPixmap,
    QFont, 
    QPainter, 
    QPaintEvent,
    QColor, 
    QFontMetrics 
)

if TYPE_CHECKING:
    from mainsindow import MainWindow

from . import rc


class DialogOver(QWidget):
    
    _instanceWidget: queue.Queue = queue.Queue(7)    # 存储实例化对象序号的队列，供paintEvent调用时判断位置
    _instanceDel: queue.Queue = queue.Queue(7)       # 存储实例化对象序号的队列, 供__del__调用时判断位置
    _instanceQueue: queue.Queue = queue.Queue(7)     #存储实例索引的队列，防止被回收
    _count: list = [0, 0, 0, 0, 0, 0, 0]             # 记录每个位置是否有对象

    def __new__(cls, *args, **kwargs) -> None:
        try:
            _index = cls._count.index(0)             # 寻找可用位置，即_count中为0的索引
        except ValueError:
            return
        cls._count[_index] = 1                       # 将对应位置置为1，表示该位置已被使用
        cls._instanceWidget.put(_index)              # 将可用位置的索引加入_instanceWidget队列
        cls._instanceDel.put(_index)                 # 将可用位置的索引加入_instanceDel队列
        instance = super(DialogOver, cls).__new__(cls)
        cls._instanceQueue.put(instance)             # 强引用防止被回收
        return instance

    def __del__(self) -> None:
        DialogOver._count[DialogOver._instanceDel.get()] = 0  # 将被删除对象的位置在_count中置为0，标记为空闲位置
        
    def __init__(
        self, 
        parent: "MainWindow",
        text: str, 
        title: Optional[str] = "", 
        flags: Optional[str] = "warning" or "danger" or "success",
        _showTime: Optional[int] = 1500,
        _dieTime: Optional[int] = 500
    )-> None:
        super().__init__()
                                                                     # 窗口设置
        self.setWindowFlags(
            Qt.WindowStaysOnTopHint 
            | Qt.FramelessWindowHint 
            | Qt.WindowType.SubWindow
            | Qt.WindowTransparentForInput
        ) 
        self.setAttribute(Qt.WA_TranslucentBackground, True)         # 设置窗口背景透明    
                                                    
        self._parent = parent                                        # 参数设置
        self._title = title
        self._text = text
        self._flags = flags
        self._dieTime = _dieTime                                     # 尺寸与偏移量设置
        self.setMinimumWidth(100)
        self.resize(self._parent.width() // 2, 40)
        self.moveSizeH = 6                                           # 每个窗口的高度偏移量, 窗口与窗口之间的间隙
        self.moveSize = 4                                            # 窗口的初始高度偏移量, 第一个窗口与父对象窗口上限的间隙
        self.moveDialog()                                            # 展示时间计时， 结束开始消失
        self.showTime = QTimer(self)                                # 定时器，控制显示时间
        self.showTime.setSingleShot(True)                           # 只触发一次
        self.showTime.start(_showTime)
        self.showTime.timeout.connect(self.disDialog)               # 显示时间到达后调用disDialog方法

        self.dieTime = QTimer(self)                                 # 定时器，控制关闭时间
        self.dieTime.setSingleShot(True)                            # 只触发一次
        self.dieTime.start(_showTime + _dieTime + 10)
        self.dieTime.timeout.connect(self.closeDialog)              # 关闭时间到达后调用closeDialog方法
        self.show()

    def paintEvent(self, event: QPaintEvent) -> None:
        # 绘制事件
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing | QPainter.TextAntialiasing)
        # 自定义的绘画方法
        if self._flags in ("success", "warning", "danger"):
            self.drawDialog(event, painter, self._flags)
        else:
            self.drawDialog(event, painter, "success")

    def drawDialog(
        self, 
        event: QPaintEvent, 
        painter: QPainter, 
        flags: str
    ) -> None:
        backgroundColor, borderColor, textColor = self.setColor(flags)           # 设置绘画颜色
        titleFont = QFont('Microsoft YaHei', 12, QFont.Bold)                     # 标题字体
        textFont = QFont('Microsoft YaHei', 12)                                  # 文字字体
        icoSize = 40 # 图标大小
        titleWidth = QFontMetrics(titleFont).horizontalAdvance(self._title) + 10 # 图标宽度, 间隙 10px
        textMaxLen = self.width() - icoSize - titleWidth                         # 计算空余空间下文字最大长度
        text, textWidth = self.prepare(self._text, textMaxLen, textFont)         # 整理文字
        backgroundWidth = icoSize + titleWidth + textWidth                       # 背景填充的宽度
        backgroundHight = self.height()                                          # 背景填充的高度
        backgroundX = (self.width() - backgroundWidth) // 2                      # 背景填充的 x 坐标
        backgroundY = 0                                                          # 背景填充的 y 坐标
        # 设置背景笔颜色 绘制背景
        painter.setPen(backgroundColor)                                          # 设置背景填充时的笔颜色
        painter.setBrush(backgroundColor)                                        # 设置背景填充时的填充颜色
        painter.drawRoundedRect(
            backgroundX, 
            backgroundY, 
            backgroundWidth,
            backgroundHight, 
            20.0, 
            20.0
        ) 
        # 画阴影
        painter.setPen(borderColor)                                              # 设置阴影笔颜色
        painter.drawRoundedRect(
            backgroundX, 
            backgroundY, 
            backgroundWidth,
            backgroundHight, 
            20.0, 
            20.0
        )
        # 画图标
        painter.drawPixmap(
            backgroundX + 5,
            backgroundY + 5,
            30,
            30,
            QPixmap(f':/image/{flags}.png').scaled(30, 30, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        )
        # 画 title 
        painter.setFont(titleFont)                                                 # 设置画笔字体
        painter.setPen(textColor)                                                  # 设置画笔颜色
        titleSizeMoveH = (backgroundHight - QFontMetrics(titleFont).height()) // 2 # 计算标题上方间隙距离
        painter.drawText(
            backgroundX + icoSize, 
            titleSizeMoveH,
            titleWidth,
            QFontMetrics(titleFont).height(),
            Qt.AlignLeft, 
            self._title
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
        x = self._parent.x() + (self._parent.width() // 2) - (self.width() // 2)
        y = self._parent.y() + self.moveSize + (DialogOver._instanceWidget.get() * (self.height() + self.moveSizeH))
        
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
        DialogOver._instanceQueue.get()                  # 取出强引用, 主动激活python回收释放实例对象，调用__del__函数
        self.close()
    
    def prepare(
        self, 
        text: str, 
        maxLen: int ,
        font: QFont
    ) -> str:
        # 整理长文本
        text = text.replace("\n","") 
        font = QFontMetrics(font)
        maxLen -= font.horizontalAdvance("pyqt")          # 字体的冗余长度
        textLen = 0
        textNew = ""
        for x in text:
            textNew += x
            textLen += font.horizontalAdvance(x)
            if textLen >= maxLen:
                textNew += "..."
                textLen += font.horizontalAdvance("...")
                break
            
        return textNew, textLen + 10
    