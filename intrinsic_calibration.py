#!/usr/bin/python3

import cv2
import numpy as np
import json


class IntrinsicCalibration:
    def __init__(self, cameras):
        self.cameras = cameras
        
        self.intrinsic_matrices = {}
        self.intrinsic_matrices_refined = {}
        self.distortions = {}
        
        
    def get_frames(self, camera):
        # import video 
        cap = cv2.VideoCapture(f'input/chessboard_videos/out{camera}F.mp4')

        # get number of frames
        amount_of_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        start_frame = 1000

        # Set the frame skip interval
        frame_skip = 15

        # save frames to array 
        frames = []
        gray_frames = []
        cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
        
        for i in range(start_frame, amount_of_frames):  
            ret, frame = cap.read()
            if i % frame_skip == 0:        
                if not ret:
                    print("Can't receive frame (stream end?). Exiting ...")
                    break
                
                # convert frame to grayscale
                gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                
                frames.append(frame)
                gray_frames.append(gray_frame)

        cap.release()
        cv2.destroyAllWindows() # destroy all opened windows
        
        return frames, gray_frames
        
        
    def detect_chessboards(self, camera, gray_frames):
        # go through the frames and try to detect a checkerboard in them
        corners_detected = {}  # frame_id, corners
        
        # termination criteria
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)  # todo: choose better params

        if camera in ['5', '6', '8']:
            chessboard_width = 6
            chessboard_height = 9
        else:
            chessboard_width = 5
            chessboard_height = 7

        # prepare object points
        object_points = np.zeros((chessboard_width * chessboard_height, 3), np.float32)
        object_points[:,:2] = np.mgrid[0:chessboard_height, 0:chessboard_width].T.reshape(-1,2) 

 
        # Arrays to store object points and image points from all the images.
        obj_points = [] # 3d point in real world space
        img_points = [] # 2d points in image plane.

        i = 0
        while i < len(gray_frames):
            # Find the chess board corners
            ret, corners = cv2.findChessboardCorners(gray_frames[i], (chessboard_height, chessboard_width), None)
            
            if ret:
                # If found, add object points, image points (after refining them)
                obj_points.append(object_points)
                
                corners_refined = cv2.cornerSubPix(gray_frames[i], corners, (11,11), (-1,-1), criteria)  # todo: choose better params
                corners_detected[i] = corners_refined
                
                img_points.append(corners)
                
                i += 5
            else:
                i += 5  # skip the next five frames

        print(f'Number of frames where corners were detected: {len(corners_detected)}')   
        
        return obj_points , img_points
        
        
    def calibrate_camera(self, obj_points, img_points, frame_shape, img_shape):
        # calibrate camera
        ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(obj_points, img_points, frame_shape, None, None)
        print(f'Camera Matrix: {mtx}')
        print(f'Distortion: {dist}')
        
        
        # refine camera matrix
        h, w = img_shape
        newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h))
        print(f'Refined camera matrix: {newcameramtx}')
        
        return mtx, dist, newcameramtx


    def save_matrices(self):
        with open('results/intrinsic.json', 'w') as outfile: 
            json.dump(self.intrinsic_matrices, outfile)
        
        with open('results/distortions.json', 'w') as outfile: 
            json.dump(self.distortions, outfile)
        
        with open('results/intrinsic_refined.json', 'w') as outfile: 
            json.dump(self.intrinsic_matrices_refined, outfile)
    
    
    def calibrate(self):
        for camera in self.cameras:
            print(f'Calibrating camera {camera}...')
            frames, gray_frames = self.get_frames(camera)
            object_points, image_points = self.detect_chessboards(camera, gray_frames)
            
            intrinsic_matrix, distortion, intrinsic_refined = self.calibrate_camera(object_points, 
                                                                                    image_points, 
                                                                                    gray_frames[0].shape[::-1], 
                                                                                    frames[0].shape[:2])

            self.intrinsic_matrices[camera] = intrinsic_matrix.tolist()
            self.distortions[camera] = distortion.tolist()
            self.intrinsic_matrices_refined[camera] = intrinsic_refined.tolist()
            print('...Done.')
    
        self.save_matrices()
    
    
    def extract_extrinsic_calibration_images(self):
        import moviepy.editor as mpy
        
        # specify times
        times = {
            '1': '00:00:56',
            '2': '00:01:49',
            '3': '00:04:02',
            '4': '00:05:08',
            '5': '00:04:13',
            '6': '00:04:06',
            '7': '00:02:25',
            '8': '00:04:41',
            '12': '00:04:24',
            '13': '00:04:23'
        }
        
        
        # cut out single frame for extrinsic calibration
        for camera in self.cameras:
            maskclip = mpy.VideoFileClip(f'input/videos/out{camera}.mp4')
            maskclip.save_frame(f'images/extrinsic_calibration_images/out{camera}.png', t=times[camera])
            
            

if __name__ == '__main__':
    print("Please remember to place the videos in the input/ folders. Thank you!")
    cameras = ['1', '2']
    ic = IntrinsicCalibration(cameras=cameras)
    ic.extract_extrinsic_calibration_images()
    ic.calibrate()
