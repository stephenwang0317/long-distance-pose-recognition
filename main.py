import os
import urllib
import traceback
import time
import sys
import numpy as np
import cv2
from rknn.api import RKNN
import copy
from pose_estimator import PoseEstimator
from skeleton_render import SkeletonRender

YOLO_ONNX_MODEL = 'yolov5s.onnx'
MEDIAPIPE_TFLITE_MODEL =  'pose_landmark_full.tflite'
IMG_PATH = os.path.join(os.environ['HOME'], 'pic/5-0-1.png')
YOLO_DATASET = './dataset_yolo.txt'
MEDIAPIPE_DATASET = './dataset_mediapipe.txt'

QUANTIZE_ON = True

OBJ_THRESH = 0.25
NMS_THRESH = 0.45
IMG_SIZE = 640
EXTRA_PIXEL = 50

CLASSES = ("person", "bicycle", "car", "motorbike ", "aeroplane ", "bus ", "train", "truck ", "boat", "traffic light",
           "fire hydrant", "stop sign ", "parking meter", "bench", "bird", "cat", "dog ", "horse ", "sheep", "cow",
           "elephant",
           "bear", "zebra ", "giraffe", "backpack", "umbrella", "handbag", "tie", "suitcase", "frisbee", "skis",
           "snowboard", "sports ball", "kite",
           "baseball bat", "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup",
           "fork", "knife ",
           "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli", "carrot", "hot dog", "pizza ", "donut",
           "cake", "chair", "sofa",
           "pottedplant", "bed", "diningtable", "toilet ", "tvmonitor", "laptop	", "mouse	", "remote ",
           "keyboard ", "cell phone", "microwave ",
           "oven ", "toaster", "sink", "refrigerator ", "book", "clock", "vase", "scissors ", "teddy bear ",
           "hair drier", "toothbrush ")


def padding(img):
    shape = img.shape
    max_side = max(shape[0], shape[1])

    img2 = cv2.copyMakeBorder(img, int((max_side - shape[0]) / 2), int((max_side - shape[0]) / 2),
                              int((max_side - shape[1]) / 2), int((max_side - shape[1]) / 2), cv2.BORDER_CONSTANT,
                              value=[0, 255, 0])
    return img2


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def xywh2xyxy(x):
    # Convert [x, y, w, h] to [x1, y1, x2, y2]
    y = np.copy(x)
    y[:, 0] = x[:, 0] - x[:, 2] / 2  # top left x
    y[:, 1] = x[:, 1] - x[:, 3] / 2  # top left y
    y[:, 2] = x[:, 0] + x[:, 2] / 2  # bottom right x
    y[:, 3] = x[:, 1] + x[:, 3] / 2  # bottom right y
    return y


def process(input, mask, anchors):
    anchors = [anchors[i] for i in mask]
    grid_h, grid_w = map(int, input.shape[0:2])

    box_confidence = sigmoid(input[..., 4])
    box_confidence = np.expand_dims(box_confidence, axis=-1)

    box_class_probs = sigmoid(input[..., 5:])

    box_xy = sigmoid(input[..., :2]) * 2 - 0.5

    col = np.tile(np.arange(0, grid_w), grid_w).reshape(-1, grid_w)
    row = np.tile(np.arange(0, grid_h).reshape(-1, 1), grid_h)
    col = col.reshape(grid_h, grid_w, 1, 1).repeat(3, axis=-2)
    row = row.reshape(grid_h, grid_w, 1, 1).repeat(3, axis=-2)
    grid = np.concatenate((col, row), axis=-1)
    box_xy += grid
    box_xy *= int(IMG_SIZE / grid_h)

    box_wh = pow(sigmoid(input[..., 2:4]) * 2, 2)
    box_wh = box_wh * anchors

    box = np.concatenate((box_xy, box_wh), axis=-1)

    return box, box_confidence, box_class_probs


def filter_boxes(boxes, box_confidences, box_class_probs):
    """Filter boxes with box threshold. It's a bit different with origin yolov5 post process!

    # Arguments
        boxes: ndarray, boxes of objects.
        box_confidences: ndarray, confidences of objects.
        box_class_probs: ndarray, class_probs of objects.

    # Returns
        boxes: ndarray, filtered boxes.
        classes: ndarray, classes for boxes.
        scores: ndarray, scores for boxes.
    """
    boxes = boxes.reshape(-1, 4)
    box_confidences = box_confidences.reshape(-1)
    box_class_probs = box_class_probs.reshape(-1, box_class_probs.shape[-1])

    _box_pos = np.where(box_confidences >= OBJ_THRESH)
    boxes = boxes[_box_pos]
    box_confidences = box_confidences[_box_pos]
    box_class_probs = box_class_probs[_box_pos]

    class_max_score = np.max(box_class_probs, axis=-1)
    classes = np.argmax(box_class_probs, axis=-1)
    _class_pos = np.where(class_max_score >= OBJ_THRESH)

    boxes = boxes[_class_pos]
    classes = classes[_class_pos]
    scores = (class_max_score * box_confidences)[_class_pos]

    return boxes, classes, scores


def nms_boxes(boxes, scores):
    """Suppress non-maximal boxes.

    # Arguments
        boxes: ndarray, boxes of objects.
        scores: ndarray, scores of objects.

    # Returns
        keep: ndarray, index of effective boxes.
    """
    x = boxes[:, 0]
    y = boxes[:, 1]
    w = boxes[:, 2] - boxes[:, 0]
    h = boxes[:, 3] - boxes[:, 1]

    areas = w * h
    order = scores.argsort()[::-1]

    keep = []
    while order.size > 0:
        i = order[0]
        keep.append(i)

        xx1 = np.maximum(x[i], x[order[1:]])
        yy1 = np.maximum(y[i], y[order[1:]])
        xx2 = np.minimum(x[i] + w[i], x[order[1:]] + w[order[1:]])
        yy2 = np.minimum(y[i] + h[i], y[order[1:]] + h[order[1:]])

        w1 = np.maximum(0.0, xx2 - xx1 + 0.00001)
        h1 = np.maximum(0.0, yy2 - yy1 + 0.00001)
        inter = w1 * h1

        ovr = inter / (areas[i] + areas[order[1:]] - inter)
        inds = np.where(ovr <= NMS_THRESH)[0]
        order = order[inds + 1]
    keep = np.array(keep)
    return keep


def yolov5_post_process(input_data):
    masks = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
    anchors = [[10, 13], [16, 30], [33, 23], [30, 61], [62, 45],
               [59, 119], [116, 90], [156, 198], [373, 326]]

    boxes, classes, scores = [], [], []
    for input, mask in zip(input_data, masks):
        b, c, s = process(input, mask, anchors)
        b, c, s = filter_boxes(b, c, s)
        boxes.append(b)
        classes.append(c)
        scores.append(s)

    boxes = np.concatenate(boxes)
    boxes = xywh2xyxy(boxes)
    classes = np.concatenate(classes)
    scores = np.concatenate(scores)

    nboxes, nclasses, nscores = [], [], []
    for c in set(classes):
        inds = np.where(classes == c)
        b = boxes[inds]
        c = classes[inds]
        s = scores[inds]

        keep = nms_boxes(b, s)

        nboxes.append(b[keep])
        nclasses.append(c[keep])
        nscores.append(s[keep])

    if not nclasses and not nscores:
        return None, None, None

    boxes = np.concatenate(nboxes)
    classes = np.concatenate(nclasses)
    scores = np.concatenate(nscores)

    return boxes, classes, scores



def get_crop_img(img, boxes, scores, classes):
    for box, score, cl in zip(boxes, scores, classes):
        if cl != 0:
            continue

        top, left, right, bottom = box
        top -= EXTRA_PIXEL
        left -= EXTRA_PIXEL
        right += EXTRA_PIXEL
        bottom += EXTRA_PIXEL

        print('class: {}, score: {}'.format(CLASSES[cl], score))
        print('box coordinate left,top,right,down: [{}, {}, {}, {}]'.format(top, left, right, bottom))

        top = int(top)
        left = int(left)
        right = int(right)
        bottom = int(bottom)
        cv2.rectangle(img, (top, left), (right, bottom), (255, 0, 0), 2)

        return img[left:bottom, top:right]



if __name__ == '__main__':

    # Create RKNN object
    rknn = RKNN(verbose=True)
    rknn2 = RKNN(verbose=True)
    
    # pre-process config
    print('--> Config model')
    rknn.config(mean_values=[[0, 0, 0]], std_values=[[255, 255, 255]], target_platform='rk3588')
    rknn2.config(mean_values=[0, 0, 0], std_values=[1, 1, 1], target_platform='rk3588')
    print('done')

    # Load ONNX model
    print('--> Loading model')
    ret = rknn.load_onnx(model=YOLO_ONNX_MODEL)
    ret2 = rknn2.load_tflite(model=MEDIAPIPE_TFLITE_MODEL)
    if ret != 0 or ret2 != 0:
        print('Load model failed!')
        exit(1)
    print('done')

    # Build model
    print('--> Building model')
    ret = rknn.build(do_quantization=QUANTIZE_ON, dataset=YOLO_DATASET)
    ret2 = rknn2.build(do_quantization=False, dataset=MEDIAPIPE_DATASET)
    if ret != 0 or ret2 != 0:
        print('Build model failed!')
        exit(2)
    print('done')

    # Init runtime environment
    print('--> Init runtime environment')
    ret = rknn.init_runtime()
    ret2 = rknn2.init_runtime()
    # ret = rknn.init_runtime('rk3566')
    if ret != 0 or ret2 != 0:
        print('Init runtime environment failed!')
        exit(3)
    print('done')

    # Set inputs
    oriImg = cv2.imread(IMG_PATH)
    # img, ratio, (dw, dh) = letterbox(img, new_shape=(IMG_SIZE, IMG_SIZE))
    oriImg = cv2.cvtColor(oriImg, cv2.COLOR_BGR2RGB)
    paddingImg = padding(oriImg)
    img = cv2.resize(paddingImg, None, fx=IMG_SIZE / paddingImg.shape[0], fy=IMG_SIZE / paddingImg.shape[0])

    # Inference
    print('--> Running model')
    outputs = rknn.inference(inputs=[img])

    # post process
    input0_data = outputs[0]
    input1_data = outputs[1]
    input2_data = outputs[2]

    input0_data = input0_data.reshape([3, -1] + list(input0_data.shape[-2:]))
    input1_data = input1_data.reshape([3, -1] + list(input1_data.shape[-2:]))
    input2_data = input2_data.reshape([3, -1] + list(input2_data.shape[-2:]))

    input_data = list()
    input_data.append(np.transpose(input0_data, (2, 3, 0, 1)))
    input_data.append(np.transpose(input1_data, (2, 3, 0, 1)))
    input_data.append(np.transpose(input2_data, (2, 3, 0, 1)))

    boxes, classes, scores = yolov5_post_process(input_data)

    paddingImg = cv2.cvtColor(paddingImg, cv2.COLOR_RGB2BGR)
    if boxes is not None:
        # draw(paddingImg, boxes * (paddingImg.shape[0] / IMG_SIZE), scores, classes)
        cropImg = get_crop_img(paddingImg, boxes * (paddingImg.shape[0] / IMG_SIZE), scores, classes)
     
    
    # show output
    # cv2.imshow("cropImg", cropImg)
    pose_estimator = PoseEstimator(rknn2)
    points = pose_estimator.process(cropImg)
    sk_render = SkeletonRender()
    render_img = sk_render.render(image=oriImg, points=points, zero_point=(0, 0))
    cv2.namedWindow("oriImg", cv2.WINDOW_NORMAL)
    cv2.imshow('oriImg', oriImg)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    

    rknn.release()
    rknn2.release()
