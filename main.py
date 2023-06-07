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


def bot_click(file_name: string):
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

    save_result_image(file_name, reference_image, target_image, top_left)

    # Calculate the click position
    click_x = top_left[0] + (target_image.shape[1] // 2)
    click_y = top_left[1] + (target_image.shape[0] // 2)

    # Simulate a click at the best match location
    pyautogui.click(click_x, click_y)

    print(f"✅ Clicked at location: ({click_x}, {click_y})")


def save_result_image(file_name: string, reference_image, target_image, top_left):
    # Draw a rectangle around the target on a copy of the reference image
    image_with_rectangle = reference_image.copy()
    bottom_right = (
        top_left[0] + target_image.shape[1],
        top_left[1] + target_image.shape[0],
    )
    cv2.rectangle(image_with_rectangle, top_left, bottom_right, (0, 0, 255), 2)

    # Save the image with the rectangle
    cv2.imwrite(f"./result/{file_name}.png", image_with_rectangle)

    print(f"✅ Save result image: {file_name}.png")


def bot_press(key: str):
    pyautogui.press(key)
    print(f"✅ Press: {key}")


def bot_shortcut(keymap: str):
    """Simulates holding down each key and releasing them in reverse order.

    Args:
    keymap (str): keymap, example: "ctrl+shift+alt+tab"
    """

    # remove space
    keymap = keymap.replace(" ", "")
    # split by "+"
    list_key = keymap.split("+")

    # key down all key in order
    for key in list_key:
        pyautogui.keyDown(key)

    # key up all key in reverse order
    for key in reversed(list_key):
        pyautogui.keyUp(key)

    print(f"✅ Shortcut: {keymap}")


def bot_type(message: str):
    pyautogui.typewrite(message)
    print(f"✅ Type: {message}")


def perform_image_recognition_on_folder():
    files = os.listdir(TARGET_FOLDER)

    if len(files) == 0:
        print("No file in the target folder.")
        print("Please put the target image in the target folder.")

    # sort file by name
    files.sort()
    print("Files in the target folder: ", files)

    for file in files:
        print(f"{file:-^30s}")

        # separate operate by file name
        file_name, file_extension = os.path.splitext(file)

        if file_extension == ".png":
            bot_click(file)
            continue

        # separate order in file name [order]_[detail] ex. 1_space.pk
        sep_file_name = file_name.split("_")
        # join detail by "_" ex. space_bar
        detail = "_".join(sep_file_name[1:])

        if file_extension == ".bt":
            bot_type(detail)
        elif file_extension == ".bp":
            bot_press(detail)
        elif file_extension == ".bs":
            bot_shortcut(detail)
        # wait 1 sec
        time.sleep(1)


def print_keylist():
    print("All key list, use in press_key()")
    print(pyautogui.KEYBOARD_KEYS)


def init():
    # generate target folder
    if not os.path.exists(TARGET_FOLDER):
        os.makedirs(TARGET_FOLDER)
        print("Init successfully.")


def main():
    init()
    perform_image_recognition_on_folder()


main()
