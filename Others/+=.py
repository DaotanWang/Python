# 数字

a = 1
a += 2
print(a) # 3

# 字符串
a = "Hello "
a += "World"
print(a) # Hello World

#列表与集合
a = [1,2,3]
a += [4,5]
print(a) # [1, 2, 3, 4, 5]

a = {1,2,3}
a += {4,5} 
print(a) # {1, 2, 3, 4, 5}

# - 对于数字,+= 实现累加
# - 对于字符串,+= 实现字符串连接操作
# - 对于列表和集合,+= 实现序列的连接
# += 的功能是:将右边的值加到左边变量上。