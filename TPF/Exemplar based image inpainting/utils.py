import numpy as np
import random
import cv2
import numba
from numba import jit

def genSquare(square_size):
    first = True
    for i in range(square_size):
        for j in range(square_size):
            aux = np.array([i - square_size // 2, j - square_size // 2])
            if first:
                square = np.array([aux])
                first = False
            else:
                square = np.append(square, np.array([aux]), axis=0)
    return square


def jpeg2MatrixMask(mask):
    # lower y upper son bounds para buscar el color negro con la funcion inRange
    lower = np.array([0, 0, 0])
    upper = np.array([15, 15, 15])
    # re-mapeamos a 0 y 255 la mascara. 255: zona a retocar, 0 a no retocar.
    shapeMask = cv2.inRange(mask, lower, upper)
    return shapeMask


def getGradient(grey_scale):
    # gradiente en x e y de la escala de grises, sobel suaviza el gradiente
    sobel_x = cv2.Sobel(grey_scale, cv2.CV_64F, 1, 0, ksize=5)
    sobel_y = cv2.Sobel(grey_scale, cv2.CV_64F, 0, 1, ksize=5)

    return sobel_x, sobel_y

def drawRect(image, pos, sq_sz, color):
    x, y = pos
    for i in range(-sq_sz // 2, sq_sz // 2+1):
        for j in range(-sq_sz // 2, sq_sz // 2+1):
            image[y + i][x + j] = color
    return

def getMaxGrad(square, shapeMask, x, y, gx, gy, grad_norm, square_size):
    max_grad = [None,None]
    max_grad_norm = -1e10
    for i in range(len(square)):
       dx = square[i][0]
       dy = square[i][1]
#        solo sumamos si esta fuera de la zona a retocar
       if shapeMask[y + dy][x + dx] == 0:
            p = grad_norm[y+dy][x+dx]
            if p > max_grad_norm:  # buscamos el mayor gradiente en norma
                max_grad_norm = p
                max_grad = gx[y + dy][x + dx], gy[y + dy][x + dx]
    
    return max_grad


@jit(nopython=True)
def getDistance(imagen,sq_sz,x,y,px,py):
    return np.sum(np.square(imagen[y-sq_sz//2: y+sq_sz//2+1][x-sq_sz//2: x+sq_sz//2+1]-
           imagen[py-sq_sz//2: py+sq_sz//2+1][px-sq_sz//2: px+sq_sz//2+1]))

def copyPattern(imagen, square_size, best_benefit_point, minDistPatch, c, mask):
    py,px= best_benefit_point
    by,bx = minDistPatch
    
    # copia patch a zona reemplazar (el patron)
    half_sq = square_size // 2

    aux = mask[py - half_sq: py + half_sq+1, px - half_sq: px + half_sq+1].copy()
    aux = (255*np.ones_like(aux)).astype(np.uint8)
    # mask tiene 3 dimenisiones q carajos

    aux2 = imagen[py - half_sq: py + half_sq+1, px - half_sq: px + half_sq+1].copy()
    aux2 = (255*np.ones_like(aux2)).astype(np.uint8)


#    imagen[py - half_sq: py + half_sq+1, px - half_sq: px + half_sq+1] = aux2

    imagen[py - half_sq: py + half_sq+1, px - half_sq: px + half_sq+1] = \
        imagen[by - half_sq: by + half_sq+1, bx - half_sq: bx + half_sq+1]


    ## copiamos la confianza del parche elegido a la la confianza del lugar donde copiamos el parche
    c[py - half_sq: py + half_sq+1, px - half_sq: px + half_sq+1] = \
        c[by - half_sq: by + half_sq+1, bx - half_sq: bx + half_sq+1] 

    ## marcamos la zona reemplazada como blanca ACA SEGURO HAY ALTO BUG
 #   np.ones_like(())
    
    mask[py - half_sq: py + half_sq+1, px - half_sq: px + half_sq+1] = aux #np.array([255, 255, 255])
    return imagen


def getBorderNormals(borde):
    n = len(borde)
    border_normal_list = []

    for i in range(n):
        dx = borde[i][0] - borde[(i - 1)%n][0]
        dy = borde[i][1] - borde[(i - 1)%n][1]
        normal_dir = np.array([dy,dx])
        normalize_factor = np.linalg.norm(normal_dir)              
        normal = normal_dir/normalize_factor
        border_normal_list.append(normal)
        # esta formula nos da la normal. no le damos importancia a la orientacion
    return border_normal_list.copy()


def getMinDistPatch(best_benefit_point,search_times,search_square_size,shapeMask,imagen,square_size):
    py,px = best_benefit_point

    best_patch = py, px  # default
    patch_distance = np.Infinity

    for j in range(search_square_size):
        for k in range(search_square_size):
            x = k + px - square_size // 2
            y = j + py - square_size // 2

            # ESTA ES LA LINEA QUE HACE QUE DEJE ANDAR
#            if sub_mat.max() == 255:
            if shapeMask[y,x] == 255:# me importa q toda la cosa no sea blanca
#            no solo el elemento
                continue
            else:
                dist = getDistance(imagen, square_size, x, y, px, py)
                if dist < patch_distance:
                    patch_distance = dist
                    #last_patch_distance
                    best_patch = y, x
    return best_patch



def getPriority(border_point_pos, border_normal, gx,gy , square, shapeMask, confidence,grad_norm, square_size):
    x, y = border_point_pos # esto esta bien!
    nx, ny = border_normal
    npx, npy = ny,-nx

    maxgx,maxgy = getMaxGrad(square, shapeMask, x, y, gx, gy,grad_norm, square_size)
    maxgxp,maxgyp = maxgy,-maxgx

    np_ = np.array([npx,npy])
    nabblap = np.array([maxgxp,maxgyp])
 
    d = abs(np.dot(nabblap,np_))

    priority = d* confidence

    return priority
