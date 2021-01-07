import matplotlib.pyplot as plt
import numpy as np
import cv2

image = np.full((9,9),63,np.uint8)
image2 = np.full((9,9),223,np.uint8)
start_point = (3,3)
end_point = (5,5)
thickness = -1
color = 127
image = cv2.rectangle(image, start_point, end_point, color, thickness)  
image2 = cv2.rectangle(image2, start_point, end_point, color+20, thickness) # 147-157 seems nice
image_final = np.hstack((image,image2))
plt.imshow(image_final,cmap='gray', vmin=0, vmax=255)
plt.show()
