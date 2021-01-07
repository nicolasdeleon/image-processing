from PIL import Image

def change_contrast(img, level):

    factor = (259 * (level+255)) / (255 * (259-level))
    for x in range(img.size[0]):
        for y in range(img.size[1]):
            color = img.getpixel((x, y))
            new_color = tuple(int(factor * (c-128) + 128) for c in color)
            img.putpixel((x, y), new_color)

    return img

img = Image.open("lenna.jpg")
img.load()

result = change_contrast(img, 100)
result.save("lenna2.png")