import sys
from PySide6.QtGui import(
    QPixmap
)
from PySide6.QtWidgets import (
    QWidget,
    QApplication, 
    QHBoxLayout, 
    QVBoxLayout,
    QLabel, 
    QMainWindow,
    QStyleFactory
    )

from menu import(
    MenuLeftSideFirst,
    MenuLeftSideSecondaryList,
    MenuLeftList,
    StackedWidget
)
from wins import (
    WecomeWidget
)
import imge

class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        "初始化背景窗口"
        self.main_widget = QWidget()                        #设置窗口初始位置和大小
        self.main_widget.setObjectName("main_widget")
        self.main_widget.setStyleSheet(
            """QWidget#main_widget
            {
                background: #ffffff;
            }
        """)
        self.setCentralWidget(self.main_widget)
        self.init_ui()
        
    def init_ui(self) -> None:
        """初始化整体布局"""
        self.layout_main = QHBoxLayout()                    # 设置整体布局
        self.layout_main.setSpacing(0)
        self.layout_main.setContentsMargins(0, 0, 0, 0)     # 消除主布局间隙
        self.main_widget.setLayout(self.layout_main)
        # ///////////////////////////////////////////
        self.layout_left = QVBoxLayout()                    # 设置菜单布局 left
        self.init_left()                                    # 初始化菜单布局 left
        self.layout_main.addLayout(self.layout_left)
        # ///////////////////////////////////////////
        wecome = WecomeWidget()
        self.widget_right = StackedWidget(wecome)           # 初始化界面布局 right
        # self.layout_main.addSpacing(10)                   # 添加空白
        self.layout_main.addWidget(self.widget_right)
    
    def init_left(self) -> None:
        """初始化左侧布局"""
        self.leftlist = MenuLeftList()
        self.leftlist.setObjectName("leftlist")
        self.leftlist.setStyleSheet(
            """QWidget#leftlist
            {
                background: #f0f0f0;
                border: none;
            }
        """)
        self.leftlist.setFixedWidth(MenuLeftSideFirst._w + 10)
        self.layout_left.addWidget(self.leftlist)
        
        data_find = MenuLeftSideFirst("物料查找", QPixmap(":/img/menu/data_find.png"))
        MenuLeftSideSecondaryList(
            self.leftlist,
            data_find,
            ["数据库查找"],
            self.display
        )
        locate = MenuLeftSideFirst("小车定位", QPixmap(":/img/menu/locate"))
        MenuLeftSideSecondaryList(
            self.leftlist,
            locate,
            ["蓝牙定位"],
            self.display
        )
        compute = MenuLeftSideFirst("数据计算", QPixmap(":/img/menu/compute.png"))
        MenuLeftSideSecondaryList(
            self.leftlist,
            compute,
            ["视觉计算"],
            self.display
        )    
        add_data = MenuLeftSideFirst("数据录入", QPixmap(":/img/menu/add_data.png"))
        MenuLeftSideSecondaryList(
            self.leftlist,
            add_data,
            ["手动录入"],
            self.display
        )
        produce_data = MenuLeftSideFirst("生成管理", QPixmap(":/img/menu/produce_data"))
        MenuLeftSideSecondaryList(
            self.leftlist,
            produce_data,
            ["生产数据"],
            self.display
        )     
        sys_set = MenuLeftSideFirst("设置", QPixmap(":/img/menu/set.png"))
        MenuLeftSideSecondaryList(
            self.leftlist,
            sys_set,
            ["系统设置"],
            self.display
        )   
        help_data = MenuLeftSideFirst("帮助", QPixmap(":/img/menu/help.png"))
        MenuLeftSideSecondaryList(
            self.leftlist,
            help_data,
            ["获取帮助"],
            self.display
        )
        
    def display(self, text: str):
        """更新右侧布局"""
        if text == "数据库查找":
            q = QLabel(text)
            self.widget_right.addWidget(q, text)
        elif text == "蓝牙定位":
            q = QLabel(text)
            self.widget_right.addWidget(q, text)
        elif text == "视觉计算":
            q = QLabel(text)
            self.widget_right.addWidget(q, text)
        elif text == "手动录入":
            q = QLabel(text)
            self.widget_right.addWidget(q, text)
        elif text == "生产数据":
            q = QLabel(text)
            self.widget_right.addWidget(q, text)
        elif text == "系统设置":
            q = QLabel(text)
            self.widget_right.addWidget(q, text)
        elif text == "获取帮助":
            a = self.widget_right.count()
            print(a)
            
            
                    
if __name__ == "__main__":

    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create("Fusion"))  #fusion风格
    window = MainWindow()
    window.showMaximized()
    window.show()
    app.exec()