from pose_estimator import PoseEstimator
from skeleton_render import SkeletonRender
from human_detector import HumanDetector
from pose_recognitor import PoseRecognitor
from action_recognitor import ActionRecognitor
import prepocess
import cv2

if __name__ == '__main__':
    video_path = './dataset/pic/1.png'
    model_path1 = './model/yolov5s.onnx'
    dataset_path1 = './dataset/dataset1.txt'
    model_path2 = './model/pose_landmark_full.tflite'
    dataset_path2 = './dataset/dataset2.txt'
    detector = HumanDetector(model_path1, dataset_path1)
    estimator = PoseEstimator(model_path2, dataset_path2)
    render = SkeletonRender()
    pose_recognitor = PoseRecognitor()
    action_recognitor = ActionRecognitor()

    cap = cv2.VideoCapture(video_path)

    hasFrame, frame = cap.read()
    while hasFrame:
        
        img_rgb = prepocess.toRgb(frame)

        left, right, top, bottom = detector.inference(img_rgb)
        print(left, right, top, bottom)
        person_img = img_rgb[top:bottom, left:right]
        #dim1是行数，所以上下代表从第几行到第几行，同理左右
        points =  estimator.inference(person_img)
        points_xy = points[:, :2]
        print(points_xy)
        render_img = render.render(image=person_img, points=points_xy, zero_point=(0,0))
        cv2.imshow("img2", render_img)
        cv2.waitKey()

        pose = pose_recognitor.recognize(points_xy)
        action = action_recognitor.forward(pose)
        print(action)

        # hasFrame, frame = cap.read()
   



    del detector
    del estimator
