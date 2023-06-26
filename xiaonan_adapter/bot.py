import asyncio
from typing import Any
from typing import TYPE_CHECKING
from nonebot.adapters import Bot as BaseBot
from nonebot.typing import overrides
from nonebot.exception import FinishedException

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
            sock: str,
            addr: list[str],
            message: dict,
    ) -> Any:
        asyncio.create_task(self.adapter.send(sock= sock, addr= addr, message= message))
        return
    
    async def finish(
            self,
            sock: str,
            addr: list[str],
            message: dict,
    ) -> Any:
        asyncio.create_task(self.adapter.send(sock= sock, addr= addr, message= message))
        raise FinishedException