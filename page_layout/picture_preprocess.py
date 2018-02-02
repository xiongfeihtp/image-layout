# ORB
import cv2
import numpy as np
from matplotlib import pyplot as plt


def Binarization(img):
    GrayImage=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    # 中值滤波
    GrayImage= cv2.medianBlur(GrayImage,5)
    ret,th1 = cv2.threshold(GrayImage,127,255,cv2.THRESH_BINARY)
    #3 为Block size, 5为param1值
    th2 = cv2.adaptiveThreshold(GrayImage,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
                        cv2.THRESH_BINARY,3,5)
    th3 = cv2.adaptiveThreshold(GrayImage,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
                        cv2.THRESH_BINARY,3,5)
    images = [GrayImage, th1, th2, th3]
    titles = ['Gray Image', 'Global Thresholding (v = 127)',
              'Adaptive Mean Thresholding', 'Adaptive Gaussian Thresholding']
    for i in range(4):
        plt.imshow(images[i], 'gray')
        plt.title(titles[i])
        plt.xticks([]), plt.yticks([])
        plt.show()
    return images


img1 = cv2.imread("./block0.jpeg")  # queryImage
#img2=cv2.imread("./convert_image/test/long_image1.jpeg")
# kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
# im = cv2.filter2D(img1, -1, kernel)
# cv2.imshow("Sharpening",im)

aw = cv2.addWeighted(img1, 4, cv2.blur(img1, (30, 30)), -4, 128)
cv2.imshow("Add_weighted", aw)
cv2.waitKey()

