
from PIL import Image, ImageEnhance 

im = Image.open("lenna.jpg")
enhancer = ImageEnhance.Brightness(im)
enhanced_im = enhancer.enhance(1.8)
enhanced_im.save("lenna2.jpg")
