import cv2
import numpy as np
from SerialCommunication import *

arduino = serial.Serial(port='COM7', baudrate=9600, timeout=1)

def canny(img):
    """
    Applies Canny edge detection and dilation to improve edge continuity.
    """
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    kernel = 5
    blur = cv2.GaussianBlur(gray, (kernel, kernel), 0)
    edges = cv2.Canny(blur, 150, 200)  # Adjust thresholds for edge sensitivity
    # Dilation to fill small gaps in edges
    edges = cv2.dilate(edges, None, iterations=1)
    return edges

def rectangular_region_of_interest(canny):
    """
    Defines a rectangular region of interest based on the image dimensions.
    """
    height, width = canny.shape
    mask = np.zeros_like(canny)
    top_left = (0, 0)
    bottom_right = (width, int(height * 0.5))  # Bottom half of the frame
    cv2.rectangle(mask, top_left, bottom_right, 255, -1)  # Filled rectangle
    masked_image = cv2.bitwise_and(canny, mask)
    return masked_image

def classify_lines_by_deviation(lines, image_width):
    """
    Classifies lines into left and right based on the standard deviation of their x-coordinates.
    """
    left_lines = []
    right_lines = []
    
    # List to hold x-coordinates for deviation calculation
    left_x = []
    right_x = []
    
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]  # Unpack the single-line array

            # Collect x-coordinates
            x_coords = [x1, x2]
            mean_x = np.mean(x_coords)
            std_x = np.std(x_coords)

            # Classify based on standard deviation of x-coordinates
            if mean_x < image_width // 2:  # Left side of the image
                left_x.append(x_coords)
                left_lines.append([x1, y1, x2, y2])
            else:  # Right side of the image
                right_x.append(x_coords)
                right_lines.append([x1, y1, x2, y2])

    # Optionally, print the standard deviation for debugging
    
    return left_lines, right_lines

def horizontal_distance(lines,image_width):
    left_lines, right_lines = classify_lines_by_deviation(lines, image_width)

    if not left_lines or not right_lines:
        return 0

    firstleft = [left_line[0] for left_line in left_lines]
    firstright = [right_line[0] for right_line in right_lines]
    
    return print(np.max(firstleft) - np.min(firstright))

def horizontal_distance_centered(lines,image):
    left_lines, right_lines = classify_lines_by_deviation(lines, image.shape[1])

    if not left_lines or not right_lines:
        return "None"

    firstleft = [left_line[0] for left_line in left_lines]
    firstright = [right_line[0] for right_line in right_lines]
    right_center = np.min(firstright) - image.shape[1]//2
    left_center = image.shape[1]//2 - np.max(firstleft)
    
    if  right_center>left_center and abs(right_center-left_center) > image.shape[1]//20:
        return "Right"
    if right_center<left_center and abs(left_center-right_center) > image.shape[1]//20:
        return "Left"
    
    return "Centered"




def plot_lines(frame, left_lines, right_lines):
    """
    Draws left and right lines on the image.
    """
    # Plot left lines in blue
    if left_lines:
        for line in left_lines:
            x1, y1, x2, y2 = line  # Unpack the coordinates of the line
            cv2.line(frame, (x1, y1), (x2, y2), (255, 0, 0), 5)

    # Plot right lines in green
    if right_lines:
        for line in right_lines:
            x1, y1, x2, y2 = line  # Unpack the coordinates of the line
            cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 5)

    return frame



# Initialize webcam capture
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    # Edge detection
    canny_image = canny(frame)

    # Region of Interest
    cropped_canny = rectangular_region_of_interest(canny_image)

    # Apply HoughLinesP
    lines = cv2.HoughLinesP(
        cropped_canny,
        rho=1,
        theta=np.pi / 180,
        threshold=50,  # Reduce threshold for more line detection
        minLineLength=50,  # Minimum length of a line
        maxLineGap=20  # Allow larger gaps to connect lines
    )

    # Classify lines into left and right groups
    left_lines, right_lines = classify_lines_by_deviation(lines,frame.shape[0])
    direction= horizontal_distance_centered(lines,frame)
    print(direction)

    send_data(arduino,direction)

    while arduino.in_waiting > 0:
        response = arduino.readline().decode('utf-8').strip()
        print("Arduino says:", response)

    # Draw lines on the frame
    frame_with_lines = plot_lines(frame.copy(), left_lines, right_lines)

    # Show the result
    cv2.imshow("Parking Slot Detection", frame_with_lines)

    # Quit when 'q' is pressed
    key = cv2.waitKey(1)
    if key == ord('q'):
        print("Quitting...")
        break

# Release the capture and close windows
cap.release()
cv2.destroyAllWindows()














