# Computer Vision
## Prerequisites
- Python3
- The packages in `requirements.txt`, can be installed via 
```bash 
 pip install -r requirements.txt
 ```
- Videos containing the chessboards, place those in `input/chessboard_videos` with names like `out1F.mp4`
- Videos of the volleyball court for extrinsic calibration, place those in `input/videos` with names like `out1.mp4`

## Usage
### Intrinsic Calibration
Note: For this, the videos mentioned above are necessary.
1. In `intrinsic_calibration.py` change line 171 `cameras = ['1', '2']` to the cameras you want to calibrate
2. Run the file 
```bash
./intrinsic_calibration.py
```
This will generate some files in the `results/` folder:
- `distortions.json`
- `intrinsic_refined.json`
- `intrinsic.json`

containing the distortion coefficients and the intrinsic matrices for the selected cameras.

Furthermore, from each input video, a single frame will be saved in `images/extrinsic_calibration_images/` which can be used to extract the pixel coordinates necessary for extrinsic calibration.

### Extrinsic Calibration
This will calibrate all cameras for which an intrinsic calibration exists.

1. Define world and image points or use the ones in `results/extrinsic_world_points.json` and `results/extrinsic_image_points.json`
2. Run the file
```bash
./extrinsic_calibration.py
```
This will generate the file `results/extrinsic.json` containing the extrinsic matrices of the cameras.

### Visualizing the Extrinsic Calibration
Run the file
```bash
./plot_camera_positions.py
```
which will
- generate a 2D and a 3D plot of the camera positions relative to the volleyball court
- visualize the ground truth camera positions from `results/ground_truth_cameras.json` in them
- Calculate the mean, median and standard deviation of the absolute error between the calibrated camera positions and the ground truth


### Homography Calibration
Run the file
```bash
./homography_calibration.py
```

This script reuses the files `results/extrinsic_image_points.json` and `results/extrinsic_world_points.json` to generate homography matrices between the cameras' image planes and the volleyball court. The results are stored in `results/homography.json` and are used for the homography tool.


### Homography Tool
This tool uses the homography matrices to visualize a clicked point in one camera's image in all other images and the real world.

Note: do not worry if startup takes a while, it is loading multiple images.

Run the file
```bash
./homography_tool.py
```
1. A grid of images from each camera and a top-view of the volleyball court will be shown
2. Left click on one of the images to select a camera
3. Press any key (e.g. `q`) to continue
4. The clicked image will be shown in fullscreen
5. Left click on any point in the image, the coordinates will be shown
6. Press any key (e.g. `q`) to continue
7. Again, the grid will be shown. This time, the clicked point will be shown in all images where it exists and in the top-view of the court
8. Press any key (e.g. `q`) to exit
