from typing import List, Callable
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QWidget,
    QApplication, 
    QHBoxLayout, 
    QVBoxLayout,
    QMainWindow,
    QApplication
)

# from .title import WinTitle
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
        # self.moveFlag = False
        self._initUI_()
        
    def _initUI_(self) -> None:
        self.stat = self.statusBar()                        # 开启状态栏
        self.widget = QWidget()
        self.setCentralWidget(self.widget)
        self.layout = QVBoxLayout(self.widget)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)          # 消除主布局间隙
        
        # self.title = WinTitle(self)
        # self.layout.addWidget(self.title)
        
        self.layout_two = QHBoxLayout()                     # 添加二级布局
        self.layout.addLayout(self.layout_two)
        
        self.left_menu = MenuLeftList()                     # 初始化菜单
        self.left_menu.setFixedWidth(MenuLeftSideFirst._w + 10)  
        self.layout_two.addWidget(self.left_menu)
        self.layout_two.addSpacing(10)
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
        print(self.right_widget.count())
        if name in MainWindow._widget:
            widget = MainWindow._widget[name]
            self.right_widget.addWidget(widget(), name)
            
    @classmethod
    def addWidget(cls, widget: Callable, name: str) -> None:
        cls._widget[name] = widget
    
    def _showNormal(self) -> None:
        self.resize(1000, 800)
        desktop = QApplication.instance().screens()[0].size()
        self.move((desktop.width() - self.width()) // 2, (desktop.height() - self.height()) // 2)

    def add_message(self, text: str) -> None:
        self.stat.showMessage(text)
            
    # def mousePressEvent(self, event: QMouseEvent) -> None:
    #     if event.button() == Qt.LeftButton:
    #         self.moveFlag = True
    #         self.pos_star = event.globalPosition().toPoint()
    #         self.win_pos = self.pos()

    # def mouseMoveEvent(self, event: QMouseEvent) -> None:
    #     if self.moveFlag:
    #         self.move(self.win_pos + event.globalPosition().toPoint() - self.pos_star)
            
    # def mouseReleaseEvent(self, event: QMouseEvent) -> None:
    #     self.moveFlag = False