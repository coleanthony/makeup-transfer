import cv2
import os

class DP_Graph(object):
    def __init__(self):
        self.class_name = os.getcwd()
        self.index = 1
        self.cap = cv2.VideoCapture(0)
        self.width = 640
        self.height = 480
        self.w = 400
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)

        self.crop_w_start = (self.width - self.w) // 2
        self.crop_h_start = (self.height - self.w) // 2


    def takephoto(self):
        while True:
            # get a frame
            ret, frame = self.cap.read()
            # show a frame
            frame = frame[self.crop_h_start:self.crop_h_start + self.w, self.crop_w_start:self.crop_w_start + self.w]
            frame = cv2.flip(frame, 1, dst=None)
            cv2.imshow("capture", frame)

            input = cv2.waitKey(1) & 0xFF

            if input == ord('x'):
                cv2.imwrite("%s/%d.jpg" % (self.class_name, self.index),
                    cv2.resize(frame, (256, 256), interpolation=cv2.INTER_AREA))
                print("%s: %d 张图片" % (self.class_name, self.index))
                self.index += 1
            if input == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()
