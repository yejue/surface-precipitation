"""
格式化打印工具包
"""


def star_decoration(content, filler="#", length=30, points=5):
    """
    格式化打印回调函数之星星打印
     - 使用 filler 来指定格式化打印填充符号
     - 使用 length 来指定星星每条边的长度，单位为字节
     - 使用 points 来指定星星角数，默认为五角星
    """
    pass


def matrix_decoration(content, filler="#", length=100, high=2):
    """
    格式化打印回调函数之矩阵打印
     - 使用 filler 来指定格式化打印填充符号
     - 使用 length 来指定横向总长度,单位为字节
     - 使用 high 来指定以打印内容为中心的上下对称行数
    """
    surrounding = (filler * length) + "\n" + ((filler+(length-2)*" "+filler+"\n")*high)
    core = content.center(length-2, " ")
    return f"{surrounding}{filler}{core}{filler}{surrounding[::-1]}"


def s_print(content, callback=matrix_decoration, filler="#"):
    """
    格式化打印工具
     - 将 content 的内容使用一定的装饰符号打印
     - 使用 callback 来指定 content 的装饰工作
    """
    temp = callback(content, filler)
    print(temp)
    return temp
