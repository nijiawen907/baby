import os.path
import uuid

import cv2
from ultralytics import YOLO

import globals
from config import threshold, save_dir
from sql import insert_scene, close_connection, get_db_connection


class Predictor:
    def __init__(self):
        self.expression_model = YOLO("../model/expression.pt")
        self.pose_model = YOLO("../model/pose.pt")
        self.expression_labels: dict = self.expression_model.names
        self.pose_labels: dict = self.pose_model.names

    def predict(self, image):
        """
        单张图片的检测
        :param image:
        :return:
        """
        expression_results = self.expression_model(image, conf=threshold, verbose=False)
        pose_results = self.pose_model(image, conf=threshold, verbose=False)
        return expression_results[0], pose_results[0]

    def predict_video(self):
        """
        本地涉摄像头的检测
        :return:
        """
        # 打开摄像头
        cap = cv2.VideoCapture(0)
        frame_id = 0
        while True:
            ret, frame = cap.read()
            if not ret or frame_id % 30 != 0:
                frame_id += 1
                continue

            # 使用 YOLO 进行推理
            expression_result, pose_result = self.predict(frame)
            # 检测结果分析。
            expression_boxes = expression_result.boxes
            pose_boxes = pose_result.boxes

            # 检测表情
            if any(item in [0, 3, 6] for item in expression_boxes.cls):
                # 设置状态为 True
                globals.set_expression_status(True)
                # 可视化结果
                file_name = str(uuid.uuid4()).replace('-', '') + '.jpg'
                # save_path = os.path.join(save_dir, file_name)
                save_path = save_dir + "/" + file_name
                expression_result.save(save_path)  # 获取带有检测框的图像
                save_data(save_path, self.expression_labels.get(int(expression_boxes.cls[0].cpu().item())))
                print(f"更改状态为{globals.get_expression_status()}")
            # 检测到高兴
            elif 4 in expression_boxes.cls:
                # 设置状态为 False
                globals.set_expression_status(False)
                # 可视化结果
                file_name = str(uuid.uuid4()).replace('-', '') + '.jpg'
                # save_path = os.path.join(save_dir, file_name)
                save_path = save_dir + "/" + file_name
                expression_result.save(save_path)  # 获取带有检测框的图像
                save_data(save_path, self.expression_labels.get(int(expression_boxes.cls[0].cpu().item())))
                # print(f"更改状态为{globals.get_expression_status()}")

            else:
                # 设置状态为 False
                globals.set_expression_status(False)
                # save_data("000", "000")

            # 检测姿势
            if any(item in [1, 2, 3] for item in pose_boxes.cls):
                # 设置状态为 True
                globals.set_pose_status(True)
                # 可视化结果
                file_name = str(uuid.uuid4()).replace('-', '') + '.jpg'
                # save_path = os.path.join(save_dir, file_name)
                save_path = save_dir + "/" + file_name
                pose_result.save(save_path)  # 获取带有检测框的图像
                save_data(save_path, self.expression_labels.get(int(pose_boxes.cls[0].cpu().item())))
            else:
                # 设置状态为 False
                globals.set_pose_status(False)
                # save_data("000", "000")

            frame_id += 1


def save_data(image_path, statu):
    try:
        get_db_connection()
        insert_scene(image_path, statu)
    finally:
        close_connection()


if __name__ == '__main__':
    predictor = Predictor()
    predictor.predict_video()
