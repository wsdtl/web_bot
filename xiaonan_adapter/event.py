from nonebot.adapters import Event as BaseEvent
from nonebot.typing import overrides
from typing import List

# 消息事件
class MessEvent(BaseEvent):
    cmd : list
    message: dict
    user_id: str
    at: bool 
        
    def is_tome(self) -> bool:
        return self.at
    
    def get_event_name(self) -> str:
        return 1

    def get_arg(self) -> List[str]:
        try:
            arg = self.cmd[1:]
        except Exception as e:
            arg = []
        return arg

    def get_type(self) -> str:
        try:
            arg = self.cmd[0]
        except Exception as e:
            arg = ""
            return arg
        return arg
        
    def get_message(self) -> dict:
        return self.message

    @overrides(BaseEvent)
    def get_user_id(self) -> str:
        return self.user_id
    
    @overrides(BaseEvent)
    def get_session_id(self) -> str:
        return "获取会话 id 的方法。"
    
    @overrides(BaseEvent)
    def get_event_description(self) -> str:
        return f"收到消息:{self.message}"

