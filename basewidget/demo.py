import sys
from PySide6.QtWidgets import QLabel, QApplication
from PySide6.QtGui import QPixmap
from basewidget import MainWindow
# 移动到主目录下运行

class Label1(QLabel):
    
    def __init__(self):
        super().__init__()
        self.setText("1")
        self.setStyleSheet("background-color: #1ecc94;")
        
class Label2(QLabel):
    
    def __init__(self):
        super().__init__()
        self.setText("2")
        self.setStyleSheet("background-color: red;")

class Label3(QLabel):
    
    def __init__(self):
        super().__init__()
        self.setText("3")
        self.setStyleSheet("background-color: blue;")

class Label4(QLabel):
    
    def __init__(self):
        super().__init__()
        self.setText("4")
        self.setStyleSheet("background-color: black;")

class Window(MainWindow):
    
    def __init__(self) -> None:
        super().__init__()
        # 添加菜单
        self.addMuen("菜单",QPixmap(":/img/menu/produce_data"),["我是菜单1","我是菜单2","我是菜单3","我是菜单4"])
        # 添加窗口
        self.addWidget(Label1, "我是菜单1")
        self.addWidget(Label2, "我是菜单2")
        self.addWidget(Label3, "我是菜单3")
        self.addWidget(Label4, "我是菜单4")
        


if __name__ == '__main__':
    app = QApplication(sys.argv)
    windows = Window()
    windows.show()
    sys.exit(app.exec())



