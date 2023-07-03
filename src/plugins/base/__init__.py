from nonebot.plugin import on
from xiaonan_adapter import MessEvent, Bot

base_baby = on(priority=99, block=True)

@base_baby.handle()
async def _(bot: Bot, event: MessEvent):
    msg = {"msg": "404 err"}
    await bot.send(event, msg)