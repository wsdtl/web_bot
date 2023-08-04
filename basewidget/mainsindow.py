from typing import List, Callable, Optional
from PySide6.QtGui import (
    QPixmap,
    Qt
)
from PySide6.QtWidgets import (
    QWidget,
    QApplication, 
    QHBoxLayout, 
    QVBoxLayout,
    QMainWindow,
    QApplication
)

from .dialog import DialogOver
from .title import MyTip
from .wecome import WecomeWidget
from .menu_index import(
    MenuLeftSideFirst,
    MenuLeftSideSecondaryList,
    MenuLeftList,
    StackedWidget
)

class MainWindow(QMainWindow):
    
    _widget = dict()
    
    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("MainWindow")
        self.setStyleSheet(
            """QWidget#MainWindow
            {
                background-color: #f6f6f6;
            }
        """)
        self._initUI_()
        
    def _initUI_(self) -> None:
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        self.stat = self.statusBar()                        # 开启状态栏
        self.widget = QWidget()
        self.setCentralWidget(self.widget)
        self.layout = QVBoxLayout(self.widget)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)          # 消除主布局间隙
        
        self.tip = MyTip(self)
        self.layout.addWidget(self.tip)
        
        self.layout_two = QHBoxLayout()                     # 添加二级布局
        self.layout.addLayout(self.layout_two)
        
        self.left_menu = MenuLeftList()                     # 初始化菜单
        self.left_menu.setFixedWidth(MenuLeftSideFirst._w + 10)  
        self.layout_two.addWidget(self.left_menu)
        # self.layout_two.addSpacing(10)
        self.right_widget = StackedWidget(WecomeWidget())   # 初始化窗口
        self.layout_two.addWidget(self.right_widget)
        
        self._showNormal()
    
    def addMuen(
            self,
            first_menu: str,
            first_menu_img: QPixmap, 
            second_menu: List[str],
        ) -> None:
        menu = MenuLeftSideFirst(first_menu, first_menu_img)
        MenuLeftSideSecondaryList(
            self.left_menu,
            menu,
            second_menu,
            self.display
        )  
    
    def display(self, name: str) -> None:
        self.add_message(name)
        self.add_popup(name)
        if name in MainWindow._widget:
            widget = MainWindow._widget[name]
            self.right_widget.addWidget(widget, name)
            
    @classmethod
    def addWidget(cls, widget: Callable, name: str) -> None:
        cls._widget[name] = widget
    
    def _showNormal(self) -> None:
        self.resize(1000, 800)
        desktop = QApplication.instance().screens()[0].size()
        self.move((desktop.width() - self.width()) // 2, (desktop.height() - self.height()) // 2)

    def add_message(self, text: str) -> None:
        self.stat.showMessage(text)
    
    def add_popup(
        self, 
        text: str, 
        title : Optional[str] = "",
        flag: Optional[str] = "success"
    ) -> None:
        DialogOver(self, text, title, flag)
            