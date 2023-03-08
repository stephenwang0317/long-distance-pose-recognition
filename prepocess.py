import cv2
import numpy as np


def img_normalize(orig_img):
    return np.ascontiguousarray(
        2 * ((orig_img / 255) - 0.5
                ).astype('float32'))

def toRgb(orig_img):
    img = cv2.cvtColor(orig_img, cv2.COLOR_BGR2RGB)
    return img

def toRgb(orig_img):
    img = cv2.cvtColor(orig_img, cv2.COLOR_RGB2BGR)
    return img

def pad(orig_img):
    # fit the image into a 256x256 square
    shape = np.r_[orig_img.shape]
    pad = (shape.max() - shape[:2]).astype('uint32') // 2
    img_pad = np.pad(
        orig_img,
        ((pad[0], pad[0]), (pad[1], pad[1]), (0, 0)),
        mode='constant')
    return img_pad, pad