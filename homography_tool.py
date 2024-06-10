#!/usr/bin/python3

import numpy as np
import cv2 
import matplotlib.pyplot as plt
import json


class HomographyTool:
    def __init__(self):
        self.original_scale = (3840, 2160)
        self.display_scale = (1920, 1080)
        self.scale_ratio = self.original_scale[0] / self.display_scale[0]
        
        self.grid = None
        self.image = None
        self.clicked_point_in_grid = None
        self.clicked_point_in_image = None
        self.world_point = None
        
    
    def import_images(self):
        self.img1 = cv2.imread(f'images/extrinsic_calibration_images/out1.png')
        self.img2 = cv2.imread(f'images/extrinsic_calibration_images/out2.png')
        self.img3 = cv2.imread(f'images/extrinsic_calibration_images/out3.png')
        self.img4 = cv2.imread(f'images/extrinsic_calibration_images/out4.png')
        self.img5 = cv2.imread(f'images/extrinsic_calibration_images/out5.png')
        self.img6 = cv2.imread(f'images/extrinsic_calibration_images/out6.png')
        self.img7 = cv2.imread(f'images/extrinsic_calibration_images/out7.png')
        self.img8 = cv2.imread(f'images/extrinsic_calibration_images/out8.png')
        self.img12 = cv2.imread(f'images/extrinsic_calibration_images/out12.png')
        self.img13 = cv2.imread(f'images/extrinsic_calibration_images/out13.png')
        
        
    def build_grid(self, court):
        # import court
        court_rs = cv2.resize(court, (int(self.original_scale[0]*2), int(self.original_scale[1]*2)))
        
        # generate black tile
        black = np.zeros_like(self.img1)
        
        # concatenate images 
        row_1 = np.concatenate((self.img1, self.img2, self.img3, self.img4), axis=1)
        row_2_left = np.concatenate((self.img5, self.img6), axis=1)
        row_3_left = np.concatenate((self.img7, self.img8), axis=1)
        
        left = np.concatenate((row_2_left, row_3_left), axis=0)
        
        rows_2_3 = np.concatenate((left, court_rs), axis=1)
        
        row4 = np.concatenate((self.img12, self.img13, black, black), axis=1)
        
        # build grid
        self.grid = np.concatenate((row_1, rows_2_3, row4), axis=0)
     
        
    def annotate_grid(self, image):
        x_step = int(self.display_scale[0] / 4)
        y_step = int(self.display_scale[1] / 4)
        
        font = cv2.FONT_HERSHEY_SIMPLEX 
        cv2.putText(image, '1', (10, 30), font, 1, (255, 255, 255), 2)
        cv2.putText(image, '2', (x_step + 10, 30), font, 1, (255, 255, 255), 2)
        cv2.putText(image, '3', (2 * x_step + 10, 30), font, 1, (255, 255, 255), 2)
        cv2.putText(image, '4', (3 * x_step +10, 30), font, 1, (255, 255, 255), 2)
        cv2.putText(image, '5', (10, y_step + 30), font, 1, (255, 255, 255), 2)
        cv2.putText(image, '6', (x_step + 10, y_step + 30), font, 1, (255, 255, 255), 2)
        cv2.putText(image, '7', (10, 2 * y_step + 30), font, 1, (255, 255, 255), 2)
        cv2.putText(image, '8', (x_step + 10, 2 * y_step + 30), font, 1, (255, 255, 255), 2)
        cv2.putText(image, '12', (10, 3 * y_step + 30), font, 1, (255, 255, 255), 2)
        cv2.putText(image, '13', (x_step + 10, 3 * y_step + 30), font, 1, (255, 255, 255), 2)
        
        cv2.putText(image, 'USAGE', (2 * x_step + 10, 3 * y_step + 30), font, 1, (255, 255, 255), 2)
        cv2.putText(image, '- Click on one of the images to select a camera', (2 * x_step + 10, 3 * y_step + 70), font, 1, (255, 255, 255), 2)
        cv2.putText(image, '- Press any key to continue', (2 * x_step + 10, 3 * y_step + 100), font, 1, (255, 255, 255), 2)
        cv2.putText(image, '- Click on a point in the image', (2 * x_step + 10, 3 * y_step + 130), font, 1, (255, 255, 255), 2)
        cv2.putText(image, '- Press any key to continue', (2 * x_step + 10, 3 * y_step + 160), font, 1, (255, 255, 255), 2)
        cv2.putText(image, '- The point will be shown in all images and on the court', (2 * x_step + 10, 3 * y_step + 190), font, 1, (255, 255, 255), 2)
        cv2.putText(image, '- Press any key to exit', (2 * x_step + 10, 3 * y_step + 220), font, 1, (255, 255, 255), 2)
    
        return image
        
        
    def display_grid(self):
        court = cv2.imread('images/court.png')
        
        self.build_grid(court)

        # display
        cv2.namedWindow('cluster', cv2.WINDOW_NORMAL)
        cv2.setWindowProperty('cluster', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        
        grid_rs = cv2.resize(self.grid, self.display_scale)
        grid_rs = self.annotate_grid(grid_rs)
        cv2.imshow('cluster', grid_rs) 
    

    def click_grid(self, event, x, y, flags, params): 
        # checking for left mouse clicks 
        if event == cv2.EVENT_LBUTTONDOWN: 
            # displaying the coordinates on the shell 
            self.clicked_point_in_grid = np.array([x, y])
            print(f'Clicked Point in Grid: {self.clicked_point_in_grid}')
        
        
    def select_camera(self):
        # size of one image in grid
        tile_width = self.display_scale[0] / 4
        tile_height = self.display_scale[1] / 4
        
        # position of clicked point
        x = self.clicked_point_in_grid[0]
        y = self.clicked_point_in_grid[1]
        
        # find out in which camera's tile the click was
        if x < tile_width:
            # 1, 5, 7, 12 - first column
            if y < tile_height:
                return '1'
            elif y < 2 * tile_height:
                return '5'
            elif y < 3 * tile_height:
                return '7'
            else:
                return '12'
        elif x < 2 * tile_width:
            # 2, 6, 8, 13 - second column
            if y < tile_height:
                return '2'
            elif y < 2 * tile_height:
                return '6'
            elif y < 3 * tile_height:
                return '8'
            else:
                return '13'
        elif x < 3 * tile_width:
            # 3 - third column
            if y < tile_height:
                return '3'
        else:
            # 4 - fourth column
            if y < tile_height:
                return '4'
        

    def display_enlarged_image(self, camera):
        # display the image of the selected camera in fullscreen
        cv2.namedWindow('image', cv2.WINDOW_NORMAL)
        cv2.setWindowProperty('image', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        self.image = cv2.imread(f'images/extrinsic_calibration_images/out{camera}.png')
        image_rs = cv2.resize(self.image, self.display_scale) 
        cv2.imshow('image', image_rs)
        
    
    def click_event(self, event, x, y, flags, params): 
        # checking for left mouse clicks 
        if event == cv2.EVENT_LBUTTONDOWN: 
            # get clicked point 
            self.clicked_point_in_image = np.array([int(self.scale_ratio * x), int(self.scale_ratio * y), 1])
            print(f'Clicked Point in Image: {self.clicked_point_in_image}') 
    
            # displaying the coordinates on the image window 
            font = cv2.FONT_HERSHEY_SIMPLEX 
            image_rs = cv2.resize(self.image, self.display_scale)
            cv2.circle(image_rs, (x, y), 3, (255, 0, 0), 4)
            cv2.putText(image_rs, f'{self.clicked_point_in_image[0]}, {self.clicked_point_in_image[1]}', (x,y), 
                        font, 1, (255, 0, 0), 2)
            cv2.imshow('image', image_rs) 
            
            
    def get_world_point(self, camera):
        # use homography matrix of selected point to transform from image to world coordinates
        homography_matrix = self.homographies[camera]
        world_point = np.dot(homography_matrix, self.clicked_point_in_image)
        self.world_point = world_point / world_point[2] / 1000
        print(f'World Point: {self.world_point}')
        
    
    def import_homographies(self):
        with open('results/homography.json') as f:
            self.homographies = json.load(f)
        
        # convert dictionary entries to numpy arrays
        for k in self.homographies.keys():
            self.homographies[k] = np.array(self.homographies[k])
        
        
    def calculate_image_positions(self):
        # get position in every image using the homography matrices
        markers = {}
        for camera in self.homographies.keys():
            image_point = np.dot(np.linalg.inv(self.homographies[camera]), self.world_point)
            image_point = (image_point / image_point[2])[:2]
            
            # check if the point is visible in the camera's image
            if 0 < image_point[0] < self.original_scale[0] and 0 < image_point[1] < self.original_scale[1]:
                markers[camera] = image_point / self.scale_ratio / 4  # because grid is 4x4 -> scale to one tile
                
        # distribute over grid
        scale_x = self.display_scale[0] / 4
        scale_y = self.display_scale[1] / 4
        
        for marker in markers.keys():
            if marker in ['1', '5', '7', '12']:  # first column
                if marker == '5':
                    markers[marker] += np.array([0, scale_y])
                elif marker == '7':
                    markers[marker] += np.array([0, 2 * scale_y])
                elif marker == '12':
                    markers[marker] += np.array([0, 3 * scale_y])
            elif marker in ['2', '6', '8', '13']:  # second column
                if marker == '2':
                    markers[marker] += np.array([scale_x, 0])
                elif marker == '6':
                    markers[marker] += np.array([scale_x, scale_y])
                elif marker == '8':
                    markers[marker] += np.array([scale_x, 2 * scale_y])
                elif marker == '13':
                    markers[marker] += np.array([scale_x, 3 * scale_y])
            elif marker == '3':  # third column
                markers[marker] += np.array([2 * scale_x, 0])
            elif marker == '4':  # fourth column
                markers[marker] += np.array([3 * scale_x, 0])
                
        return markers
    
    
    def plot_court(self):
        # plot the court
        plt.scatter([0, 0, 6, 6, 9, 9, 12, 12, 18, 18], [0, 9, 0, 9, 0, 9, 0, 9, 0, 9], color='blue')
        plt.plot([0, 0], [0, 9], 'blue')
        plt.plot([6, 6], [0, 9], 'blue')
        plt.plot([9, 9], [0, 9], 'blue')
        plt.plot([12, 12], [0, 9], 'blue')
        plt.plot([18, 18], [0, 9], 'blue')
        plt.plot([0, 18], [0, 0], 'blue')
        plt.plot([0, 18], [9, 9], 'blue')

        # set axis limits
        plt.xlim((-5, 23))
        plt.ylim((-5, 14))

        # invert the y axis so origin is in top left corner
        plt.gca().invert_yaxis()

        
    def plot_unmarked_court(self):
        self.plot_court()
        
        # save
        plt.savefig('images/court.png', dpi=600)
        
     
    def plot_world_point_on_court(self):
        self.plot_court()
        
        # plot the point
        plt.scatter(self.world_point[0], self.world_point[1], color='red')

        # save
        plt.savefig('images/marked_court.png', dpi=600)
        
    
    def display_marked_grid(self, markers):    
        # generate new grid using the court plot with the world position    
        marked_court = cv2.imread('images/marked_court.png')
        marked_court_rs = cv2.resize(marked_court, (int(self.original_scale[0]*2), int(self.original_scale[1]*2)))
        
        self.build_grid(marked_court_rs)
        
        # new window
        cv2.namedWindow('marked_cluster', cv2.WINDOW_NORMAL)
        cv2.setWindowProperty('marked_cluster', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        
        grid_rs = cv2.resize(self.grid, self.display_scale)
        
        grid_rs = self.annotate_grid(grid_rs)
        
        # create circles around positions in the camera tiles
        for point in markers.values(): 
            cv2.circle(grid_rs, point.astype(int), 10, (0, 0, 255), 3)
            
        cv2.imshow('marked_cluster', grid_rs) 
        
    
    def run(self):
        print('HOMOGRAPHY TOOL')
        print('Usage:')
        print('\t-A grid of images is displayed. Click on one of the images using the left mouse key, then press q.')
        print('\t-A single image is displayed. Click on a point, then press q.')
        print('\t-A grid of images is displayed. The clicked point from the single camera is visualized in all other cameras and on the court. Press q to exit.\n')
        
        # display grid and wait until a camera is picked
        self.import_images()
        self.plot_unmarked_court()
        self.display_grid()
        cv2.setMouseCallback('cluster', self.click_grid) 
        cv2.waitKey(0)
        
        camera = self.select_camera()
        print(f'Selected camera: {camera}')
        
        # display the camera's image in fullscreen and wait until a point is picked
        self.display_enlarged_image(camera)
        cv2.setMouseCallback('image', self.click_event) 
        cv2.waitKey(0)
        
        # calculate the world position and the image position in all other cameras
        self.import_homographies()
        self.get_world_point(camera)
        markers = self.calculate_image_positions()
        self.plot_world_point_on_court()
        
        # show the selected point in all cameras and on the court
        self.display_marked_grid(markers)
        cv2.waitKey(0)
        
        cv2.destroyAllWindows() 
        
    

if __name__ == '__main__':
     ht = HomographyTool()
     ht.run()
