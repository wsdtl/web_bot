import sys
from PySide6.QtWidgets import QLabel, QApplication
from PySide6.QtGui import QPixmap
from basewidget.mainsindow import MainWindow


class Label1(QLabel):
    
    def __init__(self):
        super().__init__()
        self.setText("1")
        
class Label2(QLabel):
    
    def __init__(self):
        super().__init__()
        self.setText("2")

class Label3(QLabel):
    
    def __init__(self):
        super().__init__()
        self.setText("3")

class Label4(QLabel):
    
    def __init__(self):
        super().__init__()
        self.setText("4")

class Window(MainWindow):
    
    def __init__(self) -> None:
        super().__init__()
        # 添加菜单
        self.addMuen("菜单",QPixmap(":/img/menu/produce_data"),["1","2","3","4"])
        # 添加窗口
        self.addWidget(Label1, "1")
        self.addWidget(Label2, "2")
        self.addWidget(Label3, "3")
        self.addWidget(Label4, "4")
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    windows = Window()
    windows.show()
    sys.exit(app.exec())

