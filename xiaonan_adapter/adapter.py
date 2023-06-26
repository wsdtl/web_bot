import ujson as json
import asyncio
import socket
from typing import Any, List

from nonebot.config import Env
from nonebot.drivers import Driver, ForwardDriver
from nonebot.typing import overrides
from nonebot.message import handle_event
from nonebot.adapters import Adapter as BaseAdapter
from nonebot.drivers import Driver, ForwardDriver
from nonebot.log import logger

from .bot import Bot
from .event import MessEvent
from .utils import  log

NICKNAME: List = Env().nickname
HOST: str = Env().sock_host
PORT: int = Env().sock_port
LISTEN: int = Env().listen

class Adapter(BaseAdapter):
    
    @overrides(BaseAdapter)
    def __init__(self, driver: Driver, **kwargs: Any) -> None:
        super().__init__(driver, **kwargs)
        self.bot = Bot(self, NICKNAME[0])
        self.tasks = set()
        self.setup()

    @staticmethod
    @overrides(BaseAdapter)
    def get_name() -> str:
        return "XiaoNan_Adapter"

    def setup(self):
        if isinstance(self.driver, ForwardDriver):
            self.driver.on_startup(self._start)
            self.driver.on_shutdown(self._shutdown)
        else:
            log.error(f"{self.get_name()} 请添加 websockets和fastapi驱动以使用本 adapter")
  
    async def main_server(self):
        host, port = (str(HOST), PORT)
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.bind((host, port))
        self.bot_connect(self.bot)
        logger.success(f"机器人{self.bot}已经链接-监测端口 {host}:{str(port)}!")
        s.listen(LISTEN)
        while True:
            try:
                sock, addr = s.accept()
                data = sock.recv(1024)
                json_data = json.loads(data)

                message = {"msg" : json_data["msg"],
                           "sock": sock,
                           "addr" : addr
                           }
                
                await self.hand_to(message= message, sock= sock, addr= addr)
                
            except Exception as e:
                logger.error(f"main_servere 发生错误{e}!")
                self.bot_disconnect(self.bot)
                sock.close()
                
    async def send(self, sock, addr: List[str], message: dict):
        json_data = json.dumps(message)
        sock.send(bytes(json_data.encode('utf-8')))
        
    async def _start(self) -> None:
        task_main_server = asyncio.create_task(self.main_server())
        self.tasks.add(task_main_server)

    async def _shutdown(self) -> None:
        self.bot_disconnect(self.bot)
         
    async def hand_to(self, message: dict, sock, addr: list[str]):
        event_class = MessEvent(message= message, sock= sock, addr= addr)
        await asyncio.create_task(handle_event(
            self.bot,
            event_class
        ))

    @overrides(BaseAdapter)
    async def _call_api(self, bot: Bot, api: MessEvent, **data: Any) -> None:
        pass

    
    

        

  