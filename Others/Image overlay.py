def Picture_Synthesis(mother_img,son_img,save_img,coordinate=None):
    """
    :param mother_img: 母图
    :param son_img: 子图
    :param save_img: 保存图片名
    :param coordinate: 子图在母图的坐标
    :return:
    """
    #将图片赋值,方便后面的代码调用
    M_Img = Image.open(mother_img)
    S_Img = Image.open(son_img)
    factor = 4#子图缩小的倍数1代表不变，2就代表原来的一半

    #给图片指定色彩显示格式
    M_Img = M_Img.convert("RGBA")  # CMYK/RGBA 转换颜色格式（CMYK用于打印机的色彩，RGBA用于显示器的色彩）

    # 获取图片的尺寸
    M_Img_w, M_Img_h = M_Img.size  # 获取被放图片的大小（母图）
    # print("母图尺寸：",M_Img.size)
    S_Img_w, S_Img_h = S_Img.size  # 获取小图的大小（子图）
    # print("子图尺寸：",S_Img.size)

    size_w = int(S_Img_w / factor)
    size_h = int(S_Img_h / factor)

    # 防止子图尺寸大于母图
    if S_Img_w > size_w:
        S_Img_w = size_w
    if S_Img_h > size_h:
        S_Img_h = size_h

    # # 重新设置子图的尺寸
    # icon = S_Img.resize((S_Img_w, S_Img_h), Image.ANTIALIAS)
    icon = S_Img.resize((S_Img_w, S_Img_h), Image.ANTIALIAS)
    w = int((M_Img_w - S_Img_w) / 2)
    h = int((M_Img_h - S_Img_h) / 2)

    try:
        if coordinate==None or coordinate=="":
            coordinate=(w, h)
            # 粘贴子图到母图的指定坐标（当前居中）
            M_Img.paste(icon, coordinate, mask=None)
        else:
            # print("已经指定坐标")
            # 粘贴子图到母图的指定坐标（当前居中）
            M_Img.paste(icon, coordinate, mask=None)
    except:
        print("坐标指定出错 ")
    # 保存图片
    M_Img.save(save_img)
