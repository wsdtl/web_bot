import re
from nonebot.plugin import on
from xiaonan_adapter import MessEvent, Bot

questionmark = on(priority=98, block=True)

@questionmark.handle()
async def _(bot: Bot, event: MessEvent):
    msg = event.get_type()
    if re.search(r"^([?？¿!！¡\s]+)$", msg):
        mark = msg[0].replace("¿", "d").replace("?", "¿").replace("？", "¿").replace("d", "?")\
                     .replace("¡", "d").replace("!", "¡").replace("！", "¡").replace("d", "!")
        await bot.send(event, mark)
        await bot.finish()
    
    if re.search(r"^([6\s]+)$", msg):
        mark = msg.replace("6","9")
        await bot.send(event, mark)
    elif re.search(r"^([9\s]+)$", msg):
        mark = msg.replace("9", "6")
        await bot.send(event, mark)
    else:
        await bot.finish()
            