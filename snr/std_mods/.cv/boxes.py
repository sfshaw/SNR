import cv2
import numpy as np
from snr.type_defs import *

Rect = Tuple[int, int, int, int]


def apply_boxes(frame: np.array,
                rects: List[Rect],
                color,
                thickness: int,
                ) -> np.array:
    for r in rects:
        x, y, w, h = r
        # Draw a green rectangle to visualize the bounding rect
        cv2.rectangle(frame,
                      (x, y), (x + w, y + h),
                      color,
                      thickness)

    return frame
