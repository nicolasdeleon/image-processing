import numpy as np

pre_matrix = np.array([
    [1, 0, 0, 0],
    [0, 0, 1, 0],
    [-3, 3, -2, -1],
    [2, -2, 1, 1]
])
post_matrix = np.array([
    [1, 0, -3, 2],
    [0, 0, 3, -2],
    [0, 1, -2, 1],
    [0, 0, -1, 1]
])

def fx_(vec, X, Y):
    b = vec[X - 1][Y] if X>0  else 0
    a = vec[X + 1][Y] if X<vec.shape[0]-1 else 0
    return (a - b) / 2

def fy_(vec, X, Y):
    b = vec[X][Y - 1] if Y>0  else 0
    a = vec[X][Y + 1] if Y<vec.shape[1]-1 else 0

    return (a - b) / 2

def fxy_(vec, X, Y):
    a = vec[X - 1][Y - 1] if X>0 and Y>0  else 0 
    b = vec[X + 1][Y + 1] if X<vec.shape[1]-1 and Y<vec.shape[1]-1 else 0 
    c = vec[X + 1][Y - 1] if X<vec.shape[1]-1 and Y>0 else 0 
    d = vec[X - 1][Y + 1] if X>0 and Y<vec.shape[1]-1 else 0 
    return (a + b - c - d) / 4

def get_derivatives(img,m,n):
    fx = np.zeros((m+1,n+1))
    fy = np.zeros((m+1,n+1))
    fxy = np.zeros((m+1,n+1))
    for i in range(m):
        for j in range(n):
            fx[i][j] = fx_(img,i,j)
            fy[i][j] = fy_(img,i,j)
            fxy[i][j] = fxy_(img,i,j)
    return fx,fy,fxy

def get_f_matrix(f,fx,fy,fxy,x,y):
    #f es la imagen
    # f_mat = np.array([  [ f[0,0] , f[0,1], fy[0,0], fy[0,1]],
    #                     [ f[1,0] , f[1,1], fy[1,0], fy[1,1]],
    #                     [ fx[0,0], fx[0,1], fxy[0,0], fxy[0,1] ],
    #                     [ fx[1,0], fx[1,1], fxy[1,0], fxy[1,1]]
    #                     ])
    # con ctrl h fui reemplazando

    f_mat = np.array([  [ f[x,y] , f[x,y+1], fy[x,y], fy[x,y+1]],
                        [ f[x+1,y] , f[x+1,y+1], fy[x+1,y], fy[x+1,y+1]],
                        [ fx[x,y], fx[x,y+1], fxy[x,y], fxy[x,y+1] ],
                        [ fx[x+1,y], fx[x+1,y+1], fxy[x+1,y], fxy[x+1,y+1]]
                        ])
    


    return f_mat