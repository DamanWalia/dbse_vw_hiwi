from skimage.metrics import structural_similarity as ssim   # conda install scikit-image
from skimage.metrics import peak_signal_noise_ratio as psnr # conda install scikit-image
import numpy as np                                          # conda install numpy
import cv2                                                  # conda install -c conda-forge opencv

def mse(imageA, imageB):
    """
    Mean squared error
    """
    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1])
    return err


def compare_image(imageA, imageB):
    """
    Assesses image quality
    """
    m = mse(imageA, imageB)
    s = ssim(imageA, imageB)
    p = psnr(imageA,imageB)
    print('PSNR: {}, SSIM: {}'.format(round(p,2), round(s,2)))

def prepare_images(imageA,imageB):
    """
    Converts image to grayscale prior to image quality assessment
    """
    a = cv2.imread(imageA)
    b = cv2.imread(imageB)

    a = cv2.cvtColor(a,cv2.COLOR_BGR2GRAY)
    b = cv2.cvtColor(b,cv2.COLOR_BGR2GRAY)
    return a,b

a,b = prepare_images('frame_actual.png','frame_0.png')
compare_image(a,b)


