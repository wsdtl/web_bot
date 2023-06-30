import nonebot
from xiaonan_adapter import Adapter as XiaonanAdapter

# 初始化 NoneBot
nonebot.init()
app = nonebot.get_asgi()

# 注册适配器
driver = nonebot.get_driver()
driver.register_adapter(XiaonanAdapter)

# 在这里加载插件
# nonebot.load_builtin_plugins("echo")  # 内置插件
# nonebot.load_plugin("thirdparty_plugin")  # 第三方插件
nonebot.load_plugins("src/plugins") # 本地插件

# config = driver.config
# nonebot.load_all_plugins(set(config.plugins), set(config.plugin_dirs))

if __name__ == "__main__":
    nonebot.run(app="__mp_main__:app")

