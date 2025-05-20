import cv2
import math
import numpy as np
import time
file_path = '/home/fa/yolov5//3.jpg'
# 四个摄相头固定位置:camer1=(1570,1321)
import math

theta = 60


def calculate_new_point(x, y, theta_deg, d):
    # 将角度转换为弧度
    theta_rad = math.radians(theta_deg)

    # 计算新的坐标位置
    new_x = x + d * math.cos(theta_rad)
    new_y = y - d * math.sin(theta_rad)

    return new_x, new_y


def show_pattern(dis):
    x, y = 1570, 1321
    distance = dis * 70
    # for theta in range():
    new_x, new_y = calculate_new_point(x, y, theta, distance)
    new_x1, new_y1 = int(new_x), int(new_y)
    # print(f"新的坐标位置：({new_x1}, {new_y1})")
    img = cv2.imread(file_path)
    cv2.circle(img, (new_x1, new_y1), 40, (255, 255, 255), thickness=-1)
    new_img = cv2.resize(img, (720, 320))
    save_path = "/home/fa/yolov5/location_pattern/{}T{}.jpg".format(4, time.time())
    cv2.imwrite(save_path, new_img)
