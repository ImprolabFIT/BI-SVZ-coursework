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

def rotate(img, angle):
    height, width = img.shape[:2]
    image_center = (width / 2, height / 2)

    rotation_mat = cv.getRotationMatrix2D(image_center, angle, 1.)

    abs_cos = abs(rotation_mat[0, 0])
    abs_sin = abs(rotation_mat[0, 1])

    bound_w = int(height * abs_sin + width * abs_cos)
    bound_h = int(height * abs_cos + width * abs_sin)

    rotation_mat[0, 2] += bound_w / 2 - image_center[0]
    rotation_mat[1, 2] += bound_h / 2 - image_center[1]

    dest = cv.warpAffine(img, rotation_mat, (bound_w, bound_h))
    return dest