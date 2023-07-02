#一般语法[start:end:step]

# - start 是起始索引。默认是第一个元素
# - end 是结束索引,（不包括该位置的元素）。默认是最后一个元素的下一位
# - step 是步长,默认是1

# 在 Python 中切片操作不仅限于字符串。它同样适用于:
# - 列表
# - 元组
# - range 对象
# - 任何可迭代对象

#纯数字无法切片

fruits = ['apple', 'banana', 'cherry', 'durian']
# - fruits[-1] 是 'durian',表示倒数第一个元素
# - fruits[-2] 是 'cherry',表示倒数第二个元素
# - 以此类推
# 所以,如果切片中的 start 和 end 索引是负数,表示如下含义:
# - start:从序列末尾开始算起的起始位置
# - end:从序列末尾开始算起的结束位置

fruits[-3:-1]  #['banana', 'cherry']
