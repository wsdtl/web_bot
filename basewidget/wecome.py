from PySide6.QtWidgets import QLabel
from PySide6.QtGui import  QPixmap
from PySide6.QtCore import QSize, Qt

from . import rc

class WecomeWidget(QLabel):
    
    _w = 800
    _h = 600
    
    def __init__(self) -> None:
        super().__init__()
        self._size = QSize(self._w, self._h)
        self.init_ui() 
        
    def init_ui(self) -> None:
        self.setAlignment(Qt.AlignCenter)
        pix = QPixmap(":/image/wecome.png").scaled(self._size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.setPixmap(pix)

        