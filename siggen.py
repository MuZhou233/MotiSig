from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageColor
from io import BytesIO
import time

def siggen(data):
    im_h = 512; im_b = 60; font_size = 48; line_h = 12
    im = Image.new('RGBA', (im_h*2, im_h), '#fff')
    draw = ImageDraw.Draw(im)
    attr_color = '#000'

    #background
    imbg = Image.new('RGBA', im.size, '#fff')
    imbgc = Image.new('RGBA', im.size, '#fff')
    bg_h = im_h - (im_b + font_size*3 + line_h*4)

    try:
        data['bg']
    except KeyError:
        pass
    else:
        imbg = Image.open(data['bg'])
        imbg = imbg.convert('RGBA')
        w, h = imbg.size
        if(w >= h*2):
            imbg = imbg.crop((0, 0, h*2, h))
        else:
            imbg = imbg.crop((0, 0, w, int(w/2)))
        imbg = imbg.resize(im.size)

    try:
        data['bg_color']
    except KeyError:
        pass
    else:
        imbgc = Image.new('RGBA', im.size, ImageColor.getrgb(data['bg_color']))

    try:
        data['bg']
        data['bg_color']
    except KeyError:
        try:
            data['bg']
        except KeyError:
            imbg = imbgc
    else:
        try:
            data['bg_blend']
        except KeyError:
            blend_a = 0.5
        else:
            blend_a = data['bg_blend']
        imbg = Image.blend(imbgc, imbg, alpha=blend_a)
    
    r,g,b,a = imbg.resize((1,1), Image.ANTIALIAS).getcolors()[0][1]
    if r*0.299 + g*0.578 + b*0.114 < 192:
        attr_color = '#fff'

    im.paste(imbg)
    imbg = Image.new('RGBA', (im_h*2, bg_h), 'white')
    imbg = circle_corner(imbg, radii = 36, corner = (1,1,0,0))
    im.paste(imbg, (0, im_h-bg_h, im_h*2, im_h), imbg)

    #copyright
    font = ImageFont.truetype("fzht.ttf", size=12)
    draw.text((0,im_h - 13), 'Powered By MotiSig · '+ time.strftime('%Y-%m-%d %H:%M',time.localtime(time.time())), '#888', font=font)

    font = ImageFont.truetype("fzht.ttf", size=font_size)
    f = BytesIO()

    #name
    draw.text((im_b, im_h - im_b - font_size), data['name'], '#000', font=font)
    
    #avatar
    imavatar_h = 0
    try:
        data['avatar']
    except KeyError:
        pass
    else:
        imavatar_h = int(im_h/2)
        imavatar = Image.open(BytesIO(data['avatar']))

        imavatar = imavatar.resize((imavatar_h, imavatar_h), Image.ANTIALIAS)
        imavatar = circle_corner(imavatar, radii = 24)
        #imavatar = circle_border(imavatar, radii=24, width=5)
        im.paste(imavatar, (im_b, im_b, im_b+imavatar_h, im_b+imavatar_h), imavatar.convert('RGBA'))

    #attr
    i = 0
    for k,v in data['attr'].items():
        text_size = font.getsize(str(v))
        draw.text((imavatar_h+im_b*2, im_b+(font_size+line_h)*i), k, attr_color, font=font)
        draw.text((im_h*2-im_b-text_size[0], im_b+(font_size+line_h)*i), str(v), attr_color, font=font)
        i = i + 1

    #region-flag
    logo_h = 64
    logo_b = 12
    logo_r = im_h*2 - im_b
    try:
        data['region']
    except KeyError:
        pass
    else:
        imflag = Image.new('RGBA', (logo_h*2,logo_h))
        flag = Image.open('region-flag/'+data['region']+'.png')

        if flag.size[0] >= flag.size[1]*2 :
            flag = flag.resize((logo_h*2, int(logo_h*2*flag.size[1]/flag.size[0])))
            imflag.paste(flag, (0, int((logo_h-flag.size[1])/2), logo_h*2, int((logo_h+flag.size[1])/2)))
        else:
            flag = flag.resize((int(logo_h*flag.size[0]/flag.size[1]), logo_h))
            imflag.paste(flag, (int((logo_h*2-flag.size[0])/2), 0, int((logo_h*2+flag.size[0])/2), logo_h))
        imflag.filter(ImageFilter.SMOOTH)
        im.paste(imflag, (logo_r-logo_h*2, im_h-im_b-logo_h, logo_r, im_h-im_b), imflag.convert('RGBA'))
        logo_r = logo_r - logo_b - imflag.size[0]

    #logos
    try:
        data['logos']
    except KeyError:
        pass
    else:
        i = 0
        for v in data['logos']:
            if isinstance(v, str):
                imlogo = Image.open(v)
                imlogo = imlogo.resize((int(logo_h*imlogo.size[0]/imlogo.size[1]), logo_h))
                im.paste(imlogo, (logo_r-imlogo.size[0], im_h-im_b-logo_h, logo_r, im_h-im_b), imlogo.convert('RGBA'))
                logo_r = logo_r - logo_b - imlogo.size[0]
            else:
                pass

    im.save(f, 'png')
    data = f.getvalue()
    f.close()

    return data

def border(img, width = 1, color = '#000'):
    scale = 3
    origin_size = img.size
    img = img.resize((img.size[0]*scale,img.size[1]*scale))
    bg = Image.new('RGBA', (img.size[0]+width*2, img.size[1]+width*2), ImageColor.getrgb(color))
    bg.paste(img, (width,width))
    img = bg.resize(origin_size)
    return img

def circle_border(img, radii, width = 1, color = '#000'):
    scale = 3
    origin_size = img.size
    img = img.resize((img.size[0]*scale,img.size[1]*scale))
    bg = Image.new('RGBA', (img.size[0]+width*2, img.size[1]+width*2), ImageColor.getrgb(color))
    bg = circle_corner(bg, radii*scale)
    bg.paste(Image.new('RGBA', img.size), (width, width), img)
    bg.paste(img, (width,width), img)
    img = bg.resize(origin_size)
    return img

def circle_corner(img, radii, corner = (1,1,1,1)):
    """
    圆角处理
    :param img: 源图象。
    :param radii: 半径，如：30。
    :param corner: 要处理的角落，顺序为：左上右上左下右下
    :return: 返回一个圆角处理后的图象。
    """

    # 原图
    scale = 3
    img = img.convert("RGBA")
    origin_size = img.size
    w, h = img.size
    radii *= scale; w *= scale; h *= scale
    
    img = img.resize((w,h), Image.ANTIALIAS)

    # 画圆（用于分离4个角）
    circle = Image.new('1', (radii * 2, radii * 2), 0)  # 创建一个黑色背景的画布
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, radii * 2, radii * 2), fill=255)  # 画白色圆形

    # 画4个角（将整圆分离为4个部分）
    alpha = Image.new('1', (w,h), 255)
    if corner[0]: alpha.paste(circle.crop((0, 0, radii, radii)), (0, 0))  # 左上角
    if corner[1]: alpha.paste(circle.crop((radii, 0, radii * 2, radii)), (w - radii, 0))  # 右上角
    if corner[2]: alpha.paste(circle.crop((0, radii, radii, radii * 2)), (0, h - radii))  # 左下角
    if corner[3]: alpha.paste(circle.crop((radii, radii, radii * 2, radii * 2)), (w - radii, h - radii))  # 右下角

    imgn = Image.new('RGBA', (w,h))
    # 接着直接使用其作为模板粘贴即可
    imgn.paste(img, (0, 0), mask=alpha)

    # 使用ANTIALIAS采样器缩小图像
    imgn = imgn.resize(origin_size, Image.ANTIALIAS)

    return imgn