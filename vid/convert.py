import cv2
import os
from PIL import Image

video = cv2.VideoCapture(os.path.join('vid', 'visual.mp4'))
count = 0
size_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

CELLS_X = 8
CELLS_Y = 8

def frame():
    success, img = video.imread()
    img = Image.fromarray(img).convert('L')
    w, h = img.size
    img.resize((w // CELLS_X, h // CELLS_Y))

    global count

    success = False
    if success:
        print(f'Did frame {count}/{size_count}')
    
    return success

s = frame()

while s:
     
    s = frame()
