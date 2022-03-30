import cv2 as cv
import numpy as np
from improutils import to_3_channels

def polar_warp(img, full_radius=True, inverse=False):
    center = (img.shape[0] / 2.0, img.shape[1] / 2.0)

    if full_radius:
        radius = np.sqrt(((img.shape[0] / 2.0) ** 2.0) + ((img.shape[1] / 2.0) ** 2.0))
    else:
        radius = center[0]

    method = cv.WARP_FILL_OUTLIERS
    size = None
    if inverse:
        method += cv.WARP_INVERSE_MAP
        size = img.shape[:2]
    dest = cv.warpPolar(img, size, center, radius, method)
    return dest

def warp_to_cartesian(img):
    return polar_warp(img, True)

def warp_to_polar(img):
    return polar_warp(img, True, True)

def draw_lines(img, lines):
    img_lines = to_3_channels(img)

    for line in lines:
        l = line[0]        
        cv.line(img_lines, (l[0], l[1]), (l[2], l[3]), (0,0,255), 2, cv.LINE_AA)
    
    return img_lines