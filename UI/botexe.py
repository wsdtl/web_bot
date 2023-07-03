import os
import sys
import ujson as json
from websocket import create_connection
from websocket._core import WebSocket
from pathlib import Path
from typing import Dict

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QTextBrowser, QLineEdit
from PyQt5.QtGui import QIcon, QPalette, QBrush, QPixmap
from PyQt5.QtCore import QThread, pyqtSignal, QSize, Qt
from qframelesswindow import FramelessWindow, StandardTitleBar

import imge

SendHtmlLeft = """           
<html>
    <body>
        <hr style="margin: 0px;"/>
        <p style="text-align: left;margin: 1px;color: #ffdd9a;font-size: 18px;font-weight:bold;font-style:oblique;">{0}</p>
        <p style="text-align: left;margin: 1px;font-size: 18px;">{1}</p>
    </body>
</html>          
"""
SendHtmlRight = """
<html>
    <body>
        <hr style="margin: 0px;"/>
        <p style="text-align: right;margin: 1px;color: #ffdd9a;font-size: 18px;font-weight:bold;font-style:oblique;">{0}</p>
        <p style="text-align: right;margin: 1px;font-size: 18px;">{1}</p>
    </body>
</html>             
"""
SendHtmlErro = """
<html>
    <body>
        <hr style="margin: 0px;"/>
        <h3 style="text-align: center;margin: 1px;color: #9aefff;">{0}</h3>
    </body>
</html>         
"""       
SendHtmlHello = """
<html>
    <body>
        <h2 style="text-align: center;margin: 1px;color: #9aefff;">欢迎使用晓楠客户端</h2>
    </body>
</html>         
"""

class WebsockRecvThread(QThread):
    """消息接收进程"""
    def __init__(self, WebsockReceiveSingal: pyqtSignal, 
                 LogInfoSingal: pyqtSignal, 
                 ConnectionsSinagl: pyqtSignal,
                 websock: WebSocket,
                 UserId: str
        ):
        super().__init__()
        self.WebsockReceiveSingal: pyqtSignal = WebsockReceiveSingal
        self.LogInfoSingal: pyqtSignal = LogInfoSingal
        self.ConnectionsSinagl: pyqtSignal = ConnectionsSinagl
        self.websock: WebSocket = websock
        self.UserId: str = UserId
        
    def run(self) -> None:
            self.HelloData = {
                "msg" : "i miss you xiaonan",
                "user_id": self.UserId
            }
            try:
                self.websock.send(self.to_json(self.HelloData))
                self.LogInfoSingal.emit(f"账户{self.UserId}登录成功")
                while True:
                    msg = self.websock.recv()
                    msg = json.loads(msg)
                    if "msg" in msg:
                        self.WebsockReceiveSingal.emit(msg["msg"]) 
            except Exception as e:
                self.LogInfoSingal.emit(f"与服务器已失去连接，请重新登录")
            finally:
                self.ConnectionsSinagl.emit(self.UserId)
            return    
        
    def to_json(self, data: dict) -> str:
        return json.dumps(data)

class WebsockSendThread(QThread):
    """消息发送进程"""
    def __init__(self,
                 msg: str,
                 UserId: str,
                 websock: WebSocket
        ):
        super().__init__()
        self.msg: str = msg
        self.UserId: str = UserId
        self.websock: WebSocket = websock
        
    def run(self) -> None:
            try:
                self.websock.send(self.to_json(self.msg, self.UserId))
            except Exception as e:
                pass
            return    
        
    def to_json(self, msg: str, UserId: str) -> str:
        data = {
            "msg": msg,
            "user_id": UserId
        }
        return json.dumps(data) 

class Window(FramelessWindow):
    """窗口监控类"""
    PATH = Path() / os.path.dirname(os.path.abspath(__file__))
    # 声明一个信号 只能放在函数的外面
    WebsockReceiveSingal = pyqtSignal(str)
    LogInfoSingal = pyqtSignal(str)
    SendSingal = pyqtSignal(str)
    ConnectionsSinagl = pyqtSignal(str)
    
    def __init__(self) -> None:
        super().__init__()
        self.connections :Dict[str: WebSocket] = {}
        self.thread: Dict[str: QThread] = {}
        self.name: str = "用户"
        self.BotName: str = "晓楠"
        self.WsUrl: str = "ws://dengxiaonan.cn:8090/xiaonan"
        self.init_ui()

    def init_ui(self) -> None:
        """初始化"""
        self.InitWindow()
        # 发送按钮
        self.pushButtonSend = QPushButton(self)
        self.pushButtonSend.setToolTip("发送")
        self.pushButtonSend.setFixedSize(QSize(50, 40))
        self.pushButtonSend.move(540, 580)
        # self.pushButtonSend.setIcon(QIcon(str(self.PATH / "img" / "send.png")))
        self.pushButtonSend.setIcon(QIcon(QPixmap(':/img/send.png')))
        self.pushButtonSend.setStyleSheet("background: rgba(225,225,225,100);border-style: outset;")
        self.pushButtonSend.setShortcut (Qt.Key_Return )
        # 隐藏按钮
        self.pushButtonEye = QPushButton(self)
        self.pushButtonEye.setToolTip("查看账号")
        self.pushButtonEye.setFixedSize(QSize(50, 30))
        self.pushButtonEye.move(190, 35)
        # self.pushButtonEye.setIcon(QIcon(str(self.PATH / "img" / "eye.png")))
        self.pushButtonEye.setIcon(QIcon(QPixmap(':/img/eye.png')))
        self.pushButtonEye.setStyleSheet("background: rgba(225,225,225,100);border-style: outset;")
        # 登录按钮
        self.pushButtonSing = QPushButton(self)
        self.pushButtonSing.setToolTip("登录")
        self.pushButtonSing.setFixedSize(QSize(50, 30))
        self.pushButtonSing.move(420, 35)
        # self.pushButtonSing.setIcon(QIcon(str(self.PATH / "img" / "sing.png")))
        self.pushButtonSing.setIcon(QIcon(QPixmap(':/img/sing.png')))
        self.pushButtonSing.setStyleSheet("background: rgba(225,225,225,100);border-style: outset;")
        # 登出按钮
        self.pushButtonExit = QPushButton(self)
        self.pushButtonExit.setToolTip("登出")
        self.pushButtonExit.setFixedSize(QSize(50, 30))
        self.pushButtonExit.move(480, 35)
        # self.pushButtonExit.setIcon(QIcon(str(self.PATH / "img" / "exit.png")))
        self.pushButtonExit.setIcon(QIcon(QPixmap(':/img/exit.png')))
        self.pushButtonExit.setStyleSheet("background: rgba(225,225,225,100);border-style: outset;")
        # 清空按钮
        self.pushButtonClear = QPushButton(self)
        self.pushButtonClear.setToolTip("清空消息框")
        self.pushButtonClear.setFixedSize(QSize(50, 30))
        self.pushButtonClear.move(540, 35)
        # self.pushButtonClear.setIcon(QIcon(str(self.PATH / "img" / "clear.png")))
        self.pushButtonClear.setIcon(QIcon(QPixmap(':/img/clear.png')))
        self.pushButtonClear.setStyleSheet("background: rgba(225,225,225,100);border-style: outset;")
        # 账户输入窗口
        self.UserId = QLineEdit(self)
        self.UserId.setPlaceholderText("使用前请先输入账户ID")
        self.UserId.setFixedSize(QSize(170, 30))
        self.UserId.move(10, 35)
        self.UserId.setStyleSheet("background: rgba(225,225,225,100);font-family: Microsoft YaHei;font-size: 16px;")
        self.UserId.setEchoMode(QLineEdit.Password)
        # 用户名输入窗口
        self.UserName = QLineEdit(self)
        self.UserName.setPlaceholderText("昵称 默认为 用户")
        self.UserName.setFixedSize(QSize(160, 30))
        self.UserName.move(250, 35)
        self.UserName.setStyleSheet("background: rgba(225,225,225,100);font-family: Microsoft YaHei;font-size: 16px;")
        # 文字发送窗口 
        self.SendTxt = QLineEdit(self)
        self.SendTxt.setPlaceholderText("请输入文字")
        self.SendTxt.setFixedSize(QSize(520, 40))
        self.SendTxt.move(10, 580)
        self.SendTxt.setStyleSheet("background: rgba(225,225,225,100);font-family: Microsoft YaHei;font-size: 16px;")
        # 对话框
        self.textBrowser = QTextBrowser(self)
        self.textBrowser.setFixedSize(QSize(580, 495))
        self.textBrowser.move(10, 75)
        self.textBrowser.setStyleSheet("background: rgba(225,225,225,100);font-family: Microsoft YaHei;")
        self.textBrowser.setHtml(SendHtmlHello)
        # self.cursot = self.textBrowser.textCursor()
        # self.textBrowser.moveCursor(self.cursot.End)
        # QApplication.processEvents()
        # 绑定槽
        self.pushButtonEye.pressed.connect(self.EyePressed)
        self.pushButtonEye.released.connect(self.EyeReleased)
        self.pushButtonSing.clicked.connect(self.Sing)
        self.pushButtonExit.clicked.connect(self.Exit)
        self.pushButtonSend.clicked.connect(self.Send)
        self.pushButtonClear.clicked.connect(self.Clear)
        # 绑定信号
        self.WebsockReceiveSingal.connect(self.WindowTextReceiv)
        self.LogInfoSingal.connect(self.WindowTextLog)
        self.SendSingal.connect(self.WindowTextSend)
        self.ConnectionsSinagl.connect(self.ConnectionsClose)
        return
    
    def InitWindow(self):
        """初始化窗口"""
        self.setFixedSize(600, 630)
        self.setTitleBar(StandardTitleBar(self))
        self.titleBar.setDoubleClickEnabled(False)
        self.titleBar.maxBtn.deleteLater()  # 删除最大化按钮
        self.setResizeEnabled(False)  # 禁止手动拉伸
        
        self.setWindowIcon(QIcon(':/img/bot.png'))  # 图标
        self.setWindowTitle('Xiaonan') # 标题
        self.setStyleSheet("border-radius:8px;font-family: Microsoft YaHei;font-size: 16px;")
        palette = QPalette()
        # palette.setBrush(QPalette.Background, QBrush(QPixmap(str(self.PATH / "img" / "back.png"))))  
        palette.setBrush(QPalette.Background, QBrush(QPixmap(':/img/back.png')))
        self.setPalette(palette)
        # 窗口打开位置，默认在屏幕中间
        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)
    
    def Sing(self) -> None:
        """登录"""   
        user_id = self.UserId.text()
        if not user_id:
            self.LogInfoSingal.emit("请先填写账户ID")
            return
        if not isinstance(user_id, str):
            self.LogInfoSingal.emit("账户ID应为纯数字")
            return
        if user_id in self.connections:
            self.LogInfoSingal.emit(f"账户{user_id}已登录，请不要重复登录")
            return  
        self.LogInfoSingal.emit("正在登录请稍后")
        self.UserId.setReadOnly(True)
        try:  
            websocket = create_connection(self.WsUrl)
            self.connections[user_id] = websocket
            RecvThread = WebsockRecvThread(
            self.WebsockReceiveSingal,
            self.LogInfoSingal,
            self.ConnectionsSinagl,
            self.connections[user_id],
            user_id
            )  # 创建线程
            RecvThread.start()  # 开始线程
            self.thread[user_id] = RecvThread 
        except ConnectionRefusedError:
            self.LogInfoSingal.emit(f"服务器掉线了") 
        except Exception:
            self.LogInfoSingal.emit(f"服务出错了") 
        return

    def EyePressed(self) -> None:
        """按下眼睛"""
        self.UserId.setEchoMode(QLineEdit.Normal)
        return
    
    def EyeReleased(self) -> None:
        """松开眼睛"""    
        self.UserId.setEchoMode(QLineEdit.Password)
        return
   
    def Exit(self) -> None:
        """退出登录"""
        if not self.connections:
            self.LogInfoSingal.emit("还没有登录呢")
            return
        for ws in self.connections.values():
            ws.close()
        for thread in self.thread.values():
            thread.quit()
        self.connections.clear()
        self.thread.clear()
        self.UserId.setReadOnly(False) 
        return
    
    def Send(self) -> None:
        """发送信息"""
        user_id = self.UserId.text()
        if not user_id:
            self.LogInfoSingal.emit("请先填写账户ID")
            return
        if not user_id in self.connections:
            self.LogInfoSingal.emit("还没有登录呢")  
            return
        msg = self.SendTxt.text()
        if msg and isinstance(msg, str):
            self.SendThread = WebsockSendThread(msg, user_id, self.connections[user_id])  # 创建线程
            self.SendThread.start()  # 开始线程
            self.SendSingal.emit(msg)
            self.SendTxt.clear()
            return
        else:
            return
    
    def Clear(self) -> None:
        """清屏"""
        self.textBrowser.clear()
        return
    
    def GetName(self) -> str:
        """获取用户昵称"""
        name = str(self.UserName.text())
        if name:
            return self.UserName.text()
        else:
            return self.name

    def ConnectionsClose(self) -> None:
        """连接意外断开"""
        for ws in self.connections.values():
            ws.close()
        for thread in self.thread.values():
            thread.quit()
        self.connections.clear()
        self.thread.clear()
        self.UserId.setReadOnly(False) 
        return
    
    def WindowTextReceiv(self, msg) -> None:
        """服务器输出"""
        msg = msg.replace("\n", "<br>")
        self.textBrowser.append(SendHtmlLeft.format(self.BotName, msg))
        cursot = self.textBrowser.textCursor()
        self.textBrowser.moveCursor(cursot.End)
        QApplication.processEvents()
        return
    
    def WindowTextLog(self, msg) -> None:
        """日志类输出"""
        msg = msg.replace("\n", "<br>")
        self.textBrowser.append(SendHtmlErro.format(msg))
        cursot = self.textBrowser.textCursor()
        self.textBrowser.moveCursor(cursot.End)
        QApplication.processEvents()
        return
     
    def WindowTextSend(self, msg) -> None:
        """用户输出"""
        msg = msg.replace("\n", "<br>")
        self.textBrowser.append(SendHtmlRight.format(self.GetName(), msg))
        cursot = self.textBrowser.textCursor()
        self.textBrowser.moveCursor(cursot.End)
        QApplication.processEvents()
        return

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())