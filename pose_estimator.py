import tensorflow as tf
import numpy as np
import cv2
from rknn.api import RKNN

class PoseEstimator:
    def __init__(self, model):
        # 配置模型
        self.model = model

    @staticmethod
    def _im_normalize(img):
        return np.ascontiguousarray(
            2 * ((img / 255) - 0.5
                 ).astype('float32'))

    def preprocess_img(self, img):
        # fit the image into a 256x256 square
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        shape = np.r_[img.shape]
        pad = (shape.max() - shape[:2]).astype('uint32') // 2
        img_pad = np.pad(
            img,
            ((pad[0], pad[0]), (pad[1], pad[1]), (0, 0)),
            mode='constant')
        img_small = cv2.resize(img_pad, (256, 256))
        img_small = np.ascontiguousarray(img_small)

        img_norm = self._im_normalize(img_small)
        return img_pad, img_norm, pad

    def process(self, image):
        img_pad, img_norm, pad = self.preprocess_img(image)
        tensor = img_norm.reshape(1, 256, 256, 3)
        output = self.model.inference(inputs=[tensor])
        print(output)
        points = output[0].reshape(-1, 5)[:, :2]
        scale = img_pad.shape[0] / 256
        for point in points:
            point *= scale
        return points

