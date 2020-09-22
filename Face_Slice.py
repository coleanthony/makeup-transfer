import cv2
from utils.makeuptransfer import *

class face_slice(object):
    def __init__(self,image_path):
        self.image_path= image_path
        self.cascade = cv2.CascadeClassifier(r"haarcascade_frontalface_default.xml")

    def process(self):
        self.img = cv2.imread(self.image_path)
        self.gray = cv2.cvtColor(self.img,cv2.COLOR_BGR2GRAY)
        rect = self.cascade.detectMultiScale(self.gray,scaleFactor=1.1,minNeighbors=9,minSize=(50,50),flags = cv2.CASCADE_SCALE_IMAGE)

        if rect != ():
            for x,y,z,w in rect:
                roiImg = self.img[y:y+w,x:x+z]
                pathx=cv2.resize(roiImg,(256,256))
                cv2.imwrite('C:\\Users\cwh\Desktop\slice_res.jpg',pathx)
                #此处放入彩妆程序，得到化妆图

                beautygan=BeautyGAN()
                beautygan.process('C:\\Users\cwh\Desktop\slice_res.jpg','C:\\Users\cwh\Desktop\\30.jpg')

                #得到彩妆图后，加到原图片里，再保存
                proImg=cv2.imread('Res/result.jpg')
                pathx=cv2.resize(proImg,(w,z))
                self.img[y:y+w,x:x+z]=pathx[0:w,0:z]

cv2.imshow('img',img)
if cv2.waitKey(0)==27:
    cv2.destroyWindow("img")