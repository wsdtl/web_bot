from nonebot.plugin import on
from xiaonan_adapter import MessEvent, Bot, TOME

echo = on("echo", priority=10, block=True)

@echo.handle()
async def _(bot: Bot ,event: MessEvent):
    arg = event.get_arg()
    msg = {"msg": arg}
    await bot.finish(event.sock, event.addr, msg)
    