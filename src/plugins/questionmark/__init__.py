from nonebot.plugin import on
from xiaonan_adapter import MessEvent, Bot

questionmark = on(priority=98, block=True)

@questionmark.handle()
async def _(bot: Bot, event: MessEvent):
    markStar = event.get_type()
    mark = markStar
    mark = mark.replace("¿", "d")
    mark = mark.replace("?", "¿")
    mark = mark.replace("？", "¿")
    mark = mark.replace("d", "?")
    mark = mark.replace("¡", "d")
    mark = mark.replace("!", "¡")
    mark = mark.replace("！", "¡")
    mark = mark.replace("d", "!")
    mark = mark.replace("6", "d")
    mark = mark.replace("9", "6")
    mark = mark.replace("d", "9")
    if mark != markStar:
        await bot.send(event, mark)
    await bot.finish()

            