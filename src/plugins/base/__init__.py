from nonebot.plugin import on, on_regex
from xiaonan_adapter import MessEvent, Bot

base_baby = on_regex(r"\d+", priority=97, block=True)

@base_baby.handle()
async def _(bot: Bot, event: MessEvent):
    msg = {"msg": "404 err"}
    await bot.send(event, msg)