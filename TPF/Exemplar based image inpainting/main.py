import cv2
import imutils
from PIL import Image
import time
from utils import *

img = cv2.imread('output3/imagen.jpeg', cv2.IMREAD_GRAYSCALE)# matriz, cada el es un RGB
# mascara con area a remover. Zona negra (0,0,0) se remueve, Blanca se deja(255,255,255)
mask = cv2.imread("output3/mask.jpeg")

#lado de los cuadrados que utilizaremos para rellenar la imagen
square_size = 8
# guardamos en un arreglo las coordenadas que describen al cuadrado
square = genSquare(square_size)

# tamanio del cuadrado de busqueda para el parche que reemplaza la posicion a rellenear
search_square_size = 32

# cuantas veces buscamos al azar por un parche
search_times = 100

def procesar(imagen, mask, iteraciones):
    # re-mapeamos a 0 y 255 la mascara. 255: zona a retocar, 0 a no retocar.
    shapeMask = jpeg2MatrixMask(mask)
    # matriz de confianza, 0 o 1, si no se retoca es 1
    c = shapeMask[:, :] == 0

    for iteracion in range(iteraciones):

        best_benefit = -100 # benefit usulamente da >0
        best_benefit_point = None

        shapeMask = jpeg2MatrixMask(mask)

        # detectamos el borde de la mascara y conseguimos un arreglo con todos los contornos
        # cnts me da los contornos cerrados (los que se van achicando segun el algoritmo)
#        cnts = cv2.findContours(image=shapeMask.copy(),mode=cv2.RETR_EXTERNAL,method=cv2.CHAIN_APPROX_NONE)
        ret, thresh = cv2.threshold(shapeMask.copy(), 127, 255, 0)
        cnts = cv2.findContours(image=thresh,mode=cv2.RETR_EXTERNAL,method=cv2.CHAIN_APPROX_NONE)
        cnts = imutils.grab_contours(cnts)

        gradient = getGradient(imagen)
        gx, gy = gradient
        grad_norm = np.square(gx) + np.square(gy)

        for borde in cnts:
            borde = borde.reshape((len(borde),2)) 

            border_normals = getBorderNormals(borde)
            for idx,border_point in enumerate(borde):
                x, y = border_point # esto esta bien!

#                drawRect(imagen, [x,y], 10, 255)

                # consigo la confianza del punto del contorno actual
                confidence = 0

                for dx, dy in square:
                    if shapeMask[y + dy, x + dx] == 0: # si fuera de la region a retocar
                        confidence += c[y + dy, x + dx]

                confidence /= len(square)

                border_norm = border_normals[idx]
                benefit = getPriority(border_point,border_norm,gx,gy ,square,shapeMask,confidence,grad_norm, square_size)
#                print("benefit esta vez",benefit)
                # buscamos maximizar el beneficio
                if benefit > best_benefit:
                    best_benefit = benefit
                    best_benefit_point = y, x

        # no termina 
        # if not best_benefit_point:
        #     print("No hay mas bordes. Fin")
        #     break

        # ahora vamos a calcular el parche que minimize la distancia
        minDistPatch = getMinDistPatch(best_benefit_point, search_times, search_square_size, shapeMask,imagen, square_size)
        imagen = copyPattern(imagen, square_size, best_benefit_point, minDistPatch, c, mask)

        if iteracion % 20 == 0:
            print("Iteracion ", iteracion)
            im2 = Image.fromarray(mask)
            im2.save("output3/mask" + str(iteracion) + ".jpeg")
            im = Image.fromarray(imagen)
            im.save("output3/imagen" + str(iteracion) + ".jpeg")


start_time = time.time()
iteraciones = 20000
procesar(img, mask,iteraciones)
end_time = time.time()
print("se calculo en:", (end_time-start_time)/60, " minutos")