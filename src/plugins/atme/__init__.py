from nonebot.plugin import on
from xiaonan_adapter import MessEvent, Bot, TOME

atme = on(permission=TOME, priority=10, block=True)

@atme.handle()
async def _(bot: Bot ,event: MessEvent):
    arg = event.get_arg()
    args = "".join(arg)
    msg = {"msg": args+"叫我干什么!"}
    await bot.send(event, msg)
      