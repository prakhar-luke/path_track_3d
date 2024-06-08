import numpy as np
import pandas as pd
import cv2
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

Camera_matrix =  [
[632.49137451 , 0.0          , 269.67868864],
[0.0          , 772.08073975 , 226.88820028],
[0.0          , 0.0          , 1.0        ],
 ]

Distortion_coeff =  [[ 4.44754911e+00, -3.87265190e+01,  1.30128997e-01, -2.94102986e-01,
   1.96878836e+02]]


fx = Camera_matrix[0][0]  
fy = Camera_matrix[1][1]  
cx = Camera_matrix[0][2]  
cy = Camera_matrix[1][2]  

camera_matrix = np.array(Camera_matrix)

dist_coeffs = np.array(Distortion_coeff)

# Known diameter of the ball (in meters)
known_diameter = 0.0726

# Load the CSV file
csv_file = "../data_points/xyr_cords.csv"# replace with path to your CSV file
data = pd.read_csv(csv_file)


def estimate_3d_position(pixel_coords, radius):
    undistorted_coords = cv2.undistortPoints(np.array([pixel_coords], dtype = np.float32), camera_matrix, dist_coeffs,
                                             P = camera_matrix)
    normalized_coords = np.array([[(undistorted_coords[0][0][0] - cx) / fx,
                                   (undistorted_coords[0][0][1] - cy) / fy]], dtype = np.float32)

    # Estimate depth (Z) using the known diameter of the ball
    # Z = (focal_length * real_diameter) / apparent_diameter
    Z = (fx * known_diameter) / (2 * radius)

    # Compute the real-world coordinates
    X = normalized_coords[0][0] * Z
    Y = normalized_coords[0][1] * Z

    return np.array([X, Y, Z], dtype = np.float32)


# List to store the 3D path
path_3d = []
frames = []
for index, row in data.iterrows():
    frame_number = row['sno']
    pixel_coords = (row['x'], row['y'])
    radius = row['r']

    position_3d = estimate_3d_position(pixel_coords, radius)
    path_3d.append(position_3d)
    frames.append(frame_number)

# Convert the 3D path to a numpy array for further processing
path_3d = np.array(path_3d)

# Plot the 3D path
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plot the points and connect them with lines
ax.plot(path_3d[:, 0], path_3d[:, 1], path_3d[:, 2], marker='o')

# Remove followin if you dont want to display frame number
# Label each point with the corresponding frame number
for i, frame in enumerate(frames):
    ax.text(path_3d[i, 0], path_3d[i, 1], path_3d[i, 2], str(frame), color='red')

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('3D Path of the Ball')

plt.show()
