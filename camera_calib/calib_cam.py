import cv2
import numpy as np

# Define the dimensions of the chessboard
chessboard_size = (5, 5)

# Define the size of a square in your desired units (e.g., meters)
# TODO : change it accoring to your measurements. 
square_size = 0.009  # 9mm

# Termination criteria for corner sub-pixel accuracy
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# Prepare object points
objp = np.zeros((np.prod(chessboard_size), 3), np.float32)
objp[:, :2] = np.indices(chessboard_size).T.reshape(-1, 2)
objp *= square_size

# Arrays to store object points and image points from all the images
objpoints = []  # 3d points in real world space
imgpoints = []  # 2d points in image plane

# Initialize video capture here I'm using droid cam to utilize phone camera
# TODO : change this to your device ID
vid_dev = 0 #"http://10.10.1.232:4747/video"
cap = cv2.VideoCapture(vid_dev)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Find the chessboard corners
    ret, corners = cv2.findChessboardCorners(gray, chessboard_size, None)
    
    if ret:
        # Refine the corner positions
        corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        
        # Store the object points and image points
        objpoints.append(objp)
        imgpoints.append(corners2)
        
        # Draw and display the corners
        frame = cv2.drawChessboardCorners(frame, chessboard_size, corners2, ret)
    
    # Display the frame
    cv2.imshow('Camera Calibration', frame)
    
    # Exit loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
    # Perform calibration if enough samples are collected
    if len(objpoints) >= 20:  # Use 20 images for calibration
        break

cap.release()
cv2.destroyAllWindows()

# Perform camera calibration
ret, camera_matrix, dist_coeffs, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

# Print the camera matrix and distortion coefficients
print("Camera matrix:\n", camera_matrix)
print("Distortion coefficients:\n", dist_coeffs)