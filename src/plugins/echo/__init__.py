from nonebot.plugin import on
from xiaonan_adapter import MessEvent, Bot

echo = on("echo", priority=10, block=True)

@echo.handle()
async def _(bot: Bot ,event: MessEvent):
    arg = event.get_arg()
    args = "".join(arg)
    msg = {"msg": args}
    await bot.send(event, msg)
    