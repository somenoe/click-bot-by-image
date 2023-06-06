import pyautogui
import cv2
# import time
import numpy as np
# import sys
import os



def capture_reference_image():
    # Capture a screenshot
    screenshot = pyautogui.screenshot()

    # Convert the PIL image to a NumPy array
    screenshot_array = np.array(screenshot)

    # Convert the color format from RGB to BGR
    screenshot_array = cv2.cvtColor(screenshot_array, cv2.COLOR_RGB2BGR)
    return screenshot_array


def capture_reference_image_and_save():
    # Capture the screen and save it as the reference image
    screenshot = pyautogui.screenshot()
    screenshot.save('reference.png')
    print("Reference image captured successfully.")

def perform_image_recognition_and_click(target):
    # Load the reference and target images
    # reference_image = cv2.imread('reference.png')
    reference_image = capture_reference_image()
    target_image = cv2.imread(target)

    # Perform template matching
    result = cv2.matchTemplate(reference_image, target_image, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    # Get the coordinates of the best match
    top_left = max_loc

    # Calculate the click position
    click_x = top_left[0] + (target_image.shape[1] // 2)
    click_y = top_left[1] + (target_image.shape[0] // 2)

    # Simulate a click at the best match location
    pyautogui.click(click_x, click_y)

    print(f"@{target} Clicked at location: ({click_x}, {click_y})")


# # Capture the reference image
# capture_reference_image()

# # Wait for some time to change the screen state (e.g., switch to the target program)
# time.sleep(5)

# # Perform image recognition and click
# perform_image_recognition_and_click('target.png')
# perform_image_recognition_and_click('target2.png')

# function read file int the folder
def perform_image_recognition_on_folder(path):
    files = os.listdir(path)
    
    if len(files) == 0:
        print("No file in the target folder.")
        print("Please put the target image in the target folder.")
        
    
    # sort file by name
    files.sort()
    print("Files in the target folder: ", files)
    
    for file in files:
        print(file)
        perform_image_recognition_and_click(f'{path}/{file}')
        
  
# # Perform image recognition and click
# perform_image_recognition_on_folder('./targets')

# main function with read argument



        
TARGET_FOLDER = './targets'
def init():
    # generate target folder
    if not os.path.exists(TARGET_FOLDER):
        os.makedirs(TARGET_FOLDER)
        print("Init successfully.")
            
            
def main():
    init()
    perform_image_recognition_on_folder(TARGET_FOLDER)
    
main()
    
# TODO: add function wait until the image appear, recheck every 1 sec
# TODO: add function to handle acion in file name ([order]_[action]_[detail].png)
# ex. 1_click_sumbit.png, 2_wait_for_upload.png, 3_click_close_page.png
# only care for first character in action ex. c(lick), w(ait), s(leep), p(ress)