from PIL import Image


def openImg(name):
    try:
        im = Image.open(name)
        return im
    except:
        print("open error")
        exit()


def pIx(Image_object):
    data = Image_object
    w = Image_object.width
    h = Image_object.height
    for x in range(1, w - 1):
        if x > 1 and x != w - 2:
            left = x - 1
            right = x + 1

        for y in range(1, h - 1):
            up = y - 1
            down = y + 1

            if x <= 2 or x >= (w - 2):
                data.putpixel((x, y), 255)

            elif y <= 2 or y >= (h - 2):
                data.putpixel((x, y), 255)

            elif data.getpixel((x, y)) == 0:
                if y > 1 and y != h - 1:
                    up_color = data.getpixel((x, up))
                    down_color = data.getpixel((x, down))
                    left_color = data.getpixel((left, y))
                    left_down_color = data.getpixel((left, down))
                    right_color = data.getpixel((right, y))
                    right_up_color = data.getpixel((right, up))
                    right_down_color = data.getpixel((right, down))

                    if down_color == 0:
                        if left_color == 255 and left_down_color == 255 and right_color == 255 and right_down_color == 255:
                            data.putpixel((x, y), 255)
                            data.save("text2.png", "png")

                    elif right_color == 0:
                        if down_color == 255 and right_down_color == 255 and up_color == 255 and right_up_color == 255:
                            data.putpixel((x, y), 255)
                            data.save("text3.png", "png")

                if left_color == 255 and right_color == 255 and up_color == 255 and down_color == 255:
                    data.putpixel((x, y), 255)
            else:
                pass
                data.save("test.png", "png")
picture_path='./sampel2/3.jpg'


threshold = 140
table = []
for i in range(256):
    if i < threshold:
        table.append(0)
    else:
        table.append(1)
img = openImg(picture_path)
imgry = img.convert('L')
out = imgry.point(table, '1')
pIx(out)


