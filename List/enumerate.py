# enumerate 是一个 Python 的内置函数,用于遍历序列中的元素同时获取其索引。
# enumerate 接受一个可迭代对象作为参数,返回一个迭代器,每次迭代都返回一个元组,元组的第 0 个元素是索引,第 1 个元素是值。

fruits = ['apple', 'banana', 'cherry']
for idx, fruit in enumerate(fruits):
    print(idx, fruit)

# 输出:
# 0 apple
# 1 banana
# 2 cherry
