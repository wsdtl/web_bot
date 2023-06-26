from nonebot.adapters import Event as BaseEvent
from nonebot.typing import overrides
from nonebot.config import Env
from nonebot.log import logger
from typing import List

NICKNAME: List = Env().nickname

# 消息事件
class MessEvent(BaseEvent):
    
    sock = str
    addr: list[str]
    message: dict
        
    def is_tome(self) -> bool:
        cmd = self.message["msg"].split()
        if cmd[0] in NICKNAME:
            return True
        else:
            return False
    
    def get_event_name(self) -> str:
        return ":".join(self.addr)

    def get_arg(self) -> str:
        cmd = self.message["msg"].split()
        if self.is_tome():
            try:
                arg = cmd[2:]
            except Exception as e:
                logger.error(f"event get_arg 错误{e}")
                arg = ""
            return arg
        else:
            return cmd[1:]

    def get_type(self):
        cmd = self.message["msg"].split()
        if self.is_tome():
            try:
                _type = cmd[2:]
            except Exception as e:
                logger.error(f"event get_type 错误{e}")
                _type = "at_me"
            return _type
        else:
            return cmd[0]
        
    def get_message(self):
        return self.message

    @overrides(BaseEvent)
    def get_user_id(self) -> str:
        if "user_id" in self.message:
            return self.message["user_id"]
        else:
            return None
    
    @overrides(BaseEvent)
    def get_session_id(self) -> str:
        return "获取会话 id 的方法。"
    
    @overrides(BaseEvent)
    def get_event_description(self) -> str:
        msg = f"收到消息:{self.message}"
        return msg

