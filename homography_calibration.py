#!/usr/bin/python3

import numpy as np
import cv2
import json


class HomographyCalibration:
    def __init__(self):
        # points used for calibration
        self.image_points = {}
        self.world_points = {}
        
        self.homographies = {}
        
        # load image and world points
        self.load_image_points()
        self.load_world_points()
        
    
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
            
    
    def calculate_homography_matrices(self):
        for camera in self.image_points.keys():
            homography, _ = cv2.findHomography(self.image_points[camera], self.world_points[camera])
            self.homographies[camera] = homography.tolist()
            
    
    def save_matrices(self):
        with open('results/homography.json', 'w') as outfile: 
            json.dump(self.homographies, outfile)
    
    
    def run(self):
        print("Start homography calibration...")
        self.calculate_homography_matrices()
        self.save_matrices()
        print("...Done.")



if __name__ == '__main__':
    hc = HomographyCalibration()
    hc.run()
