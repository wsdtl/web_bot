from nonebot.plugin import on
from xiaonan_adapter import MessEvent, Bot, TOME

atme = on(permission=TOME, priority=10, block=True)

@atme.handle()
async def _(bot: Bot ,event: MessEvent):
    arg = event.get_arg()
    msg = {"msg": arg}
    await bot.finish(event.sock, event.addr, msg)
    
at_me = on("at_me", priority=11, block=True)

@at_me.handle()
async def _(bot: Bot ,event: MessEvent):
    arg = event.get_arg()
    msg = {"msg": arg}
    await bot.finish(event.sock, event.addr, msg)    