import cv2
import os
import string
import colorama
from colorama import Fore, Style

# ASCII configuration
ASPECT_RATIO = 16 / 9
ASCII_WIDTH = 80  # Width of the ASCII output
ASCII_HEIGHT = int(ASCII_WIDTH / ASPECT_RATIO)
MATRIX_CHARS = "@#%&*+=-:. "

# Function to resize frame
def resize_frame(frame):
    return cv2.resize(frame, (ASCII_WIDTH, ASCII_HEIGHT))

# Function to convert the frame to ASCII
# Updated to use white color for the ASCII characters
def frame_to_ascii(frame):
    ascii_frame = ''
    scale_factor = 256 / len(MATRIX_CHARS)  # Map pixel values to ASCII characters
    for row in frame:
        for pixel in row:
            ascii_index = int(pixel / scale_factor)
            # Remove color effect to keep default CMD color
            ascii_frame += MATRIX_CHARS[ascii_index]
        ascii_frame += '\n'
    return ascii_frame

# Initialize webcam
cap = cv2.VideoCapture(0)  # Use 0 for the default camera

colorama.init(autoreset=True)

if not cap.isOpened():
    print("Error: Unable to access the webcam.")
    exit()

try:
    while True:
        # Read frame from the webcam
        ret, frame = cap.read()
        if not ret:
            print("Error: Unable to read frame from webcam.")
            continue

        # Convert to grayscale
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Resize the frame to ASCII dimensions
        resized_frame = resize_frame(gray_frame)

        # Convert resized frame to ASCII
        ascii_frame = frame_to_ascii(resized_frame)

        # Clear the terminal and print the ASCII frame
        os.system('cls' if os.name == 'nt' else 'clear')
        print(ascii_frame)

        # Exit on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    # Release resources
    cap.release()
