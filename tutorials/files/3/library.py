import cv2
import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple, Dict
from pathlib import Path
from prettytable import PrettyTable
from improutils import *


def _plot_grid(xv, yv, squares, ax):
    for i  in np.linspace(0, xv.shape[1] - 1, squares+1, dtype=int):
        ax.plot(xv[i,:], yv[i,:], 'k-')
    for j in np.linspace(0, xv.shape[0] - 1, squares+1, dtype=int):
        ax.plot(xv[:,j], yv[:,j], 'k-')
    
    ax.axis('off')

def _radial_distortion(xv, yv, k):
    xv_radial = np.zeros_like(xv)
    yv_radial = np.zeros_like(yv)
    for i in range(xv.shape[0]):
        for j in range(xv.shape[1]):
            r = np.sqrt(xv[i,j]**2 + yv[i,j]**2)
            radial = (1 + (k[0]*(r**2) + k[1]*(r**4) + k[2]*(r**6)))/(1 + (k[3]*(r**2) + k[4]*(r**4) + k[5]*(r**6)))
            xv_radial[i,j] = xv[i,j]*radial
            yv_radial[i,j] = yv[i,j]*radial
    return xv_radial, yv_radial

def _tangetial_distortion(xv, yv, p):
    xv_tang = np.zeros_like(xv)
    yv_tang = np.zeros_like(yv)
    for i in range(xv.shape[0]):
        for j in range(xv.shape[1]):
            x = xv[i,j]
            y = yv[i,j]
            r = np.sqrt(x**2 + y**2)
            x_tang = x + (2*p[0]*x*y + p[1]*(r**2 + 2*x**2))
            y_tang = y + (p[0]*(r**2 + 2*y**2) + 2*p[1]*x*y)
            xv_tang[i,j] = x_tang
            yv_tang[i,j] = y_tang
    return xv_tang, yv_tang

def plot_distortion(k1:float,k2:float,k3:float,k4:float,k5:float,k6:float, p1:float,p2:float) -> None:
    """Plots radial, tangential and compounded (radial + tangential) distortion grid. Using the Brown-Conrady model.

    Args:
        k1 (float): radial distortion coefficient
        k2 (float): radial distortion coefficient
        k3 (float): radial distortion coefficient
        k4 (float): radial distortion coefficient
        k5 (float): radial distortion coefficient
        k6 (float): radial distortion coefficient
        p1 (float): tangential distortion coefficient
        p2 (float): tangential distortion coefficient
    """
    k = (k1,k2,k3,k4,k5,k6)
    p = (p1,p2)
    squares = 10 # amount of squares in the grid
    pts = 100
    # realistical values for image with 2500 x 2500 pixels with focal length of 35mm which is close to 10500 pixels with basler camera pixel size, origin is in the center - therfore x and y should be within values +-(2500/10500)/2
    width = 0.23
    height = 0.23
    xv, yv = np.meshgrid(np.linspace(-width/2,width/2,pts), np.linspace(-height/2,height/2,pts))

    xv_radial, yv_radial = _radial_distortion(xv, yv, k)
    xv_tang, yv_tang = _tangetial_distortion(xv, yv, p)

    _, axs = plt.subplots(1, 3, figsize=(15, 5))

    _plot_grid(xv_radial, yv_radial, squares, axs[0])
    axs[0].set_title('Radial distortion grid')

    _plot_grid(xv_tang, yv_tang, squares, axs[1])
    axs[1].set_title('Tangential distortion grid')

    _plot_grid(xv_radial + xv_tang, yv_radial + yv_tang, squares, axs[2])
    axs[2].set_title('Compounded distortion grid')
    plt.show()

def camera_calibration(calib_path: str, 
                       chess_shape: Tuple[int,int], 
                       cv2_flags:int = 0, 
                       extensions: List[str] = ["jpg", "jpeg" ,"png", "tiff", "bmp"]) -> Tuple[float, 
                                                                                        np.ndarray,
                                                                                        np.ndarray, 
                                                                                        Tuple[np.ndarray], 
                                                                                        Tuple[np.ndarray], 
                                                                                        np.ndarray, 
                                                                                        np.ndarray, 
                                                                                        np.ndarray, 
                                                                                        Dict[str,np.ndarray]]: 
    """Calibrates camera from images with chessboard pattern, using OpenCV's cv2.calibrateCameraExtended function

    Args:
        calib_path (str): path to the folder containing chessboard pattern images
        chess_shape (Tuple[int,int]): chessborad shape in the format (rows, columns) - count of inner corners
        cv2_flags (int, optional): additional OpenCV's flags for cv2.calibrateCameraExtended. Defaults to 0.
        extensions (List[str], optional): allowed image extensions. Defaults to ["jpg", "jpeg" ,"png", "tiff"].

    Returns:
        Tuple[float, np.ndarray, np.ndarray, Tuple[np.ndarray], Tuple[np.ndarray], np.ndarray, np.ndarray, np.ndarray, Dict[str,np.ndarray]]: 
        returns the output from cv2.calibrateCameraExtended and dictionary with image names as keys and images with drawn chessboard corners as values
    """
    def correct_extension(path, extensions):
        return path.is_file() and path.suffix[1:].lower() in extensions
    # termination criteria for subpixel corner detection
    # by default it is set to 30 iterations and epsilon = 0.001
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    
    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    objp = np.zeros((chess_shape[0] * chess_shape[1], 3), np.float32)
    objp[:, :2] = np.mgrid[0:chess_shape[0], 0:chess_shape[1]].T.reshape(-1, 2)

    # arrays to store object points and image points from all the images.
    objpoints = [] # 3D point in real world space
    imgpoints = [] # 2D points in image plane.

    image_paths = sorted([path for path in Path(calib_path).glob("*") if correct_extension(path,extensions)]) 
    chess_brd_images = 0
    read_images = 0
    chessboard_images = {}
    for img_path in image_paths:
        img_name = img_path.name
        
        img = cv2.imread(img_path)
        if img is None:
            print(f"File {img_name} could not be read, skipping...")
            continue
        else:
            read_images += 1

            print(f"File {img_name} is being processed...")

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # find the chess board corners
        ret, corners = cv2.findChessboardCorners(gray, chess_shape, None)

        # if found, add object points, image points (after refining them)
        if ret:
            chess_brd_images += 1
            print(f"\t Corners found!")
            objpoints.append(objp)
            subpix_corners = cv2.cornerSubPix(gray,corners, (11,11), (-1,-1), criteria)
            imgpoints.append(subpix_corners)

            chessboard_images[img_name] = cv2.drawChessboardCorners(img, chess_shape, subpix_corners, ret)

        else:
            print(f"\t Corners NOT found!")
            continue
    
    print(f"Number of images with detected chessboard: {chess_brd_images}/{read_images}")
    calib_values = cv2.calibrateCameraExtended(objpoints, imgpoints, gray.shape[::-1],cameraMatrix= None, distCoeffs=None, flags = cv2_flags, criteria=criteria)
    reprojection_error, camera_matrix, dist_coeffs, rvecs, tvecs, std_deviations_intrinsics, std_deviations_extrinsics, per_view_errors = calib_values
    return reprojection_error, camera_matrix, dist_coeffs, rvecs, tvecs, std_deviations_intrinsics, std_deviations_extrinsics, per_view_errors, chessboard_images
    
def calibration_stats(reprojection_error:float,
                      camera_matrix: np.ndarray, 
                      dist_coeffs:np.ndarray, 
                      std_deviations_intrinsics:np.ndarray=None,
                      per_view_errors:np.ndarray=None, 
                      view_names:List[str]=None, 
                      pixel_size:float=None) -> None:
    """Prints calibration statistics using. 
    RMS re-projection error, estimated intrinsics and distortion parameters, standard deviations of intrinsics, focal length in millimeters and per view reprojection errors.

    Args:
        reprojection_error (float): re-projection error from cv2.calibrateCamera
        camera_matrix (np.ndarray): camera matrix from cv2.calibrate
        dist_coeffs (np.ndarray): distortion coefficients from cv2.calibrateCamera
        std_deviations_intrinsics (np.ndarray, optional): std_deviations_intrinsics from cv2.calibrateCameraExtended. Defaults to None.
        per_view_errors (np.ndarray, optional): per_view_errors from cv2.calibrateCameraExtended. Defaults to None.
        view_names (List[str], optional): image names for which we detected the chessboard. Defaults to None.
        pixel_size (float, optional): actual size of pixels of a camera in micrometers eg. 4.8e-6. Defaults to None.
    """
    # opencv always returns atleast 4 distortion coefficients
    params_amount = 4 + dist_coeffs.shape[1]
    
    parameters = ["fx", "fy", "cx", "cy", "k1", "k2", "p1", "p2", "k3", "k4", "k5", "k6", "s1", "s2", "s3", "s4", "Tx", "Ty"]
    units = ["pixels"] * 4 + ["unitless"] * (params_amount - 4)
    
    print(f"RMS re-projection error: {reprojection_error:.5f} pixels")
    
    print(f"\nEstimated intrinsics parameters")
    intrinsics_table = PrettyTable()
    intrinsics_table.add_column("Parameter", parameters[:4])
    intrinsics_table.add_column("Estimated Value", [f"{val:.5f}" for val in [camera_matrix[0, 0], camera_matrix[1, 1], camera_matrix[0, 2], camera_matrix[1, 2]]])
    intrinsics_table.add_column("Unit", units[:4])
    print(intrinsics_table)
    
    print(f"\nEstimated Distortion parameters")
    distortion_table = PrettyTable()
    distortion_table.add_column("Parameter", parameters[4:params_amount])
    distortion_table.add_column("Distortion", [f"{val:.5f}" for val in dist_coeffs[0, :params_amount-4]])
    distortion_table.add_column("Unit", units[4:params_amount])
    print(distortion_table)
    
    if std_deviations_intrinsics is not None:
        print(f"\nIntrinsic parameters standard deviation")
        intrinsics_std_table = PrettyTable()
        intrinsics_std_table.add_column("Parameter", parameters[:params_amount])
        intrinsics_std_table.add_column("Value", [f"±{val:.5f}" for val in std_deviations_intrinsics[:params_amount,0]])
        intrinsics_std_table.add_column("Unit", units[:params_amount])
        print(intrinsics_std_table)
        
    if pixel_size is not None and std_deviations_intrinsics is not None:
        print(f"\nEstimated Focal length in millimeters")
        focal_length_table = PrettyTable()
        focal_length_table.add_column("Parameter", parameters[:2])
        focal_length_table.add_column("Value ± Std Deviation", [f"{val*1000*pixel_size:.5f} ± {std*1000*pixel_size:.5f}" for val, std in zip([camera_matrix[0, 0], camera_matrix[1, 1]], std_deviations_intrinsics[:2,0])])
        focal_length_table.add_column("Unit", ["millimeter"] * 2)
        print(focal_length_table)

    if per_view_errors is not None:
        print(f"\nPer view reprojection errors")
        view_error_table = PrettyTable()
        # Sort the view names and errors by the errors in descending order
        sorted_views_and_errors = sorted(zip(view_names, per_view_errors[:,0]), key=lambda x: x[1], reverse=True)
        sorted_view_names, sorted_errors = zip(*sorted_views_and_errors)
        view_error_table.add_column("Image name", sorted_view_names)
        view_error_table.add_column("Re-projection error (sorted)", [f"{val:.5f}" for val in sorted_errors])
        view_error_table.add_column("Unit", ["pixels"] * len(sorted_view_names))
        print(view_error_table)

def correct_frame(img, camera_matrix, dist_coeffs):
    """Returns undistorted image."""
    return cv2.undistort(img, camera_matrix, dist_coeffs)