from typing import List, Tuple

import numpy as np
import cv2

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
