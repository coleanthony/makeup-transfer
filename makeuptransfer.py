import tensorflow as tf
import numpy as np
import os
import glob
from imageio import imread, imsave
import cv2

class BeautyGAN(object):
    def __init__(self):
        self.batch_size=1   #只训练一轮
        self.img_size=256   #beautygan用力vgg网络，所以图片大小为256*256
        self.result=None

    def preprocess(self,img):
        return (img / 255. - 0.5) * 2

    def deprocess(self,img):
        return (img + 1) / 2

    def process(self,nomakeup,mkup):
        path=nomakeup    #读取未化妆图像
        no_makeup = cv2.resize(imread(path), (self.img_size, self.img_size))  #修改大小

        X_img = np.expand_dims(self.preprocess(no_makeup), 0)
        makeups = glob.glob(mkup)     #读取化妆图
        result = np.ones((self.img_size, self.img_size, 3))   #定义result的格式
        #result[self.img_size: 2 * self.img_size, :self.img_size] = no_makeup / 255.    #像素点要归一


        tf.reset_default_graph()
        sess = tf.Session()
        sess.run(tf.global_variables_initializer())    #初始化一个session

        saver = tf.train.import_meta_graph(os.path.join('model', 'model.meta'))
        saver.restore(sess, tf.train.latest_checkpoint('model'))      #加载训练模型

        graph = tf.get_default_graph()    #获取当前默认的计算图
        X = graph.get_tensor_by_name('X:0')   #
        Y = graph.get_tensor_by_name('Y:0')
        Xs = graph.get_tensor_by_name('generator/xs:0')

        for i in range(len(makeups)):#可以一次性传入多张makeup的图片
            makeup = cv2.resize(imread(makeups[i]), (self.img_size, self.img_size))
            Y_img = np.expand_dims(self.preprocess(makeup), 0)
            Xs_ = sess.run(Xs, feed_dict={X: X_img, Y: Y_img})
            Xs_ = self.deprocess(Xs_)
            #result[:self.img_size, (i + 1) * self.img_size: (i + 2) * self.img_size] = makeup / 255.
            result = Xs_[0]
        self.result=result
        self.save()

    def save(self):
        imsave('Res/result.jpg', self.result)  #保存
















