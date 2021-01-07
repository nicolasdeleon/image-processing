import cv2
import matplotlib.pyplot as plt
import numpy as np
from skimage.transform import iradon, radon


class ImageFrame:
    def __init__(self, image=None):
        self.image = image if image else np.zeros((512, 512, ), np.uint8)
        self.n_ovals = 0
        self.ovals = []

    def add_oval(self, oval):
        try:
            assert type(oval) == Oval
            self.ovals.append(oval)
        except TypeError:
            raise AssertionError('Input variable should be oval')

    def clear_ovals(self):
        self.ovals = []
        self.image = np.zeros((512, 512, ), np.float64)

    def apply_ovals(self):
        frames = []
        how_to_norm = np.zeros_like(self.image)
        float_img = np.zeros_like(self.image).astype(np.float64)
        for oval in self.ovals:
            buffer_img = self.image.copy()
            img = cv2.ellipse(
                buffer_img.copy(),
                center=(oval.centroX, oval.centroY),
                axes=(oval.semiejeX, oval.semiejeY),
                angle=oval.inclinacion,
                startAngle=0,
                endAngle=360,
                color=self.__intensity2color(oval.intensidad),
                thickness=-1
                )
            intensity_img, htnorm = self.__color_to_intensity_normalized(img)
            how_to_norm += htnorm
            for i in range(float_img.shape[0]):
                for j in range(float_img.shape[1]):
                    if htnorm[i][j]:
                        float_img[i][j] += intensity_img[i][j]

        for i in range(how_to_norm.shape[0]):
            for j in range(how_to_norm.shape[1]):
                if how_to_norm[i][j] == 0:
                    float_img[i][j] = -1
                else:
                    float_img[i][j] /= how_to_norm[i][j]
                
                self.image[i][j] = int(np.interp(float_img[i][j], [-1, 1], [0, 255]))

    def __intensity2color(self, intensity):
        return int(np.interp(intensity, [-1, 1], [0, 255]))

    def __color_to_intensity_normalized(self, img):
        image = img.copy().astype(np.float64)
        ht_norm = np.zeros_like(img)
        count = 0
        for i in range(image.shape[0]):
            for j in range(image.shape[1]):
                if img[i][j] != 0.0:
                    ht_norm[i][j] += 1
                    count += 1
                image[i][j] = np.interp(image[i][j], [0, 255], [-1, 1])

        return image, ht_norm


class Oval:
    def __init__(self, intensidad, inclinacion, semiejeX, semiejeY, centroX, centroY):
        self.intensidad = intensidad
        self.inclinacion = inclinacion
        self.semiejeX = semiejeX
        self.semiejeY = semiejeY
        self.centroX = centroX
        self.centroY = centroY
