import numpy as np
import cv2
from rknn.api import RKNN
from pose_estimator import PoseEstimator
from skeleton_render import SkeletonRender
import copy
import os

IMG_PATH = "cropImg.jpg"

def show_outputs(outputs):
    print(len(outputs))
    
    for output in outputs:
        print(output.shape)
    
    print(outputs)


if __name__ == '__main__':

    # Create RKNN object
    rknn = RKNN(verbose=True)

    # Pre-process config
    print('--> Config model')
    rknn.config(mean_values=[0, 0, 0], std_values=[1, 1, 1], target_platform='rk3588',)
    print('done')

    # Load model
    print('--> Loading model')
    ret = rknn.load_tflite(model='pose_landmark_full.tflite')
    if ret != 0:
        print('Load model failed!')
        exit(ret)
    print('done')

    # Build model
    print('--> Building model')
    ret = rknn.build(do_quantization=False, dataset='./dataset.txt')
    if ret != 0:
        print('Build model failed!')
        exit(ret)
    print('done')

    # Export rknn model

    
    # Set inputs
    img = cv2.imread(IMG_PATH)

    # Init runtime environment
    print('--> Init runtime environment')
    ret = rknn.init_runtime()
    if ret != 0:
        print('Init runtime environment failed!')
        exit(ret)
    print('done')

    # Inference
    print('--> Running model')
    pose_estimator = PoseEstimator(rknn)
    img2 = copy.deepcopy(img)
    points =  pose_estimator.process(img2)
    sk_render = SkeletonRender()
    render_img = sk_render.render(image=img, points=points, zero_point=(0,0))
    cv2.imshow("img2", render_img)
    cv2.waitKey(0)
    rknn.release()
