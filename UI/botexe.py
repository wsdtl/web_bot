import os
import sys
import ujson as json
from websocket import create_connection
from pathlib import Path
from typing import Dict

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QTextBrowser, QLineEdit
from PyQt5.QtGui import QIcon, QPalette, QBrush, QPixmap
from PyQt5.QtCore import QThread, pyqtSignal, QSize, Qt

SendHtmlLeft = """           
<html>
    <body>
        <hr style="margin-bottom: 1px;margin-top: 1px;">
        <p style="text-align: left;margin: 1px;padding: 1px;color: #ffcde6;font-size: 18px;font-weight:bold;">{0}</p>
        <p style="text-align: left;margin: 1px;padding: 1px;font-size: 16px;">{1}</p>
    </body>
</html>          
"""
SendHtmlRight = """
<html>
    <body>
        <hr style="margin-bottom: 1px;margin-top: 1px;">
        <p style="text-align: right;margin: 1px;padding: 1px;color: #ffcde6;font-size: 18px;font-weight:bold;">{0}</p>
        <p style="text-align: right;margin: 1px;padding: 1px;font-size: 16px;">{1}</p>
    </body>
</html>             
"""
SendHtmlErro = """
<html>
    <body>
        <hr style="margin-bottom: 1px;margin-top: 1px;">
        <h1 style="text-align: center;margin: 1px;padding: 1px;color: #00ffff;">{0}</h1>
    </body>
</html>         
"""       
SendHtmlHello = """
<html>
    <body>
        <h1 style="text-align: center;margin: 1px;padding: 1px;color: #00ffff;">欢迎使用晓楠客户端</h1>
    </body>
</html>         
"""


class WebsockRecvThread(QThread):
    
    def __init__(self, WebsockReceiveSingal: pyqtSignal, 
                 LogInfoSingal: pyqtSignal, 
                 ConnectionsSinagl: pyqtSignal,
                 websock: any,
                 UserId: str
        ):
        super().__init__()
        self.WebsockReceiveSingal: pyqtSignal = WebsockReceiveSingal
        self.LogInfoSingal: pyqtSignal = LogInfoSingal
        self.ConnectionsSinagl: pyqtSignal = ConnectionsSinagl
        self.websock: any = websock
        self.UserId: str = UserId
        
    def run(self):
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
                self.LogInfoSingal.emit(f"与服务器已失去连接，请重新登录，{e}")
            finally:
                self.ConnectionsSinagl.emit(self.UserId)
            return    
        
    def to_json(self, data: dict) -> str:
        return json.dumps(data)

class WebsockSendThread(QThread):
    
    def __init__(self,
                 msg: str,
                 UserId: str,
                 websock: any
        ):
        super().__init__()
        self.msg: str = msg
        self.UserId: str = UserId
        self.websock: any = websock
        
    def run(self):
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

class Window(QWidget):
  
    PATH = Path() / os.path.dirname(os.path.abspath(__file__))
    # 声明一个信号 只能放在函数的外面
    WebsockReceiveSingal = pyqtSignal(str)
    LogInfoSingal = pyqtSignal(str)
    SendSingal = pyqtSignal(str)
    ConnectionsSinagl = pyqtSignal(str)
    
    def __init__(self) -> None:
        super().__init__()
        self.connections :Dict[str: QThread] = {}
        self.thread: Dict[str:QThread] = {}
        self.name: str = "用户"
        self.BotName: str = "晓楠"
        self.WsUrl: str = "ws://dengxiaonan.cn:8090/xiaonan"
        self.init_ui()

    
    def init_ui(self):
        self.setFixedSize(600, 600)
        self.setWindowTitle("晓楠客户端")
        self.setWindowIcon(QIcon(str(self.PATH / "img" / "bot.png")))
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(QPixmap(str(self.PATH / "img" / "back.png"))))  
        self.setPalette(palette)
        # 发送按钮
        self.pushButtonSend = QPushButton(self)
        self.pushButtonSend.setToolTip("发送")
        self.pushButtonSend.setMinimumSize(QSize(50, 40))
        self.pushButtonSend.move(540, 550)
        self.pushButtonSend.setIcon(QIcon(str(self.PATH / "img" / "send.png")))
        self.pushButtonSend.setStyleSheet("background:rgba(225,225,225,100);")
        self.pushButtonSend.setShortcut (Qt.Key_Return )
        # 隐藏按钮
        self.pushButtonEye = QPushButton(self)
        self.pushButtonEye.setToolTip("隐藏账号")
        self.pushButtonEye.setMinimumSize(QSize(50, 30))
        self.pushButtonEye.move(190, 10)
        self.pushButtonEye.setIcon(QIcon(str(self.PATH / "img" / "eye.png")))
        self.pushButtonEye.setStyleSheet("background:rgba(225,225,225,100);")
        # 登录按钮
        self.pushButtonSing = QPushButton(self)
        self.pushButtonSing.setToolTip("登录")
        self.pushButtonSing.setMinimumSize(QSize(50, 30))
        self.pushButtonSing.move(420, 10)
        self.pushButtonSing.setIcon(QIcon(str(self.PATH / "img" / "sing.png")))
        self.pushButtonSing.setStyleSheet("background:rgba(225,225,225,100);")
        # 登出按钮
        self.pushButtonExit = QPushButton(self)
        self.pushButtonExit.setToolTip("登出")
        self.pushButtonExit.setMinimumSize(QSize(50, 30))
        self.pushButtonExit.move(480, 10)
        self.pushButtonExit.setIcon(QIcon(str(self.PATH / "img" / "exit.png")))
        self.pushButtonExit.setStyleSheet("background:rgba(225,225,225,100);")
        # 清空按钮
        self.pushButtonClear = QPushButton(self)
        self.pushButtonClear.setToolTip("清空消息框")
        self.pushButtonClear.setMinimumSize(QSize(50, 30))
        self.pushButtonClear.move(540, 10)
        self.pushButtonClear.setIcon(QIcon(str(self.PATH / "img" / "clear.png")))
        self.pushButtonClear.setStyleSheet("background:rgba(225,225,225,100);")
        # 账户输入窗口
        self.UserId = QLineEdit(self)
        self.UserId.setPlaceholderText("使用前请先输入账户ID")
        self.UserId.setMinimumSize(QSize(170, 30))
        self.UserId.move(10, 10)
        self.UserId.setStyleSheet("background:rgba(225,225,225,100);border-style:outset;font-family:Microsoft YaHei;font-size:16px;")
        self.UserId.setEchoMode(QLineEdit.Password)
        # 用户名输入窗口
        self.UserName = QLineEdit(self)
        self.UserName.setPlaceholderText("昵称，默认为 用户")
        self.UserName.setMinimumSize(QSize(160, 30))
        self.UserName.move(250, 10)
        self.UserName.setStyleSheet("background:rgba(225,225,225,100);border-style:outset;font-family:Microsoft YaHei;font-size:16px;")
        # 文字发送窗口
        self.SendTxt = QLineEdit(self)
        self.SendTxt.setPlaceholderText("请输入文字")
        self.SendTxt.setMinimumSize(QSize(520, 40))
        self.SendTxt.move(10, 550)
        self.SendTxt.setStyleSheet("background:rgba(225,225,225,100);border-style:outset;font-family:Microsoft YaHei;font-size:16px;")
        # 对话框
        self.textBrowser = QTextBrowser(self)
        self.textBrowser.setMinimumSize(QSize(580, 490))
        self.textBrowser.move(10, 50)
        self.textBrowser.setStyleSheet("background:rgba(225,225,225,100);font-family:Microsoft YaHei;")
        self.textBrowser.append(SendHtmlHello)
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
                
    def Sing(self) -> None:
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
        self.UserId.setReadOnly(True)  
        websocket = create_connection(self.WsUrl)
        self.connections[user_id] = websocket
        thread = self.RecvThread = WebsockRecvThread(
            self.WebsockReceiveSingal,
            self.LogInfoSingal,
            self.ConnectionsSinagl,
            self.connections[user_id],
            user_id
        )  # 创建线程
        self.RecvThread.start()  # 开始线程
        self.thread[user_id] = thread
        return
    # 按下眼睛
    def EyePressed(self) -> None:
        self.UserId.setEchoMode(QLineEdit.Normal)
        return
    # 松开眼睛
    def EyeReleased(self) -> None:
        self.UserId.setEchoMode(QLineEdit.Password)
        return
    # 退出登录
    def Exit(self) -> None:
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
    # 发送信息
    def Send(self) -> None:
        user_id = self.UserId.text()
        if not user_id:
            self.LogInfoSingal.emit("请先填写账户ID")
        msg = self.SendTxt.text()
        if msg and isinstance(msg, str) and user_id in self.connections:
            self.SendThread = WebsockSendThread(msg, user_id, self.connections[user_id])  # 创建线程
            self.SendThread.start()  # 开始线程
            self.SendSingal.emit(msg)
            self.SendTxt.clear()
            return
        else:
            return
    # 清屏
    def Clear(self) -> None:
        self.textBrowser.clear()
        return
    # 获取用户昵称
    def GetName(self) -> str:
        name = str(self.UserName.text())
        if name:
            return self.UserName.text()
        else:
            return self.name
    # 连接意外断开
    def ConnectionsClose(self) -> None:
        for ws in self.connections.values():
            ws.close()
        for thread in self.thread.values():
            thread.quit()
        self.connections.clear()
        self.thread.clear()
        self.UserId.setReadOnly(False) 
        return
    # 服务器输出
    def WindowTextReceiv(self, msg) -> None:
        msg = msg.replace("\n", "<br>")
        self.textBrowser.append(SendHtmlLeft.format(self.BotName, msg))
        return
    # 日志类输出
    def WindowTextLog(self, msg) -> None:
        msg = msg.replace("\n", "<br>")
        self.textBrowser.append(SendHtmlErro.format(msg))
        return
     # 用户输出
    def WindowTextSend(self, msg) -> None:
        msg = msg.replace("\n", "<br>")
        self.textBrowser.append(SendHtmlRight.format(self.GetName(), msg))
        return

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())