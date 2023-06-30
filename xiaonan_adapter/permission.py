from nonebot.permission import Permission
from .event import MessEvent

async def _to_me(event: MessEvent) -> bool:
    return event.is_tome()

TOME: Permission = Permission(_to_me)
"""匹配消息是否at 机器人"""


__all__ = [
    "TOME"
]
