from PIL import Image, ImageDraw, ImageFont, ImageFilter
from io import BytesIO
import time

def siggen(data):
    im_h = 512; im_b = 40; font_size = 48; line_h = 12
    im = Image.new('RGBA', (im_h*2, im_h), 'white')
    draw = ImageDraw.Draw(im)
    
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
        im.paste(imavatar, (im_b, im_b, im_b+imavatar_h, im_b+imavatar_h), imavatar.convert('RGBA'))

    #attr
    i = 0
    for k,v in data['attr'].items():
        text_size = font.getsize(str(v))
        draw.text((imavatar_h+im_b*2, im_b+(font_size+line_h)*i), k, '#000', font=font)
        draw.text((im_h*2-im_b-text_size[0], im_b+(font_size+line_h)*i), str(v), '#000', font=font)
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
