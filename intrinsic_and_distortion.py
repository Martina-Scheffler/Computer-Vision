#!/usr/bin/python3

import numpy as np
import cv2
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

def cut_video(camera):
    # skip 35s and use only 10s
    ffmpeg_extract_subclip(f'./chessboard_videos/out{camera}F.mp4', 35, 45, 
                           targetname=f'./chessboard_videos/out{camera}F_cut.mp4')
    

def export_frames_from_video(camera):
    # import video - use 5s cut clip
    cap = cv2.VideoCapture(f'./chessboard_videos/out{camera}F_cut.mp4')
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # save frames to arrays, both in color and grayscale
    frames = []
    gray_frames = []
    
    for i in range(0, frame_count):
        print(i)
        ret, frame = cap.read()
        
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        
        # convert frame to grayscale
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # save frames
        frames.append(frame)
        gray_frames.append(gray_frame)

    cap.release()
    cv2.destroyAllWindows()
    
    return frames, gray_frames



def find_calibration_points(gray_frames):
    # go through the frames and try to detect a checkerboard in them
    corners_detected = {}  # frame_id, corners
    
    # termination criteria
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)  # todo: choose better params

    chessboard_width = 5
    chessboard_height = 7

    # prepare object points
    object_points = np.zeros((chessboard_width * chessboard_height, 3), np.float32)
    object_points[:,:2] = np.mgrid[0:chessboard_height, 0:chessboard_width].T.reshape(-1,2)
    
    # arrays to store object points and image points from all the images.
    obj_points = [] # 3D point in real world space
    img_points = [] # 2D points in image plane.

    i = 0
    while i < len(gray_frames):
        # find the chess board corners
        ret, corners = cv2.findChessboardCorners(gray_frames[i], (chessboard_height, chessboard_width), None)
        
        if ret:
            # if found, add object points, image points (after refining them)
            obj_points.append(object_points)
            
            corners_refined = cv2.cornerSubPix(gray_frames[i], corners, (11,11), (-1,-1), criteria)  # todo: choose better params
            corners_detected[i] = corners_refined
            
            img_points.append(corners_refined)
            
            i += 1
        else:
            i += 5  # skip the next five frames to save some time
        if len(corners_detected) >= 10:
            break
        
    if len(corners_detected) < 10:
        raise RuntimeError('Not enough chessboard detections, calibration not possible.')
    
    return obj_points, img_points


 
def calibrate(object_points, image_points, image_size):
    # calibrate camera
    _, mtx, dist, _, _ = cv2.calibrateCamera(object_points, image_points, image_size, None, None)
    print(f'Camera Matrix: {mtx}')
    print(f'Distortion: {dist}')
    return mtx, dist

   
def save_intrinsic_matrix_and_distortion(intrinsic_matrix, distortions, camera):
    np.save(f'intrinsic_matrices/{camera}', intrinsic_matrix)
    np.save(f'distortions/{camera}', distortions)

 
def calibrate_cameras(cameras):
    for camera in cameras:
        print(f'Calibrating camera #{camera}...')
        # cut_video(camera)
        _, gray_frames = export_frames_from_video(camera)
        object_points, image_points = find_calibration_points(gray_frames)
        intrinsic_matrix, distortions = calibrate(object_points, image_points, gray_frames[0].shape[::-1])
        save_intrinsic_matrix_and_distortion(intrinsic_matrix, distortions, camera)
        print(f'...Done.')


if __name__ == '__main__':
    cameras = [1, 2, 3, 4, 5, 6, 7, 8, 12, 13]
    calibrate_cameras(cameras)
