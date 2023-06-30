import asyncio
from typing import Any
from typing import TYPE_CHECKING
from nonebot.adapters import Bot as BaseBot
from nonebot.typing import overrides

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
            user_id: str,
            message: dict,
    ) -> Any:
        await asyncio.create_task(self.adapter.send(user_id, message))
        return
    