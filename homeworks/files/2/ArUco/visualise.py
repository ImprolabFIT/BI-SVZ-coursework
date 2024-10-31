import cv2
from ArUco.constants import Color
import numpy as np

def draw_corners(bgr_img: np.ndarray, corners: np.ndarray, color: Color, thickness: int) -> np.ndarray:
    """Draw corners on an image.

    Parameters
    ----------
    bgr_img : np.ndarray
        Image in BGR format.
    corners : np.ndarray
        Corners to draw.
    color : Color
        Color of drawn edges.
    thickness : int
        Thickness of drawn edges.
    Returns
    -------
    np.ndarray
        Image with drawn corners.
    """
    for corner in corners:
        corner = corner.astype(int)
        cv2.polylines(bgr_img, [corner], isClosed=True,
                      color=color, thickness=thickness)
    return bgr_img


def draw_aruco(bgr_img: np.ndarray, corners: np.ndarray, ids: np.ndarray, rejected: np.ndarray, thickness: int = 5, corners_col: Color = Color.GREEN, rejected_col: Color = Color.RED, fontScale: int = 1) -> np.ndarray:
    """Draw ArUco markers on an image. Draws corners of correctly detected markers and rejected markers. Also draws ID of correctly detected markers.

    Parameters
    ----------
    bgr_img : np.ndarray
        Image in BGR format.
    corners : np.ndarray
        Corners of correctly detected ArUco markers.
    ids : np.ndarray
        ID of correctly detected ArUco markers.
    rejected : np.ndarray
        Corners of rejected ArUco markers. (Usually mistankenly detected)
    thickness : int, optional
        thickness of drawn marker edge, by default 5
    corners_col : Color, optional
        color of accepted markers (in BGR), by default Color.GREEN
    rejected_col : Color, optional
        color of rejected markers (in BGR), by default Color.RED
    fontScale : int, optional
        Size of, by default 1

    Returns
    -------
    np.ndarray
        Image with drawn ArUco markers.
    """
    if ids is not None:
        draw_corners(bgr_img, corners, color=corners_col, thickness=thickness)
        for i, corner in enumerate(corners):
            center = corner.squeeze().mean(axis=0).astype(int).squeeze()
            txt = str(ids[i][0])
            cv2.putText(bgr_img,
                        txt,
                        tuple(center),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        fontScale,
                        Color.BLUE,
                        2)
    if rejected is not None:
        draw_corners(bgr_img, rejected, color=rejected_col,
                     thickness=max(1, thickness//2))

    return bgr_img
