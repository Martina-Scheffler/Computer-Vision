#!/usr/bin/python3

import numpy as np
import matplotlib.pyplot as plt
import json

class PlotCameraPositions:
    def __init__(self):
        self.extrinsic_matrices = {}
        self.ground_truth_cameras = {}
        
        self.load_extrinsic_matrices()
        self.load_ground_truth()
        
        
    def load_extrinsic_matrices(self):
        with open('results/extrinsic.json') as f:
            self.extrinsic_matrices = json.load(f)
        
        # convert dictionary entries to numpy arrays
        for k in self.extrinsic_matrices.keys():
            self.extrinsic_matrices[k] = np.array(self.extrinsic_matrices[k])
            
    
    def load_ground_truth(self):
        with open('results/ground_truth_cameras.json') as f:
            self.ground_truth_cameras = json.load(f)
        
        # convert dictionary entries to numpy arrays
        for k in self.ground_truth_cameras.keys():
            self.ground_truth_cameras[k] = np.array(self.ground_truth_cameras[k])
            
            
    def twoD_plot(self):
        # plot the court
        plt.scatter([0, 0, 6, 6, 9, 9, 12, 12, 18, 18], [0, 9, 0, 9, 0, 9, 0, 9, 0, 9], color='blue')
        plt.plot([0, 0], [0, 9], 'blue')
        plt.plot([6, 6], [0, 9], 'blue')
        plt.plot([9, 9], [0, 9], 'blue')
        plt.plot([12, 12], [0, 9], 'blue')
        plt.plot([18, 18], [0, 9], 'blue')
        plt.plot([0, 18], [0, 0], 'blue')
        plt.plot([0, 18], [9, 9], 'blue')
        
        # plot cameras
        for camera in self.extrinsic_matrices.keys():
            plt.scatter(self.extrinsic_matrices[camera][0, 3], 
                        self.extrinsic_matrices[camera][1, 3], 
                        color='red', label=camera)
            
            plt.text(self.extrinsic_matrices[camera][0, 3], 
                     self.extrinsic_matrices[camera][1, 3],
                     camera)

        # plot ground truth
        for camera in self.ground_truth_cameras.keys():
            plt.scatter(self.ground_truth_cameras[camera][0], 
                        self.ground_truth_cameras[camera][1],
                        color='green', label=camera)


        # invert the y axis so origin is in top left corner
        plt.gca().invert_yaxis()
        
        # axis labels
        plt.xlabel('x [m]')
        plt.ylabel('y [m]', rotation=0)

        plt.axis('equal')
        
        plt.show()
        
    
    def threeD_plot(self):
        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')

        # plot the court
        ax.scatter([0, 0, 6, 6, 9, 9, 12, 12, 18, 18], [0, 9, 0, 9, 0, 9, 0, 9, 0, 9], 0, color='blue')
        ax.plot([0, 0], [0, 9], 0, 'blue')
        ax.plot([6, 6], [0, 9], 0, 'blue')
        ax.plot([9, 9], [0, 9], 0, 'blue')
        ax.plot([12, 12], [0, 9], 0, 'blue')
        ax.plot([18, 18], [0, 9], 0, 'blue')
        ax.plot([0, 18], [0, 0], 0, 'blue')
        ax.plot([0, 18], [9, 9], 0, 'blue')

        # plot the cameras
        for camera in self.extrinsic_matrices.keys():
            ax.scatter(self.extrinsic_matrices[camera][0, 3],
                       self.extrinsic_matrices[camera][1, 3],
                       self.extrinsic_matrices[camera][2, 3],
                       color='red', label=camera)
            
            ax.text(self.extrinsic_matrices[camera][0, 3],
                    self.extrinsic_matrices[camera][1, 3],
                    self.extrinsic_matrices[camera][2, 3],
                    camera)
        
        
        # plot ground truth
        for camera in self.ground_truth_cameras.keys():
            ax.scatter(self.ground_truth_cameras[camera][0],
                       self.ground_truth_cameras[camera][1], 
                       self.ground_truth_cameras[camera][2], 
                       color='green', label=camera)

        # invert the y axis so origin is in top left corner
        plt.gca().invert_zaxis()
        plt.gca().invert_yaxis()
        
        # axis labels
        ax.set_xlabel('x [m]')
        ax.set_ylabel('y [m]')
        ax.set_zlabel('z [m]')

        plt.show()
        
        
    def errors(self):
        # Calculate errors
        errors = []

        for camera in self.ground_truth_cameras.keys():
            errors.append(abs(self.ground_truth_cameras[camera] - self.extrinsic_matrices[camera][0:3, 3]))
    
        errors = np.array(errors)
        print(f'Mean Error [m]: {errors.mean(axis=0)}')
        print(f'Median Error [m]: {np.median(errors, axis=0)}')
        print(f'Std. Deviation [m]: {np.std(errors, axis=0)}')
        
        

if __name__ == '__main__':
    pt = PlotCameraPositions()
    pt.twoD_plot()
    pt.threeD_plot()
    pt.errors()
