from PyPDF2 import PdfReader, PdfWriter
import fitz
import shutil
import tesserocr
from PIL import Image
import re
import os
import glob

print("请输入你的pdf文件路径：")
path = input()
input_folder = r"{}".format(path)

for pdf_file in os.listdir(input_folder):
    if pdf_file.endswith(".pdf"):

        pdf_path = os.path.join(input_folder, pdf_file)
        pdf_reader = PdfReader(pdf_path)

        for page_num in range(len(pdf_reader.pages)):
            pdf_writer = PdfWriter()
            pdf_writer.add_page(pdf_reader.pages[page_num])

            output_file = f"{pdf_file.rsplit('.')[0]}_page{page_num + 1}.pdf"
            output_path = os.path.join(input_folder, output_file)

            with open(output_path, 'wb') as output_pdf:
                pdf_writer.write(output_pdf)

            print(f"Created: {output_file}")
def pdf2img(ii,pdf_path, img_dir):
    doc = fitz.open(pdf_path)  # 打开pdf
    for page in doc:  # 遍历pdf的每一页

        zoom_x = 2.0  # 设置每页的水平缩放因子
        zoom_y = 2.0  # 设置每页的垂直缩放因子
        mat = fitz.Matrix(zoom_x, zoom_y)
        pix = page.get_pixmap(matrix=mat)
        pix.save(r"{}/page-{}-{}.jpg".format(img_dir, ii, page.number)) # 保存
file_names = []

# 使用glob模块遍历文件夹
for file_name in glob.glob(os.path.join(input_folder, '*.pdf')):
    # 判断文件名中是否包含".pdf"和"_"
    if '_' in file_name and file_name.endswith('.pdf'):
        # 如果文件名中包含"_"，并且以.pdf结尾，则添加到输出列表中
        file_names.append(os.path.basename(file_name))

    # 输出文件名列表
print(file_names)

for ii in file_names:
    pdf_path = os.path.join(input_folder, ii)
    # 图片保存位置
    img_dir = input_folder

    # pdf转图片
    pdf2img(ii,pdf_path, img_dir)

new_folder_name = "result"

# 组合新文件夹的完整路径
new_folder = os.path.join(input_folder, new_folder_name)

# 创建新文件夹
os.makedirs(new_folder, exist_ok=True)

file_names = []

# 使用glob模块遍历文件夹
for file_name in glob.glob(os.path.join(input_folder, '*.jpg')):
    # 判断文件名中是否包含".pdf"和"_"
    if '_' in file_name and file_name.endswith('.jpg'):
        # 如果文件名中包含"_"，并且以.pdf结尾，则添加到输出列表中
        file_names.append(os.path.basename(file_name))

    # 输出文件名列表
print(file_names)

p = '\d{3}-\d{8}'

for iii in file_names:
    path_jpg = os.path.join(input_folder, iii)
    image = Image.open(path_jpg)
    res = tesserocr.image_to_text(image)
    match = re.findall(p,res)
    if match:
        print(match)
        for cc in match:
            dst_img_path = os.path.join(new_folder, cc+".jpg")
            shutil.copy(path_jpg, dst_img_path)
    else:
        dst_img_path = os.path.join(new_folder, iii + "_no_match.jpg")
        shutil.copy(path_jpg, dst_img_path)

folder_path = os.path.join(input_folder,"result")

# 获取文件夹中的所有文件名
file_names = os.listdir(folder_path)

# 用于保存JPG文件的文件名
jpg_file_names = []

# 遍历所有文件名，查找JPG文件
for file_name in file_names:
    if file_name.endswith('.jpg'):
        jpg_file_names.append(file_name)

print(jpg_file_names)
    # 转换JPG文件为PDF文件
for jpg_file_name in jpg_file_names:
    # 打开JPG文件
    img = Image.open(os.path.join(folder_path, jpg_file_name))
    name = str(jpg_file_name[:12])
    name = "POD_"+name
    print(name)
    # 将JPG文件保存为PDF文件
    pdf_path = os.path.join(folder_path, name + '.pdf')
    img.save(pdf_path)

jpg_files = glob.glob(os.path.join(folder_path, '*.jpg'))

# 遍历所有JPG文件并删除
for file_path in jpg_files:
    os.remove(file_path)

file_pattern = os.path.join(input_folder, '*[_-]**')
matching_files = glob.glob(file_pattern)

for file_path in matching_files:
    os.remove(file_path)

