from utils import *
import cv2
import matplotlib.pyplot as plt

img = cv2.imread("mono.bmp", cv2.IMREAD_GRAYSCALE)[::4,::4]
img = img.astype(np.float64)

m,n = img.shape
scale = 4
new_img = np.zeros((scale*m,scale*n))
new_img = new_img.astype(np.float64)

# tengo que iterar de a 2x2 depues lo llevo a (scale*2)x(scale*2)
# es con overlap, avanzo de a 1 paso entre cuadrados de 2x2

fx,fy,fxy = get_derivatives(img,m,n)

for i in range(m-1):
    for j in range(n-1):
        x,y = i,j
        alpha_vector = np.matmul(np.matmul(pre_matrix,get_f_matrix(img,fx,fy,fxy,x,y)),post_matrix)
        for k in range(scale): # expando un cuadradito de 1x1 a scalexscale
            for l in range(scale):
                x_ = k/(scale)
                y_ = l/(scale)

                cubic_x = np.array([1,x_, x_**2, x_**3])
                cubic_y = np.array([1,y_, y_**2, y_**3])

                new_img[x*scale+k,y*scale+l] = min(np.matmul(np.matmul(cubic_x,alpha_vector),cubic_y.T),255)

new_img = new_img.astype(np.uint8)

plt.imshow(new_img, cmap='gray', vmin=0, vmax=255)
plt.show()