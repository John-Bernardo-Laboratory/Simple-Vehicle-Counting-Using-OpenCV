# Simple Vehicle Counting Using OpenCV

## Overview
This application performs vehicle counting using OpenCV, a popular computer vision library. It detects and tracks vehicles moving in a video, distinguishing between vehicles moving up and down.

## Installation Steps

### 1. Install Python
- Download and install Python 3.x from [Python's official website](https://www.python.org/downloads/).
- During installation, ensure the option to add Python to your PATH is selected.

### 2. Install Required Libraries
Install the necessary libraries using `pip`. Open your terminal or command prompt and run the following command:

```bash
pip install numpy opencv-python
```

### 3. Running The Scripts 
Open the terminal or command prompt in the repository folder by Shift + right-click and selecting "Open Command Window Here" or "Open PowerShell Window Here," then type:
```bash
python vehicles_counting.py
```
Alternatively, you can open the repository using Visual Studio Code and run the script from the integrated terminal.

To close the frame, press the `Esc` key or `Ctrl + C` in the terminal.

### 4. Updating the Video File Path
To change the video file path, locate the line in the script that initializes the video capture:

```python
cap = cv2.VideoCapture("./test/test_1.mp4")
```
Update this line to point to the location of your video file. For example, if your video file is named my_video.mp4 and located in a different directory, modify the line as follows:

```python
cap = cv2.VideoCapture("./test/my_video.mp4")
```
Ensure the path you provide is relative to the script's location or use an absolute path.

### 5. Troubleshooting

- **Video Not Playing**: Verify that the video file path is correct and the video file is accessible.
- **Library Errors**: Ensure all required libraries are installed correctly.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

  
