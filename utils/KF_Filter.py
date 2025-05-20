from filterpy.kalman import KalmanFilter
import numpy as np
from shapely.geometry import box

class KalmanTracker:
    def __init__(self, dt=1.0, accel_noise_mag=0.1):
        self.kf = KalmanFilter(dim_x=8, dim_z=4)
        self.missed_frames = 0

        self.kf.F = np.array([
            [1, 0, 0, 0, dt, 0, 0, 0],
            [0, 1, 0, 0, 0, dt, 0, 0],
            [0, 0, 1, 0, 0, 0, dt, 0],
            [0, 0, 0, 1, 0, 0, 0, dt],
            [0, 0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 1]
        ])

        # Measurement function (4x8)
        self.kf.H = np.array([
            [1, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 0]
        ])

        self.kf.R = np.eye(4) * 5.0

        self.kf.Q = np.eye(8) * accel_noise_mag

        self.kf.x = np.zeros((8, 1))
        self.kf.P = np.eye(8) * 1000

    def predict(self):
        self.kf.predict()
        self.kf.predict()
        x, y, w, h = self.kf.x[:4].flatten()
        x1, y1 = x - w / 2, y - h / 2
        x2, y2 = x + w / 2, y + h / 2
        self.missed_frames += 1
        return [x1, x2, y1, y2]

    def update(self, bbox):
        self.missed_frames = 0
        x1, x2, y1, y2 = bbox[0],bbox[1],bbox[2],bbox[3],
        x = (x1 + x2) / 2
        y = (y1 + y2) / 2
        w = x2 - x1
        h = y2 - y1

        self.kf.update(np.array([x, y, w, h]))
    def is_active(self, max_missed=3):
        return self.missed_frames < max_missed
def compute_giou(box1, box2):

    x1_1, y1_1, x2_1, y2_1 = box1[:4]
    x1_2, y1_2, x2_2, y2_2 = box2[:4]

    rect1 = box(x1_1, y1_1, x2_1, y2_1)
    rect2 = box(x1_2, y1_2, x2_2, y2_2)

    intersection_area = rect1.intersection(rect2).area
    union_area = rect1.union(rect2).area
    iou = intersection_area / union_area if union_area > 0 else 0

    enclosing_box = rect1.union(rect2).bounds
    enclosing_area = (enclosing_box[2] - enclosing_box[0]) * (enclosing_box[3] - enclosing_box[1])

    giou = iou - ((enclosing_area - union_area) / enclosing_area if enclosing_area > 0 else 0)

    return giou
