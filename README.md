# LagtrainCurses
## Rendering Lagtrain with a Terminal integrated with Curses using Python3

### Getting Started

1. You will need to install following packages (if you haven't installed them yet)

- PyGame (audio)
- windows-curses (Windows only, rendering)
- Pillow (Video to ASCII Conversion, image scaling)
- opencv-python (Video to ASCII Conversion, frame getting)

*Note to self: why not just render the video by a video file instead of a file that contains readable frames.*

2. Converting

Run `convert.py` and wait for it to finish converting the video into readable frames.

The main file will need the readable frames file to directly run it.

3. Run (You will need a terminal to run this)

Your current directory in your terminal should be changed into folder with the main file in it, then type `python main.py` or `python3 main.py`.
