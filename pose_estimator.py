import numpy as np
import cv2
from rknn.api import RKNN
import prepocess

class PoseEstimator:
    def __init__(self, model_path, dataset_path):

        self.INPUT_WIDTH = 256
        self.INPUT_HEIGHT = 256
        self.INPUT_CHANNEL = 3


        # Create RKNN object
        self.rknn = RKNN(verbose=True)

        # Pre-process config
        print('--> Config model')
        self.rknn.config(mean_values=[0, 0, 0], std_values=[1, 1, 1], target_platform='rk3588')
        print('done')

        # Load model
        print('--> Loading model')
        ret = self.rknn.load_tflite(model=model_path)
        if ret != 0:
            print('Load model failed!')
            exit(ret)
        print('done')

        # Build model
        print('--> Building model')
        ret = self.rknn.build(do_quantization=False, dataset=dataset_path)
        if ret != 0:
            print('Build model failed!')
            exit(ret)
        print('done')

            # Init runtime environment
        print('--> Init runtime environment')
        ret = self.rknn.init_runtime()
        if ret != 0:
            print('Init runtime environment failed!')
            exit(ret)
        print('done')

    # def __del__(self):
    #     if self.rknn:
    #         self.rknn.release()

    def _preprocess(self, img):
        
        img_pad, pad = prepocess.pad(img)

        img_small = cv2.resize(img_pad, (self.INPUT_WIDTH, self.INPUT_HEIGHT))
        img_small = np.ascontiguousarray(img_small)

        img_norm = prepocess.img_normalize(img_small)
        return img_pad, img_norm, pad
    
    def _postprocess(self, data, pad, scale):
        points = data[0].reshape(-1, 5)[:, :3]
        result = []
        for point in points:
            point *= scale
            point[0] -= pad[1]
            point[1] -= pad[0]
            result.append(point)
        return np.array(result)
    def inference(self, image):
        img_pad, img_norm, pad = self._preprocess(image)
        tensor = img_norm.reshape(1, self.INPUT_WIDTH, self.INPUT_HEIGHT, self.INPUT_CHANNEL)
        output = self.rknn.inference(inputs=[tensor])

        scale = img_pad.shape[0] / self.INPUT_WIDTH

        points = self._postprocess(output, pad, scale)

        return points

