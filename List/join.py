#它的主要作用是:将序列中的元素以指定的字符连接成一个新的字符串。

"".join(sequence)
# 这里 "" 表示连接时不使用任何分隔符

sequence = ['a','b', 'c']
result = ", ".join(sequence)

print(result)
# a, b, c

