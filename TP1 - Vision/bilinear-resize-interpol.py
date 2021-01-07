import matplotlib.pyplot as plt
import cv2
import numpy as np

img = cv2.imread("mono.bmp", cv2.IMREAD_GRAYSCALE)

def resize_bilinear_interpol(img, scale):
    new_img = np.zeros((img.shape[0] * scale, img.shape[1] * scale), dtype=np.uint8)
    new_img[::scale, ::scale] = img[::]

    def inter_pol_1D(X, X1, X2, val_X1_cte, val_X2_cte):
        return (abs(X2 - X) / abs(X2 - X1)) * val_X1_cte + (abs(X - X1) / abs(X2 - X1)) * val_X2_cte

    for x in range(new_img.shape[0]):
        for y in range(new_img.shape[1]):
            y1 = y // scale
            y2 = (y + scale) // scale
            x1 = x // scale
            x2 = (x + scale) // scale
            try:
                if(x2 not in range(img.shape[0]) and y2 not in range(img.shape[0])):
                    new_img[x, y] = inter_pol_1D(y, y1*scale, y2*scale,
                        inter_pol_1D(x, x1*scale, x2*scale, img[x1, y1], 0),
                        inter_pol_1D(x, x1*scale, x2*scale, 0, 0)
                        )
                elif(x2 not in range(img.shape[0])):
                    new_img[x, y] = inter_pol_1D(y, y1*scale, y2*scale,
                        inter_pol_1D(x, x1*scale, x2*scale, img[x1, y1], 0),
                        inter_pol_1D(x, x1*scale, x2*scale, img[x1, y2], 0)
                        )
                elif(y2 not in range(img.shape[0])):
                    new_img[x, y] = inter_pol_1D(y, y1*scale, y2*scale,
                        inter_pol_1D(x, x1*scale, x2*scale, img[x1, y1], img[x2, y1]),
                        inter_pol_1D(x, x1*scale, x2*scale, 0, 0)
                        )
                else:
                    new_img[x, y] = inter_pol_1D(y, y1*scale, y2*scale,
                        inter_pol_1D(x, x1*scale, x2*scale, img[x1, y1], img[x2, y1]),
                        inter_pol_1D(x, x1*scale, x2*scale, img[x1, y2], img[x2, y2])
                        )
            except IndexError:
                print(f'Failed at {x}, {y}')

    return new_img

img_bilinear = resize_bilinear_interpol(img[1::4, 1::4], 4)
img_bilinear_cv2 = cv2.resize(img[1::4, 1::4], (256, 256), cv2.INTER_LINEAR)
img_packed = cv2.hconcat([img_bilinear_cv2, img_bilinear])
plt.imshow(img_packed, cmap="gray", vmin=0, vmax=255)
plt.show()
