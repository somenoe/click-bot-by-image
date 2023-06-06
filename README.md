# Auto Click Bot by Image

This project is a Python script for performing image recognition and clicking on the best match location. It uses the PyAutoGUI library to simulate mouse clicks and the OpenCV library for image recognition.

## Getting Started

To get started with this project, you will need to install the following dependencies:

- Python 3.x
- PyAutoGUI
- OpenCV

You can install these dependencies using pip:

```
pip install -r requirements.txt
```

## Usage

1. Capture the image of the button you want to click on
2. Add the image to the `targets` folder. The file name will be used as the order to click (e.g., `1.png`, `2.png`, `3.png`, etc.)
3. Open the application you want to click on
4. Run the script

```
python main.py
```

## Build

You can build the script into an executable file using PyInstaller:

```
pyinstaller --onefile main.py
```

The executable file will be in the `dist` folder.

## TODO

- [ ] Add function to wait until the image appears, recheck every 1 sec
- [ ] Add function to handle action in file name (`[order]_[action]_[detail].png`)
- [ ] Only care for the first character in action (e.g., `c`lick, `w`ait, `s`leep, `p`ress)

