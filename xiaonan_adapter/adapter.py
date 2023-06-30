import re
import ujson as json
import asyncio
import contextlib
from typing import Any, List, Dict, cast, Tuple

from nonebot.config import Env
from nonebot.typing import overrides
from nonebot.message import handle_event
from nonebot.adapters import Adapter as BaseAdapter
from nonebot.log import logger
from nonebot.exception import WebSocketClosed

from nonebot.internal.driver import (
    URL,
    Driver,
    Request,
    ForwardDriver,
    WebSocket,
    WebSocketServerSetup,
)

from .bot import Bot
from .event import MessEvent
from .utils import log

NICKNAME: List = Env().nickname
nicknames: Dict = {re.escape(n) for n in NICKNAME}
nickname_regex = "|".join(nicknames)

class Adapter(BaseAdapter):
    
    @classmethod
    @overrides(BaseAdapter)
    def get_name(cls) -> str:
        return "XiaonanAdapter"

    @overrides(BaseAdapter)
    def __init__(self, driver: Driver, **kwargs: Any) -> None:
        super().__init__(driver, **kwargs)
        self.bot = Bot(self, NICKNAME[0])
        self.connections: Dict[str, WebSocket] = {}
        self.tasks: List["asyncio.Task"] = []
        self._setup()
                
    def _setup(self) -> None:
        self.setup_websocket_server(
            WebSocketServerSetup(
                URL("/xiaonan"), f"{self.get_name()} WS", self._handle_ws
            )
        )
        if isinstance(self.driver, ForwardDriver):
            self.driver.on_startup(self._start)
            self.driver.on_shutdown(self._shutdown)
        else:
            log.error(f"{self.get_name()} 请添加 websockets和fastapi驱动以使用本 adapter")   

    async def _start(self) -> None:
        self.bot_connect(self.bot)
   
    async def _shutdown(self) -> None:
        self.bot_disconnect(self.bot)
        self.connections.clear()
        
    async def _handle_ws(self, websocket: WebSocket) -> None:
        response = self._check_response(websocket.request)
        if not response:
            content = cast(str, "协议不匹配,链接关闭。")
            await websocket.close(1008, content)
            return
        
        await websocket.accept()
        try:
            data = await websocket.receive()
            user_id = self._check_user(json.loads(data), websocket)
            if not user_id:
                content = cast(str, "用户校核不成功,链接关闭。")
                await websocket.close(1008, content)
                return
            
            while True:
                data = await websocket.receive()
                json_data = json.loads(data)
                if not "msg" in json_data:
                    continue       
                asyncio.create_task(self._handle_event(json_data, user_id))

        except WebSocketClosed as e:
            logger.error(f"WebSocketClosed eero {e}")
        except Exception as e:
            logger.error(f"Exception {e}")
        finally:
            with contextlib.suppress(Exception):
                await websocket.close()
            self.connections.pop(user_id)
            logger.success(f"用户{user_id}已登出。")
                
    async def _handle_event(self, message: dict, user_id: str) -> None:
        cmd, at= self._check_nickname(message)
        event_class = MessEvent(cmd=cmd, message=message, user_id=user_id, at=at)
        await handle_event(self.bot, event_class)
        return

    def _check_response(self, request: Request) -> bool:
        headers = request.headers.get("upgrade", None)
        if headers == "websocket":
            return True
        else:
            return False
        
    def _check_user(self, data: dict, websocket: WebSocket) -> str:
        if not data or not isinstance(data, dict):
            return
        user_id = data.get("user_id", None) 
        hello_msg = data.get("msg", None)
        if hello_msg != "i miss you xiaonan" or not user_id:
            return
        if user_id in self.connections:
            return user_id
        else:
            self.connections[user_id] = websocket
            logger.success(f"用户{user_id}成功登录。")
            return user_id
    
    def _check_nickname(self, message: dict) -> Tuple[List[str],bool]:
        msg = message.get("msg", "")
        if m := re.search(rf"^({nickname_regex})([\s,，]*|$)", msg, re.IGNORECASE):
            return msg[m.end() :].split(), True
        else:
            return msg.split(), False
            
    
    @overrides(BaseAdapter)
    async def _call_api(self, bot: Bot, api: MessEvent, **data: Any) -> None:
        pass
    
    async def send(self, user_id, message: dict) -> None:
        await self.connections[user_id].send(json.dumps(message))
        return 

    
    