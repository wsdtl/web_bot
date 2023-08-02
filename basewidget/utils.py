from PySide6.QtGui import (
    QPixmap,
    QColor
)

def change_theme_color(icon: QPixmap, color: QColor) -> QPixmap:
    """更改纯色 QPixmap 颜色 遮罩方法"""
    pix = QPixmap(icon.width(), icon.height())  # 创建目标大小 QPixmap
    pix.fill(color)                             # 修改目标 QPixmap 颜色
    mask = icon.mask()                          # 获取图标 遮罩 范围
    pix.setMask(mask)                           # 为 目标 QPixmap 颜色添加遮罩蒙版 并作为新的颜色图标返回
    
    return pix   