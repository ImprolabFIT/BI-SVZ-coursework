import cv2
import numpy as np
from ArUco.constants import ARUCO_DICT
from collections import namedtuple

import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')


ArucoInference = namedtuple('ArucoInference', [
    'detection', 'marker_name', 'marker_type', 'marker_count', 'detector', 'corners', 'ids', 'rejected'])


def create_detector(aruco_type: int) -> cv2.aruco.ArucoDetector:
    """Helper for creating an ArUco detector with default parameters.

    Parameters
    ----------
    aruco_type : int
        type of ArUco marker

    Returns
    -------
    cv2.aruco.ArucoDetector
        ArUco detector class
    """
    dictionary = cv2.aruco.getPredefinedDictionary(aruco_type)
    parameters = cv2.aruco.DetectorParameters()
    detector = cv2.aruco.ArucoDetector(dictionary, parameters)
    return detector


def infer_aruco_type(gray_img: np.ndarray) -> ArucoInference:
    """Infers the best ArUco type by trying out all types

    Parameters
    ----------
    gray_img : np.ndarray
        grayscale image

    Returns
    -------
    ArucoInference
        detection, marker_{name, type, count}, detector, corners, ids, rejected

    Note
    ----
    Preferably only call once, then use the returned detector for further detections.
    """
    assert gray_img.ndim == 2, "Input image must be grayscale"
    marker_counts = []

    for ar_name, ar_type in ARUCO_DICT.items():
        detector = create_detector(ar_type)
        corners, ids, rejected = detector.detectMarkers(gray_img)
        res = ArucoInference(detection=(corners, ids, rejected),
                             marker_name=ar_name,
                             marker_type=ar_type,
                             marker_count=0 if ids is None else len(ids),
                             detector=detector,
                             corners=corners,
                             ids=ids,
                             rejected=rejected)
        marker_counts.append(res)

    best_aruco_type = max(marker_counts, key=lambda x: x.marker_count)

    if best_aruco_type.marker_count == 0:
        logging.warning("No ArUco markers detected")
    else:
        logging.info(f"Detected {best_aruco_type.marker_count} markers of type '{best_aruco_type.marker_name}'.")

    return best_aruco_type
