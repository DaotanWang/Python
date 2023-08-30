import os
from pathlib import Path

folder_path = 'D:\\file'

# 删除所有子文件夹下的 image001.jpg
for root, dirs, files in os.walk(folder_path):
    if 'image001.jpg' in files:
        os.remove(os.path.join(root, 'image001.jpg'))

# 重命名子文件夹下的pdf文件
for root, dirs, files in os.walk(folder_path):
    pdfs = [f for f in files if f.endswith('.pdf')]
    if len(pdfs) > 0:
        subfolder = Path(root).name
        for i, pdf in enumerate(pdfs):
            new_name = subfolder
            if i > 0:
                new_name += f'({i+1})'
            new_name += '.pdf'
            os.rename(os.path.join(root, pdf), os.path.join(root, new_name))
