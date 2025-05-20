import numpy as np
from scipy.optimize import linear_sum_assignment
import numpy as np

def compute_iou(box1, box2):

    print(f"box1::{box1}")
    print(f"box2::{box2}")

    x_left = max(box1[0], box2[0])
    y_top = max(box1[1], box2[1])
    x_right = min(box1[2], box2[2])
    y_bottom = min(box1[3], box2[3])

    intersection = max(0, x_right - x_left) * max(0, y_bottom - y_top)

    box1_area = (box1[2] - box1[0]) * (box1[3] - box1[1])
    box2_area = (box2[2] - box2[0]) * (box2[3] - box2[1])

    union = box1_area + box2_area - intersection

    iou = intersection / union if union > 0 else 0

    return iou

def match_detections_to_trackers(detections, trackers):
    """
    :param detections: list of (x1, y1, x2, y2)
    :param trackers: list of (x1', y1', x2', y2') from KalmanFilter.predict()
    :return: matched_indices [(det_idx, tracker_idx)], unmatched_dets, unmatched_trks
    """
    if len(trackers) == 0:
        return [], list(range(len(detections))), []

    iou_matrix = np.zeros((len(detections), len(trackers)), dtype=np.float32)
    print(f"detections::{detections}")
    print(f"trackers::{trackers}")

    for d, det in enumerate(detections):
        for t, trk in enumerate(trackers):
            print(f"Current frame{d}::{det}")
            print(f"past frame{t}::{trk}")
            iou_matrix[d, t] = compute_iou(det, trk)
            print(f"iou_matrix::{iou_matrix}")#

    row_idx, col_idx = linear_sum_assignment(-iou_matrix)

    matched_indices = []
    unmatched_dets = list(range(len(detections)))
    unmatched_trks = list(range(len(trackers)))

    for r, c in zip(row_idx, col_idx):
        if iou_matrix[r, c] > 0.6:
            matched_indices.append((r, c))
            unmatched_dets.remove(r)
            unmatched_trks.remove(c)

    return matched_indices, unmatched_dets, unmatched_trks
