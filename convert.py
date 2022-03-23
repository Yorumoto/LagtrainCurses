import cv2
import os
from PIL import Image

video = cv2.VideoCapture(os.path.join('vid', 'visual.mp4'))
count = 0
size_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

CELLS_X = 128 * 2
CELLS_Y = 36 * 2

raw_text = open('info_txt.inf', 'w+')
raw_text.write(f'{CELLS_X},{CELLS_Y}\n')
frame_rate = 15

def frame():
    global count

    success, img = video.read()
    
    if not success:
        return False

    img = Image.fromarray(img).convert('L')
    w, h = img.size
    img = img.resize((CELLS_X, CELLS_Y))
    # img.save('lol.png')

    # success = False

    s = f"{(1/frame_rate) * count}\n"
    data = img.load()

    for y in range(CELLS_Y):
        for x in range(CELLS_X):
            s += f"{data[x, y] // 75}"
        s += "\n"
    s += ',\n'

    raw_text.write(s)

    if success:
        count += 1
        print(f'Did frame {count}/{size_count}', end='\r')
            
    return True

try:
    while frame(): pass
except KeyboardInterrupt:
    pass

raw_text.close()
