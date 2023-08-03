from typing import List, Optional, TYPE_CHECKING, Callable
from PySide6.QtCore import(
    QSize,
    Qt
)
from PySide6.QtGui import(
    QPaintEvent,
    QPainter,
    QPixmap,
    QFont,
    QFontMetrics,
    QColor
)
from PySide6.QtWidgets import (
    QStackedWidget,
    QWidget,
    QListWidget, 
    QVBoxLayout,
    QListWidgetItem,
    QPushButton,
    QButtonGroup
)

from . import rc
from .utils import change_theme_color

if TYPE_CHECKING:
    from mainsindow import MainWindow
    
    
class PushButton(QPushButton):
    
    _group = QButtonGroup()
    
    def __init__(self, son) -> None:
        super().__init__()
        PushButton._group.addButton(son)
        
class MenuLeftSideFirst(PushButton):

    _w: int = 170
    _h: int = 50

    def __init__(
        self, 
        text: str, 
        icon: QPixmap,
        font_name: Optional[str] = 'SimHei', 
        font_size: Optional[int] = 14,
        theme_color: Optional[QColor] = QColor(255, 255, 255, 255)
    ) -> None:
        super().__init__(self)
        
        self._text = text
        self._icon = icon.scaled(QSize(15, 15), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self._icon_press = change_theme_color(icon, theme_color).scaled(QSize(15, 15), Qt.KeepAspectRatio, Qt.SmoothTransformation) 
        self._move_letf = 14
        self._move_space = 10
        self._font = QFont(font_name, font_size, QFont.Light)
        self._fontMetrics = QFontMetrics(self._font)
        self.setFixedSize(QSize(self._w - 10, self._h - 10))
        self.setCheckable(True)  # 设置可以被选中
        self.setAutoExclusive(True)  # 设置自动排它
        self.setObjectName("MenuLeftSideFirst")
        self.setStyleSheet(
        """
        QPushButton#MenuLeftSideFirst 
        {
            border-radius: 0px;
            padding-left: 20px;
            padding-top: 10px;
            padding-right: 20px;
            padding-bottom: 10px;
        }
        QPushButton#MenuLeftSideFirst:hover 
        {
            border-left: 2px solid #1ecc94;
        }
        QPushButton#MenuLeftSideFirst:checked     
        {
            border-radius: 5px;
            background-color: #1ecc94;
        }         
        """)
        
    def text(self) -> str:
        return self._text
        
    def paintEvent(self, event: QPaintEvent) -> None: 
        super().paintEvent(event) 
        painter = QPainter(self) 
        painter.setRenderHints(QPainter.Antialiasing | QPainter.TextAntialiasing)
        if self.isChecked():
            self.draw(event, painter, self._icon_press, "#ffffff")
        else:
            self.draw(event, painter, self._icon, "#000000")
    
    def draw(self, event: QPaintEvent, painter: QPainter, icon: QPixmap, font_color: str) -> None:
        painter.drawPixmap(
            self._move_letf,
            (self.height() - icon.height()) // 2, 
            icon.width(), 
            icon.height(), 
            icon
        )
        # 画文字
        painter.setFont(self._font)
        painter.setPen(QColor(font_color))
        painter.drawText(
            self._move_letf + self._move_space + self._icon.width(),
            (self.height() - self._fontMetrics.height()) // 2, 
            self._fontMetrics.horizontalAdvance(self.text()),
            self._fontMetrics.height(),
            Qt.AlignLeft,
            self._text
        )
 
class MenuLeftSideSecondary(PushButton):
    
    _w: int = 170
    _h: int = 50

    def __init__(
        self, 
        text: str, 
        sign_func: "MainWindow.display",
        font_name: Optional[str] = 'SimHei', 
        font_size: Optional[int] = 12
    ) -> None:
        super().__init__(self)
        self._text = text
        self._sign_func = sign_func
        self._move_letf = 20
        self._move_space = 5
        self._font = QFont(font_name, font_size, QFont.Light)
        self._fontMetrics = QFontMetrics(self._font)
        self._icon = QPixmap(":/image/arrow.png").scaled(QSize(12, 12), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.setFixedSize(QSize(self._w - 10, self._h - 10))
        self.setCheckable(True)  # 设置可以被选中
        self.setAutoExclusive(True)  # 设置自动排它
        self.setObjectName("MenuLeftSideSecondary")
        self.setStyleSheet(
        """
        QPushButton#MenuLeftSideSecondary 
        {
            border-radius: 0px;
            padding-left: 20px;
            padding-top: 10px;
            padding-right: 20px;
            padding-bottom: 10px;
        }
        QPushButton#MenuLeftSideSecondary:hover 
        {
            border-left: 2px solid #1ecc94;
        }
        QPushButton#MenuLeftSideSecondary:checked     
        {
            border-radius: 5px;
            background-color: #1ecc94;
        }         
        """)
        self.clicked.connect(lambda: self._sign_func(self.text()))
        
    def text(self) -> str:
        return self._text
        
    def paintEvent(self, event: QPaintEvent) -> None: 
        super().paintEvent(event) 
        painter = QPainter(self) 
        painter.setRenderHints(QPainter.Antialiasing | QPainter.TextAntialiasing)
        if self.isChecked():
            self.draw(event, painter, "#ffffff", icon = True)
        else:
            self.draw(event, painter, "#000000")
    
    def draw(self, event: QPaintEvent, painter: QPainter, font_color: str, icon: Optional[bool] = False) -> None:
        if icon:
            painter.drawPixmap(
                self._move_letf,
                (self.height() - self._icon.height()) // 2, 
                self._icon.width(), 
                self._icon.height(), 
                self._icon
            )
            # 画文字
            painter.setFont(self._font)
            painter.setPen(QColor(font_color))
            painter.drawText(
                self._move_letf + self._icon.width() + self._move_space ,
                (self.height() - self._fontMetrics.height()) // 2, 
                self._fontMetrics.horizontalAdvance(self.text()),
                self._fontMetrics.height(),
                Qt.AlignLeft,
                self._text
            )
        else:
            # 画文字
            painter.setFont(self._font)
            painter.setPen(QColor(font_color))
            painter.drawText(
                self._move_letf + self._move_space,
                (self.height() - self._fontMetrics.height()) // 2, 
                self._fontMetrics.horizontalAdvance(self.text()),
                self._fontMetrics.height(),
                Qt.AlignLeft,
                self._text
            )
            

class MenuLeftSideSecondaryList:
    
    _item_hidden = list()
    _item_hidden_num = None
    
    def __init__(
        self,
        list_widget: QListWidget,
        menu_main: MenuLeftSideFirst,
        menu_name: List[str],
        sign_func: "MainWindow.display"
    ) -> None:
        super().__init__()
        self._list_widget = list_widget
        self._menu_name = menu_name
        self._sign_func = sign_func
        self._num = len(self._menu_name)

        menu_main_widget = QWidget()
        menu_main_widget.setFixedSize(menu_main._w, menu_main._h)
        layout = QVBoxLayout(menu_main_widget)
        layout.addWidget(menu_main)
        self.item_mian_nenu = QListWidgetItem(self._list_widget)
        self.item_mian_nenu.setSizeHint(QSize(menu_main._w, menu_main._h))
        
        self._list_widget.setItemWidget(self.item_mian_nenu, menu_main_widget)
        
        self.item = QListWidgetItem(self._list_widget)
        self.item.setHidden(True)
        MenuLeftSideSecondaryList._item_hidden.append(self.item)
        menu_main.clicked.connect(lambda: self.set_setHidden(self.item))
        
        self.init_menu()

    def init_menu(self) -> None:
        
        menu_widget = QWidget()
        menu_widget.setFixedSize(MenuLeftSideSecondary._w, MenuLeftSideSecondary._h * self._num)
        layout = QVBoxLayout(menu_widget)
        
        for x in range(self._num):
            button = MenuLeftSideSecondary(
                self._menu_name[x],
                self._sign_func
            )
            layout.addWidget(button)
        self.item.setSizeHint(QSize(menu_widget.width(), menu_widget.height()))
        self._list_widget.setItemWidget(self.item, menu_widget)
        
    @classmethod
    def set_setHidden(cls, item: QListWidgetItem) -> None:
        if cls._item_hidden_num is None:
            item.setHidden(not item.isHidden())
            cls._item_hidden_num = cls._item_hidden.index(item)
        else:
            if cls._item_hidden_num != cls._item_hidden.index(item):
                item_old = cls._item_hidden[cls._item_hidden_num]
                item_old.setHidden(not item_old.isHidden())
                
                item.setHidden(not item.isHidden())
                cls._item_hidden_num = cls._item_hidden.index(item)               
                
        
class MenuLeftList(QListWidget):  
    
    def __init__(self) -> None:
        super().__init__()  
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff) 
        self.setObjectName("MenuLeftList")
        self.setStyleSheet(
            """QListWidget#MenuLeftList
            {
                background-color: qlineargradient(x1:0.5, y1:0, x2:0.5, y2:1, stop:0 #f0f0f0, stop:0.9 #f0f0f0, stop:1 #f6f6f6);
                border: none;
            }
        """)

    def paintEvent(self, event: QPaintEvent) -> None:   
        event.ignore()


class StackedWidget(QStackedWidget):
    
    _wins_tuple = dict()
    
    def __init__(self, widget_zero: QWidget) -> None:
        super().__init__()
        num = super().addWidget(widget_zero)
        super().setCurrentIndex(num)
        StackedWidget._wins_tuple["wecome"] = widget_zero
        
    def addWidget(self, widget: Callable, name: str) -> None:
        result = self.indexOf(name)
        if result == 0:
            widget_new = widget()
            StackedWidget._wins_tuple[name] = widget_new
            num =  super().addWidget(widget_new)
            super().setCurrentIndex(num)
        else:
            super().setCurrentIndex(result)
        
    def indexOf(self, name: str) -> int:
        if name == "wecome":
            raise IndexError("再次传入了首页")
        if name in StackedWidget._wins_tuple:
            return super().indexOf(StackedWidget._wins_tuple[name])
        else:
            return 0
        
