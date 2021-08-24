import cv2
import numpy as np
from snr.prelude import *

from .boxes import Rect

# Minimim area threshold that is boxed
AREA_THRESHHOLD = 1000

LINE_THICKNESS = 6

green = (0, 255, 0)
color = green
# Function that takes in a image and draws boxes around suspicious plants


def box_image(image: np.array) -> List[Rect]:
    """Sample CV method courtesy of the BIG_J
    """
    # Converting image from BGR to HSV color space
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Generating the mask that outlines the plants
    # Method 1: Look for the color green
    mask1 = cv2.inRange(hsv, (30, 30, 30), (70, 255, 255))
    # Method 2

    # Take the mask and clean up the holes in the mask
    # Open removes area of the holes in the mask (removes noise) and
    # then adds area to the holes
    mask1 = cv2.morphologyEx(mask1,
                             cv2.MORPH_OPEN,
                             np.ones((3, 3), np.uint8))
    # Dilate areas in the mask (Add area to the holes in the mask)
    mask1 = cv2.morphologyEx(
        mask1, cv2.MORPH_DILATE, np.ones((3, 3), np.uint8))

    ret, thresh = cv2.threshold(mask1, 127, 255, 0)
    contours, hierarchy = cv2.findContours(thresh,
                                           cv2.RETR_TREE,
                                           cv2.CHAIN_APPROX_SIMPLE)

    boxes: List[Tuple[int, int, int, int]] = []  # List of Rectangle objects
    # Loop through each of the "Plant" areas
    for c in contours:
        # If the "Plant" is large enough draw a rectangle around it
        if cv2.contourArea(c) > AREA_THRESHHOLD:
            # Get the bounding rect
            (x, y, w, h) = cv2.boundingRect(c)
            boxes.append((x, y, w, h))

    return boxes
