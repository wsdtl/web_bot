from typing import Optional, TYPE_CHECKING
from PySide6.QtWidgets import(
    QWidget, 
    QHBoxLayout, 
    QPushButton
)
from PySide6.QtCore import (
    QSize, 
    QEvent,
    QRect
)
from PySide6.QtGui import (
    Qt,
    QPixmap,
    QColor,
    QPaintEvent, 
    QPainter, 
    QEnterEvent,
    QMouseEvent
)

from .utils import change_theme_color
from .menu_index import MenuLeftSideFirst

if TYPE_CHECKING:
    from mainsindow import MainWindow


class TitlePushButtonMax(QPushButton):

    def __init__(
        self, 
        parent: "MainWindow",
        theme_color: Optional[QColor] = QColor(30, 204, 148, 255)
    ) -> None:
        super().__init__()
        self.setFixedSize(24, 24)
        self._size = QSize(16, 16)
        icon = QPixmap(":/image/max.png")
        self._icon = icon.scaled(self._size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self._icon_press = change_theme_color(icon, theme_color).scaled(self._size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        icon_max = QPixmap(":/image/max_press.png")
        self._icon_max = icon_max.scaled(self._size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self._icon_max_press = change_theme_color(icon_max, theme_color).scaled(self._size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self._parent = parent
        self._falg = False
        
        self.clicked.connect(self.__toggleMaxState)
    
    def __toggleMaxState(self):
        if self._parent.isMaximized():
            self._parent.showNormal()
        else:
            self._parent.showMaximized()
      
    def paintEvent(self, event: QPaintEvent) -> None: 
        painter = QPainter(self) 
        painter.setRenderHints(QPainter.Antialiasing | QPainter.TextAntialiasing)
        
        if self._parent.isMaximized():
            if self._falg:
                self.draw(event, painter, self._icon_max_press)
            else:
                self.draw(event, painter, self._icon_max)
        else:
            if self._falg:
                self.draw(event, painter, self._icon_press)
            else:
                self.draw(event, painter, self._icon)
            
    def draw(self, event: QPaintEvent, painter: QPainter, icon: QPixmap) -> None:
        painter.drawPixmap(
            (self.width() - self._size.width()) // 2,
            (self.height() - self._size.height()) // 2, 
            self._size.width(), 
            self._size.height(), 
            icon
        )   
    
    def enterEvent(self, event: QEnterEvent) -> None:
        self._falg = True
        return super().enterEvent(event)

    def leaveEvent(self, event: QEvent) -> None:
        self._falg = False
        return super().leaveEvent(event)

class TitlePushButtonMin(QPushButton):

    def __init__(
        self, 
        parent: QWidget,
        theme_color: Optional[QColor] = QColor(30, 204, 148, 255)
    ) -> None:
        super().__init__()
        self.setFixedSize(24, 24)
        self._size = QSize(16, 16)
        icon = QPixmap(":/image/min.png")
        self._icon = icon.scaled(self._size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self._icon_press = change_theme_color(icon, theme_color).scaled(self._size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self._falg = False
        
        self.clicked.connect(lambda: parent.showMinimized())
        
    def paintEvent(self, event: QPaintEvent) -> None: 
        painter = QPainter(self) 
        painter.setRenderHints(QPainter.Antialiasing | QPainter.TextAntialiasing)
        if self._falg:
            self.draw(event, painter, self._icon_press)
        else:
            self.draw(event, painter, self._icon)
            
    def draw(self, event: QPaintEvent, painter: QPainter, icon: QPixmap) -> None:
        painter.drawPixmap(
            (self.width() - self._size.width()) // 2,
            (self.height() - self._size.height()) // 2, 
            self._size.width(), 
            self._size.height(), 
            icon
        )    
    
    def enterEvent(self, event: QEnterEvent) -> None:
        self._falg = True
        return super().enterEvent(event)

    def leaveEvent(self, event: QEvent) -> None:
        self._falg = False
        return super().leaveEvent(event)

class TitlePushButtonExit(QPushButton):

    def __init__(
        self, 
        parent: QWidget,
        theme_color: Optional[QColor] = QColor(30, 204, 148, 255)
    ) -> None:
        super().__init__()
        self.setFixedSize(24, 24)
        self._size = QSize(16, 16)
        icon = QPixmap(":/image/exit.png")
        self._icon = icon.scaled(self._size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self._icon_press = change_theme_color(icon, theme_color).scaled(self._size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self._falg = False
        
        self.clicked.connect(lambda: parent.close())
      
    def paintEvent(self, event: QPaintEvent) -> None: 
        painter = QPainter(self) 
        painter.setRenderHints(QPainter.Antialiasing | QPainter.TextAntialiasing)
        if self._falg:
            self.draw(event, painter, self._icon_press)
        else:
            self.draw(event, painter, self._icon)
            
    def draw(self, event: QPaintEvent, painter: QPainter, icon: QPixmap) -> None:
        painter.drawPixmap(
            (self.width() - self._size.width()) // 2,
            (self.height() - self._size.height()) // 2, 
            self._size.width(), 
            self._size.height(), 
            icon
        )                             
    
    def enterEvent(self, event: QEnterEvent) -> None:
        self._falg = True
        return super().enterEvent(event)

    def leaveEvent(self, event: QEvent) -> None:
        self._falg = False
        return super().leaveEvent(event)
   

class MyTip(QWidget):
    
    def __init__(
        self,
        parent: QWidget
    ) -> None:
        super().__init__()
        self.setFixedHeight(36)
        self.moveFlag = False
        self._parent = parent
        self._logo = QPixmap(":/image/logo.png")
        self.layout = QHBoxLayout(self)
        self.layout.addStretch(1)
        self.layout.addWidget(TitlePushButtonMin(parent))
        self.layout.addWidget(TitlePushButtonMax(parent))
        self.layout.addWidget(TitlePushButtonExit(parent))
        self.layout.addSpacing(10)
        
    def paintEvent(self, event: QPaintEvent) -> None:
        # 开始绘制       
        painter = QPainter(self) 
        painter.setRenderHints(QPainter.Antialiasing | QPainter.TextAntialiasing)
        self.draw(event, painter)
        
    def draw(self, event: QPaintEvent, painter: QPainter) -> None:
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor("#f0f0f0"))
        w = MenuLeftSideFirst._w + 10
        h = self.height()
        painter.drawRect(0, 0, w, h)
        painter.drawPixmap(
            (w - self._logo.width()) // 2,
            (h - self._logo.height()) // 2, 
            self._logo.width(), 
            self._logo.height(),
            self._logo
        )
        
    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.LeftButton:
            self.moveFlag = True
            self.pos_star = event.globalPosition().toPoint()
            self.win_pos = self._parent.pos()
   
    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if self.moveFlag:
            self._parent.move(self.win_pos + event.globalPosition().toPoint() - self.pos_star)
            
    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        self.moveFlag = False
        

        

        
   