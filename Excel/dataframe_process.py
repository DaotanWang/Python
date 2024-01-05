

# 插入列

data.insert(len(data.columns), "导入时间", "")

data.insert(len(data.columns), "罚单处理情况", "")

# 填值

data["导入时间"] = date.today()


# 保存表格

data.to_excel(file_paths[i], index=False)
