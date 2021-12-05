from skimage.metrics import structural_similarity as ssim
from skimage.metrics import peak_signal_noise_ratio as psnr
import numpy as np
import cv2
from tifffile import imread
from PIL import Image
import os

dirname = os.path.dirname(__file__)
print(dirname)

def mse(imageA, imageB):
    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1])
    return err


def compare_image(imageA, imageB, title):
    m = mse(imageA, imageB)
    s = ssim(imageA, imageB)
    p = psnr(imageA,imageB)
    print('{} PSNR: {}, SSIM: {}'.format(title, round(p,2), round(s,2)))

def prepare_images(imageA,imageB):
    a = cv2.imread(imageA)
    b = cv2.imread(imageB)

    a = cv2.cvtColor(a,cv2.COLOR_BGR2GRAY)
    b = cv2.cvtColor(b,cv2.COLOR_BGR2GRAY)
    return a,b

a,b = prepare_images('frame_actual.png','frame_0.png')
compare_image(a,b,'ssim')


