import asyncio
from typing import Any, Union, Optional, TYPE_CHECKING
from nonebot.adapters import Bot as BaseBot
from nonebot.typing import overrides
from nonebot.exception import FinishedException

from .event import MessEvent

if TYPE_CHECKING:
    from .adapter import Adapter


class Bot(BaseBot):
    adapter: "Adapter"

    def __init__(
        self, adapter: "Adapter", self_id: str
    ) -> None:
        super().__init__(adapter, self_id)

    @overrides(BaseBot)
    async def send(
            self,
            event: MessEvent,
            message: Optional[Union[str, dict]] = None,
    ) -> Any:
        if isinstance(message, str):
            message = {
                "msg" : message
            }
        await asyncio.create_task(self.adapter.send(event.user_id, message))
        return
    
    async def finish(self) -> None:
        raise FinishedException
    