import cv2
import imutils
from PIL import Image
import time


img = cv2.imread('output3/imagen.jpeg',cv2.IMREAD_GRAYSCALE)
# mascara con area a remover. Zona negra (0,0,0) se remueve, Blanca se deja(255,255,255)
mask = cv2.imread("output3/mask.jpeg")

square_size = 8

half_square = square_size//2


#shapeMask = jpeg2MatrixMask(mask)

def procesar(imagen, mask, iteraciones):
    # re-mapeamos a 0 y 255 la mascara. 255: zona a retocar, 0 a no retocar.
    shapeMask = jpeg2MatrixMask(mask)
#     # matriz de confianza, 0 o 1, si no se retoca es 1
    c = shapeMask[:, :] == 0
    for iteracion in range(iteraciones):
        shapeMask = jpeg2MatrixMask(mask)
        cnts = cv2.findContours(shapeMask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        cnts = imutils.grab_contours(cnts)

        gradient = getGradient(img)
        gx, gy = gradient
        grad_norm = np.square(gx) + np.square(gy)
#     for it in iteraciones:
#         priority = 

        



# start_time = time.time()
# iteraciones = 5000
# procesar(img, mask,iteraciones)
# end_time = time.time()
# print("se calculo en:", (end_time-start_time)/60, " minutos")
