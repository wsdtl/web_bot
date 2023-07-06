import os
import sys
import ujson as json
from websocket import create_connection
from websocket._core import WebSocket
from pathlib import Path
from typing import Dict, Tuple

from PyQt5.QtWidgets import (
    QApplication,
    QWidget, 
    QPushButton, 
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QLabel,
    QMenu
    )
from PyQt5.QtGui import (
    QIcon, 
    QPalette, 
    QBrush, 
    QPixmap,
    QFont, 
    QCursor,
    QPainter, 
    QPaintEvent,
    QColor, 
    QFontMetrics, 
    QLinearGradient,
    QMouseEvent
    )
from PyQt5.QtCore import (
    QThread,
    pyqtSignal, 
    QSize,
    QPoint,
    Qt, 
    QPointF
    )
from qframelesswindow import (
    FramelessWindow,
    StandardTitleBar
    )

import imge

class DrawingBubble(QLabel):
    def __init__(self, text: str, parentWidth: int, align: str):
        super().__init__()
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.fontMaxWidth = parentWidth - 100
        self.parentWidth = parentWidth
        self.align = align
        self.fontSize = 12
        self.font = QFont('Microsoft YaHei', self.fontSize)
        text, w, h = self.prepare(text)
        self.text = text
        self.w = w
        self.h = h
        self.moveSize = 10
        self.setFixedSize(self.parentWidth, self.h + self.moveSize)
            
    def paintEvent(self, event: QPaintEvent) -> None:
        # 开始绘制       
        painter = QPainter(self) 
        painter.setRenderHints(QPainter.Antialiasing | QPainter.TextAntialiasing)
        # 自定义的绘画方法
        if self.align == "left":
            self.drawTextLeft(event, painter)
        elif self.align == "right":
            self.drawTextRight(event, painter)
        elif self.align == "center":
            self.drawTextCenter(event, painter)
        else:
            pass
            
    def drawTextCenter(self, event: QPaintEvent, painter: QPainter) -> None:
        # 设置笔
        painter.setFont(QFont('Microsoft YaHei', 16))
        # 文字颜色
        textColor = QColor(0, 0, 0)
        textColor.setNamedColor('#ffd2b6')
        # 画出文本
        painter.setPen(textColor)
        painter.drawText(event.rect(), Qt.AlignCenter, self.text)
    
    def drawTextLeft(self, event: QPaintEvent, painter: QPainter) -> None:
        # 设置笔
        painter.setFont(self.font)
        # 渐变
        backgroundColor = QLinearGradient(QPointF(100, 100), QPointF(400, 400))
        blue = QColor(0, 0, 0)
        blue.setNamedColor('#9aefff')
        white = QColor(0, 0, 0)
        white.setNamedColor('#d1eff3')
        # 背景颜色
        backgroundColor.setColorAt(0, blue)
        backgroundColor.setColorAt(1, white)
        # 阴影颜色
        borderColor= QColor(0, 0, 0)
        borderColor.setNamedColor('#d3d3d3')
        # 文字颜色
        textColor = QColor(0, 0, 0)
        # 背景
        painter.setBrush(backgroundColor)
        painter.drawRoundedRect(self.moveSize + 1, self.moveSize + 1, self.w -2 , self.h -2, 6, 6)
        # 阴影
        painter.setPen(borderColor)
        painter.drawRoundedRect(self.moveSize, self.moveSize, self.w , self.h, 6, 6)
        # 画出文本
        painter.setPen(textColor)
        painter.drawText(self.moveSize + 5, self.moveSize, self.w, self.h, Qt.AlignLeft, self.text)

    def drawTextRight(self, event: QPaintEvent, painter: QPainter) -> None:
        # 设置笔
        painter.setFont(self.font)
         # 渐变
        backgroundColor = QLinearGradient(QPointF(100, 100), QPointF(400, 400))
        blue = QColor(0, 0, 0)
        blue.setNamedColor('#9aefff')
        white = QColor(0, 0, 0)
        white.setNamedColor('#d1eff3')
        # 背景颜色
        backgroundColor.setColorAt(0, blue)
        backgroundColor.setColorAt(1, white)
        # 阴影颜色
        borderColor= QColor(0, 0, 0)
        borderColor.setNamedColor('#d3d3d3')
        # 文字颜色
        textColor = QColor(0, 0, 0)
        # 右边偏移差量
        moveRight = self.parentWidth - self.w
        # 背景
        painter.setBrush(backgroundColor)
        painter.drawRoundedRect(moveRight -self.moveSize + 1,  self.moveSize + 1, self.w -2 , self.h -2, 6, 6)
        # 阴影
        painter.setPen(borderColor)
        painter.drawRoundedRect(moveRight - self.moveSize, self.moveSize, self.w , self.h, 6, 6)
        # 画出文本
        painter.setPen(textColor)
        painter.drawText(moveRight - self.moveSize + 5, self.moveSize, self.w, self.h, Qt.AlignLeft, self.text)
    
    def prepare(self, text: str) -> Tuple[str, int, int]:
        # 字符长度计算
        font = QFontMetrics(self.font)
        textLen = 0
        textNew = ""
        textMaxLen = 0
        for x in text:
            textNew += x
            if x != "\n":
                textLen +=  font.width(x)
            if x == '\n':
                if textLen > textMaxLen:
                    textMaxLen = textLen
                textLen = 0
            if textLen >= self.fontMaxWidth:
                if textLen > textMaxLen:
                    textMaxLen = self.fontMaxWidth
                textLen = 0
                textNew += '\n'
            if textLen > textMaxLen:
                textMaxLen = textLen
        textNew = textNew.replace("\n\n","\n")        
        textNew = textNew.rstrip()
        fontRow = textNew.count("\n") + 1
        return textNew, int(textMaxLen) + 15, int(font.height() * fontRow) + 5
    
    def getText(self) -> str:
        return self.text
    
class ListWidget(QListWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setContextMenuPolicy(Qt.CustomContextMenu)  # 创建QMenu信号事件
        self.customContextMenuRequested.connect(self.showMenu)
        self.contextMenu = QMenu(self)
        self.rCpoy = self.contextMenu.addAction("复制")
        self.rCpoy.triggered.connect(self.copy)
        self.rRemove = self.contextMenu.addAction("删除")
        self.rRemove.triggered.connect(self.remove)
        self.contextMenu.setStyleSheet(
            "QMenu{ background: lightgray; color: #000000;}"  
            "QMenu::item:text { padding-left: 10px;padding-right: 10px;}"
            "QMenu::item:selected{ color: #1aa3ff;background-color: #e6f5ff;border-radius: 4px;}"
        )
        
    #获取选择行的内容
    def selectedText(self) -> str:
        item = self.selectedItems()
        if item:
            text = item[0].data(Qt.UserRole)
        else:
            text = ""
        return text
        
    def copy(self) -> None:
        clipboard = QApplication.clipboard()
        clipboard.setText(self.selectedText())
        
    def remove(self) -> None:
        item = self.selectedItems()
        if item:
            row = self.row(item[0])
            self.takeItem(row)

    def showMenu(self, pos: QPoint):
        if self.selectedItems():
        # pos 鼠标位置
        # 菜单显示前,将它移动到鼠标点击的位置
            self.contextMenu.popup(QCursor.pos())  # 在鼠标位置显示
        
    def mousePressEvent(self, event: QMouseEvent) -> None:
        super().mousePressEvent(event)
        event.ignore()
                
    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        super().mouseMoveEvent(event)
        event.ignore()
            
    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        super().mouseReleaseEvent(event)
        event.ignore()
    

class WebsockrecvThread(QThread):
    """消息接收进程"""
    def __init__(self, websockReceiveSingal: pyqtSignal, 
                 logInfoSingal: pyqtSignal, 
                 connectionsSinagl: pyqtSignal,
                 websock: WebSocket,
                 userId: str
        ) -> None:
        super().__init__()
        self.websockReceiveSingal: pyqtSignal = websockReceiveSingal
        self.logInfoSingal: pyqtSignal = logInfoSingal
        self.connectionsSinagl: pyqtSignal = connectionsSinagl
        self.websock: WebSocket = websock
        self.userId: str = userId
        
    def run(self) -> None:
            self.HelloData = {
                "msg" : "i miss you xiaonan",
                "user_id": self.userId
            }
            try:
                self.websock.send(self.toJson(self.HelloData))
                self.logInfoSingal.emit(f"账户{self.userId}登录成功")
                while True:
                    msg = self.websock.recv()
                    msg = json.loads(msg)
                    if "msg" in msg:
                        self.websockReceiveSingal.emit(msg["msg"]) 
            except Exception as e:
                self.logInfoSingal.emit(f"与服务器已失去连接，请重新登录")
            finally:
                self.connectionsSinagl.emit(self.userId)
            return    
        
    def toJson(self, data: dict) -> str:
        return json.dumps(data)

class WebsockSendThread(QThread):
    """消息发送进程"""
    def __init__(self,
                 msg: str,
                 userId: str,
                 websock: WebSocket
        ) -> None:
        super().__init__()
        self.msg: str = msg
        self.userId: str = userId
        self.websock: WebSocket = websock
        
    def run(self) -> None:
            try:
                self.websock.send(self.toJson(self.msg, self.userId))
            except Exception as e:
                pass
            return    
        
    def toJson(self, msg: str, userId: str) -> str:
        data = {
            "msg": msg,
            "user_id": userId
        }
        return json.dumps(data) 

class Window(FramelessWindow):
    """窗口监控类"""
    PATH = Path() / os.path.dirname(os.path.abspath(__file__))
    # 声明一个信号 只能放在函数的外面
    websockReceiveSingal = pyqtSignal(str)
    logInfoSingal = pyqtSignal(str)
    sendSingal = pyqtSignal(str)
    connectionsSinagl = pyqtSignal(str)
    
    def __init__(self) -> None:
        super().__init__()
        self.connections :Dict[str: WebSocket] = {}
        self.thread: Dict[str: QThread] = {}
        self.name: str = "用户"
        self.botName: str = "晓楠"
        self.wsUrl: str = "ws://dengxiaonan.cn:8090/xiaonan"
        self.init_ui()

    def init_ui(self) -> None:
        """初始化"""
        self.initWindow()
        # 发送按钮
        self.pushButtonSend = QPushButton(self)
        self.pushButtonSend.setToolTip("发送")
        self.pushButtonSend.setFixedSize(QSize(50, 40))
        self.pushButtonSend.move(540, 580)
        # self.pushButtonSend.setIcon(QIcon(str(self.PATH / "img" / "send.png")))
        self.pushButtonSend.setIcon(QIcon(QPixmap(':/img/send.png')))
        self.pushButtonSend.setStyleSheet(
            "QPushButton{ background: rgba(225,225,225,100);border-style: outset;}"
        )
        self.pushButtonSend.setShortcut (Qt.Key_Return )
        # 隐藏按钮
        self.pushButtonEye = QPushButton(self)
        self.pushButtonEye.setToolTip("查看账号")
        self.pushButtonEye.setFixedSize(QSize(50, 30))
        self.pushButtonEye.move(190, 35)
        # self.pushButtonEye.setIcon(QIcon(str(self.PATH / "img" / "eye.png")))
        self.pushButtonEye.setIcon(QIcon(QPixmap(':/img/eye.png')))
        self.pushButtonEye.setStyleSheet(
            "QPushButton{ background: rgba(225,225,225,100);border-style: outset;}"
        )
        # 登录按钮
        self.pushButtonSing = QPushButton(self)
        self.pushButtonSing.setToolTip("登录")
        self.pushButtonSing.setFixedSize(QSize(50, 30))
        self.pushButtonSing.move(420, 35)
        # self.pushButtonSing.setIcon(QIcon(str(self.PATH / "img" / "sing.png")))
        self.pushButtonSing.setIcon(QIcon(QPixmap(':/img/sing.png')))
        self.pushButtonSing.setStyleSheet(
            "QPushButton{ background: rgba(225,225,225,100);border-style: outset;}"
        )
        # 登出按钮
        self.pushButtonExit = QPushButton(self)
        self.pushButtonExit.setToolTip("登出")
        self.pushButtonExit.setFixedSize(QSize(50, 30))
        self.pushButtonExit.move(480, 35)
        # self.pushButtonExit.setIcon(QIcon(str(self.PATH / "img" / "exit.png")))
        self.pushButtonExit.setIcon(QIcon(QPixmap(':/img/exit.png')))
        self.pushButtonExit.setStyleSheet(
            "QPushButton{ background: rgba(225,225,225,100);border-style: outset;}"
        )
        # 清空按钮
        self.pushButtonClear = QPushButton(self)
        self.pushButtonClear.setToolTip("清空消息框")
        self.pushButtonClear.setFixedSize(QSize(50, 30))
        self.pushButtonClear.move(540, 35)
        # self.pushButtonClear.setIcon(QIcon(str(self.PATH / "img" / "clear.png")))
        self.pushButtonClear.setIcon(QIcon(QPixmap(':/img/clear.png')))
        self.pushButtonClear.setStyleSheet(
            "QPushButton{ background: rgba(225,225,225,100);border-style: outset;}"
        )
        # 账户输入窗口
        self.userId = QLineEdit(self)
        self.userId.setPlaceholderText("使用前请先输入账户ID")
        self.userId.setFixedSize(QSize(170, 30))
        self.userId.move(10, 35)
        self.userId.setEchoMode(QLineEdit.Password)
        self.userId.setFocus() # 设置焦点
        self.userId.setContextMenuPolicy(Qt.NoContextMenu) # 取消右键菜单
        self.userId.setStyleSheet(
            "QLineEdit{ background: rgba(225,225,225,100);}"
            )
        # 用户名输入窗口
        self.userName = QLineEdit(self)
        self.userName.setPlaceholderText("昵称 默认为 用户")
        self.userName.setFixedSize(QSize(160, 30))
        self.userName.move(250, 35)
        self.userName.setContextMenuPolicy(Qt.NoContextMenu) # 取消右键菜单
        self.userName.setStyleSheet(
            "QLineEdit{ background: rgba(225,225,225,100);}"
        )
        # 文字发送窗口 
        self.sendTxt = QLineEdit(self)
        self.sendTxt.setPlaceholderText("请输入文字")
        self.sendTxt.setFixedSize(QSize(520, 40))
        self.sendTxt.move(10, 580)
        self.sendTxt.setContextMenuPolicy(Qt.NoContextMenu) # 取消右键菜单
        self.sendTxt.setStyleSheet(
            "QLineEdit{ background: rgba(225,225,225,100);}"
        )
        # 对话框
        self.listWidget = ListWidget()
        self.listWidget.setParent(self)
        self.listWidget.setFixedSize(QSize(580, 495))
        self.listWidget.move(10, 75)
        self.listWidget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff) # 删除垂直条
        self.listWidget.setStyleSheet(
            "QListWidget{ background: rgba(225,225,225,100);font-family: Microsoft YaHei;}"
            "QListWidget::item:selected:!active{ border-width:none; background:transparent;}"
        )
        widget = DrawingBubble("欢迎使用晓楠客户端", self.listWidget.width(), "center")
        item = QListWidgetItem()  # 创建QListWidgetItem对象
        item.setData(Qt.UserRole, widget.getText())
        item.setSizeHint(QSize(self.listWidget.width() - 20, widget.h + widget.moveSize))
        self.listWidget.addItem(item)
        self.listWidget.setItemWidget(item, widget)
        # 绑定槽
        self.pushButtonEye.pressed.connect(self.eyePressed)
        self.pushButtonEye.released.connect(self.eyeReleased)
        self.pushButtonSing.clicked.connect(self.sing)
        self.pushButtonExit.clicked.connect(self.exit)
        self.pushButtonSend.clicked.connect(self.send)
        self.pushButtonClear.clicked.connect(self.clear)
        # 绑定信号
        self.websockReceiveSingal.connect(self.windowTextReceiv)
        self.logInfoSingal.connect(self.windowTextLog)
        self.sendSingal.connect(self.indowTextSend)
        self.connectionsSinagl.connect(self.connectionsClose)
        return
    
    def initWindow(self) -> None:
        """初始化窗口"""
        self.setFixedSize(600, 630)
        self.setTitleBar(StandardTitleBar(self))
        self.titleBar.setDoubleClickEnabled(False)
        self.titleBar.maxBtn.deleteLater()  # 删除最大化按钮
        self.setResizeEnabled(False)  # 禁止手动拉伸
        self.moveFlag = False   # 鼠标移动标志
        # self.setMouseTracking(True) # 鼠标跟踪
        self.setWindowIcon(QIcon(':/img/bot.png'))  # 图标
        self.setWindowTitle('Xiaonan') # 标题
        self.setStyleSheet(
            "border-radius:8px;font-family: Microsoft YaHei;font-size: 16px;"
        )
        palette = QPalette()
        # palette.setBrush(QPalette.Background, QBrush(QPixmap(str(self.PATH / "img" / "back.png"))))  
        palette.setBrush(QPalette.Background, QBrush(QPixmap(':/img/back.png')))
        self.setPalette(palette)
        # 窗口打开位置，默认在屏幕中间
        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)
    
    def sing(self) -> None:
        """登录"""   
        user_id = self.userId.text()
        if not user_id:
            self.logInfoSingal.emit("请先填写账户ID")
            return
        if not isinstance(user_id, str):
            self.logInfoSingal.emit("账户ID应为纯数字")
            return
        if user_id in self.connections:
            self.logInfoSingal.emit(f"账户{user_id}已登录，请不要重复登录") 
            return  
        # 鼠标繁忙
        self.setCursor(Qt.BusyCursor)
        self.logInfoSingal.emit("正在登录请稍后")
        self.userId.setReadOnly(True)
        try:  
            websocket = create_connection(self.wsUrl)
            self.connections[user_id] = websocket
            recvThread = WebsockrecvThread(
            self.websockReceiveSingal,
            self.logInfoSingal,
            self.connectionsSinagl,
            self.connections[user_id],
            user_id
            )  # 创建线程
            recvThread.start()  # 开始线程
            self.thread[user_id] = recvThread 
        except ConnectionRefusedError:
            self.logInfoSingal.emit(f"服务器掉线了") 
        except Exception:
            self.logInfoSingal.emit(f"服务出错了") 
        # 鼠标恢复
        self.setCursor(Qt.ArrowCursor)    
        return

    def eyePressed(self) -> None:
        """按下眼睛"""
        self.userId.setEchoMode(QLineEdit.Normal)
        return
    
    def eyeReleased(self) -> None:
        """松开眼睛"""    
        self.userId.setEchoMode(QLineEdit.Password)
        return
   
    def exit(self) -> None:
        """退出登录"""
        if not self.connections:
            self.logInfoSingal.emit("还没有登录呢")
            return
        for ws in self.connections.values():
            ws.close()
        for thread in self.thread.values():
            thread.quit()
        self.connections.clear()
        self.thread.clear()
        self.userId.setReadOnly(False) 
        return
    
    def send(self) -> None:
        """发送信息"""
        user_id = self.userId.text()
        if not user_id:
            self.logInfoSingal.emit("请先填写账户ID")
            return
        if not user_id in self.connections:
            self.logInfoSingal.emit("还没有登录呢")  
            return
        msg = self.sendTxt.text()
        if msg and isinstance(msg, str):
            self.SendThread = WebsockSendThread(msg, user_id, self.connections[user_id])  # 创建线程
            self.SendThread.start()  # 开始线程
            self.sendSingal.emit(msg)
            self.sendTxt.clear()
            return
        else:
            return
    
    def clear(self) -> None:
        """清屏"""
        self.listWidget.clear()
        return
    
    def getName(self) -> str:
        """获取用户昵称"""
        name = str(self.userName.text())
        if name:
            return self.userName.text()
        else:
            return self.name

    def connectionsClose(self) -> None:
        """连接意外断开"""
        for ws in self.connections.values():
            ws.close()
        for thread in self.thread.values():
            thread.quit()
        self.connections.clear()
        self.thread.clear()
        self.userId.setReadOnly(False) 
        return
    
    def windowTextReceiv(self, msg) -> None:
        """服务器输出"""
        widget = DrawingBubble(msg, self.listWidget.width(), "left")
        item = QListWidgetItem()  # 创建QListWidgetItem对象
        item.setData(Qt.UserRole, widget.getText())
        item.setSizeHint(QSize(self.listWidget.width() - 20, widget.h + widget.moveSize))
        self.listWidget.addItem(item)
        self.listWidget.setItemWidget(item, widget)
        # 定位到最后一行
        self.listWidget.setCurrentRow(self.listWidget.count() - 1)
        self.listWidget.repaint()
        return
    
    def windowTextLog(self, msg) -> None:
        """日志类输出"""
        widget = DrawingBubble(msg, self.listWidget.width(), "center")
        item = QListWidgetItem()  # 创建QListWidgetItem对象
        item.setData(Qt.UserRole, widget.getText())
        item.setSizeHint(QSize(self.listWidget.width() - 20, widget.h + widget.moveSize))
        self.listWidget.addItem(item)
        self.listWidget.setItemWidget(item, widget)
        # 定位到最后一行
        self.listWidget.setCurrentRow(self.listWidget.count() - 1)
        self.listWidget.repaint()
        return
     
    def indowTextSend(self, msg) -> None:
        """用户输出"""
        widget = DrawingBubble(msg, self.listWidget.width(), "right")
        item = QListWidgetItem()  # 创建QListWidgetItem对象
        item.setData(Qt.UserRole, widget.getText())
        item.setSizeHint(QSize(self.listWidget.width() - 20, widget.h + widget.moveSize))
        self.listWidget.addItem(item)
        self.listWidget.setItemWidget(item, widget)
        # 定位到最后一行
        self.listWidget.setCurrentRow(self.listWidget.count() - 1)
        self.listWidget.repaint()
        return
    
    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.LeftButton:
            self.moveFlag = True
            self.mouseX = event.globalX()
            self.mouseY = event.globalY()
            self.winX = self.x()
            self.winY = self.y()
                
    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if self.moveFlag:
            self.move(
                self.winX + event.globalX() - self.mouseX, 
                self.winY + event.globalY() - self.mouseY
            )
            
    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        self.moveFlag = False
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())