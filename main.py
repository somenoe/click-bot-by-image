# import sys
import time
import string
import cv2
import numpy as np
import os
import pyautogui

TARGET_FOLDER = "./targets"


def capture_reference_image():
    # Capture a screenshot
    screenshot = pyautogui.screenshot()

    # Convert the PIL image to a NumPy array
    screenshot_array = np.array(screenshot)

    # Convert the color format from RGB to BGR
    screenshot_array = cv2.cvtColor(screenshot_array, cv2.COLOR_RGB2BGR)
    return screenshot_array


def template_matching(
    reference_image,
    target_image,
):
    # Perform template matching
    result = cv2.matchTemplate(reference_image, target_image, cv2.TM_CCORR_NORMED)
    # Find the best match
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    # Calculate the percent match
    percent_match = max_val * 100

    return percent_match, max_loc


def perform_image_recognition_and_click(file_name: string):
    # Load the reference and target images
    target_image = cv2.imread(f"{TARGET_FOLDER}/{file_name}")

    runtimes = 0
    MAX_RUNTIMES = 15
    MIN_MATCH_PERCENT = 90
    percent_match = 0
    while percent_match <= MIN_MATCH_PERCENT:
        reference_image = capture_reference_image()

        percent_match, max_loc = template_matching(reference_image, target_image)
        print(f"@{file_name} Percent match: {percent_match:.2f}%")

        if percent_match <= MIN_MATCH_PERCENT:
            print(f"@{file_name} Not found, wait 1 sec and try again.")
            runtimes += 1
            if runtimes >= MAX_RUNTIMES:
                print(f"@{file_name} Not found, 10 times, stop.")
                return
            # wait 1 sec
            time.sleep(1)

    # Get the coordinates of the best match
    top_left = max_loc

    # Calculate the click position
    click_x = top_left[0] + (target_image.shape[1] // 2)
    click_y = top_left[1] + (target_image.shape[0] // 2)

    # Draw a rectangle around the target on a copy of the reference image
    image_with_rectangle = reference_image.copy()
    bottom_right = (
        top_left[0] + target_image.shape[1],
        top_left[1] + target_image.shape[0],
    )
    cv2.rectangle(image_with_rectangle, top_left, bottom_right, (0, 0, 255), 2)

    # Save the image with the rectangle
    cv2.imwrite(f"./result/{file_name}.png", image_with_rectangle)

    # Simulate a click at the best match location
    pyautogui.click(click_x, click_y)

    print(f"@{file_name} Clicked at location: ({click_x}, {click_y})")


def bot_type(text: string):
    pyautogui.typewrite(text)


def perform_image_recognition_on_folder():
    files = os.listdir(TARGET_FOLDER)

    if len(files) == 0:
        print("No file in the target folder.")
        print("Please put the target image in the target folder.")

    # sort file by name
    files.sort()
    print("Files in the target folder: ", files)

    for file in files:
        # perform_image_recognition_and_click(file)
        print(f"{file>20}")


def init():
    # generate target folder
    if not os.path.exists(TARGET_FOLDER):
        os.makedirs(TARGET_FOLDER)
        print("Init successfully.")


def main():
    init()
    perform_image_recognition_on_folder()


main()

# TODO: add function wait until the image appear, recheck every 1 sec
# TODO: add function to handle acion in file name ([order]_[action]_[detail].png)
# ex. 1_click_sumbit.png, 2_wait_for_upload.png, 3_click_close_page.png
# only care for first character in action ex. c(lick), w(ait), s(leep), p(ress)
