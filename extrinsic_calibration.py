#!/usr/bin/python3

import numpy as np 
import cv2
import json


class ExtrinsicCalibration():
    def __init__(self):
        # matrices
        self.intrinsic_matrices = {}
        self.distortions = {}
        
        # calibration points
        self.image_points = {}
        self.world_points = {}
        
        # result
        self.extrinsic_matrices = {}
        
        # load necessary data
        self.load_intrinsic_matrices()
        self.load_distortions()
        self.load_image_points()
        self.load_world_points()
        
    
    def load_intrinsic_matrices(self):
        with open('results/intrinsic.json') as f:
            self.intrinsic_matrices = json.load(f)
        
        # convert dictionary entries to numpy arrays
        for k in self.intrinsic_matrices.keys():
            self.intrinsic_matrices[k] = np.array(self.intrinsic_matrices[k])
        
        
    def load_distortions(self):
        with open('results/distortions.json') as f:
            self.distortions = json.load(f)
        
        # convert dictionary entries to numpy arrays
        for k in self.distortions.keys():
            self.distortions[k] = np.array(self.distortions[k])
            
    
    def load_image_points(self):
        with open('results/extrinsic_image_points.json') as f:
            self.image_points = json.load(f)
        
        # convert dictionary entries to numpy arrays
        for k in self.image_points.keys():
            self.image_points[k] = np.array(self.image_points[k])
            
    
    def load_world_points(self):
        with open('results/extrinsic_world_points.json') as f:
            self.world_points = json.load(f)
        
        # convert dictionary entries to numpy arrays
        for k in self.world_points.keys():
            self.world_points[k] = np.array(self.world_points[k]) 
            
            
    def calculate_extrinsic_matrices(self):
        for camera in self.intrinsic_matrices.keys():
            # calibrate extrinsic matrix
            _, rvecs, tvecs = cv2.solvePnP(self.world_points[camera],
                                           self.image_points[camera],
                                           self.intrinsic_matrices[camera],
                                           self.distortions[camera])

            # make rotation matrix from vector
            rotation_matrix, _ = cv2.Rodrigues(rvecs)

            # convert from 3x3 to 4x4
            rotation_matrix = np.pad(rotation_matrix, (0, 1), mode='constant')
            rotation_matrix[3, 3] = 1

            # convert to meters
            tvecs = tvecs.flatten() / 1000.

            # build translation matrix
            t_matrix = np.array([[1, 0, 0, tvecs[0]],
                                [0, 1, 0, tvecs[1]],
                                [0, 0, 1, tvecs[2]],
                                [0, 0, 0, 1]])

            # combine rotation and translation
            world_f_camera = np.dot(t_matrix, rotation_matrix)
            
            # invert
            extrinsic_matrix = np.linalg.inv(world_f_camera)
            
            # save to dictionary
            self.extrinsic_matrices[camera] = extrinsic_matrix.tolist()
        
    
    def save_matrices(self):
        with open('results/extrinsic.json', 'w') as outfile: 
            json.dump(self.extrinsic_matrices, outfile)
            
            
    def run(self):
        self.calculate_extrinsic_matrices()
        self.save_matrices()
            
            
            
if __name__ == '__main__':
    ec = ExtrinsicCalibration()
    ec.run()     
