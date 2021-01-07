import matplotlib.pyplot as plt
import cv2
import numpy as np
img = cv2.imread("mono.bmp")
#punto a
downsampled_monkey = img[1::4,1::4] # de 1 hasta el final saltando de a 4
#punto b
downsampled_dani = img[0::4,0::4]
#punto c 
aux_list = list(range(0,len(img),4))
c= np.array([np.mean(img[i:i+4,j:j+4]) for i in aux_list for j in aux_list])
c.resize( ( len(img)//4,len(img[0])//4 ) )

# plt.imshow(downsampled_monkey)
# plt.show()
# plt.imshow(downsampled_dani)
plt.imshow(c)
plt.show()