import cv2
import os
import json
from PIL import Image

user_settings = {}

with open('convert_settings.json', 'r') as json_f:
    user_settings = json.loads(json_f.read())

user_settings['scale'] = max(user_settings['scale'], 1)

video = cv2.VideoCapture(os.path.join('vid', 'visual.mp4'))
count = 0
size_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

CELLS_X = (128 * 2) * user_settings['scale']
CELLS_Y = (36 * 2) * user_settings['scale']

# raw_text = open('info_txt.inf', 'w+')
# raw_text.write(f'{CELLS_X},{CELLS_Y}\n')
frame_rate = int(max(user_settings['frame_rate'], 1))
frames = []
last_frame = []

def get_level(pixel):
    return pixel // user_settings['black_depth']

def frame():
    global count, frames, last_frame

    success, img = video.read()
    
    if not success:
        return False

    img = Image.fromarray(img).convert('L')
    # w, h = img.size
    img = img.resize((CELLS_X, CELLS_Y))
    # img.save('lol.png')

    # success = False

    s = f"{(1/frame_rate) * count}\n"
    data = img.load()

    if not last_frame:
        for y in range(CELLS_Y):
            for x in range(CELLS_X):
                # s += f"{min(}"
                l = get_level(data[x, y])
                s += f"{x},{y},{l},"
                last_frame.append(l)
    else:
        for y in range(CELLS_Y):
            for x in range(CELLS_X):
                i = (y * CELLS_X) + x
                l = get_level(data[x, y])

                if l == last_frame[i]:
                    continue
                
                last_frame[i] = l
                s += f"{x},{y},{l},"

    s += '\n,\n'

    frames.append(s)

    if success:
        count += 1
        print(f'Did frame {count}/{size_count} | {(count * (1 /frame_rate)) :.2f} seconds have been loaded.', end='\r')
            
    return True

try:
    try:
        while frame(): pass
    except KeyboardInterrupt:
        print('\nEnded prematurely')
    print()
    with open('info_txt.inf', 'w+') as f:
        f.write(f'{CELLS_X},{CELLS_Y}\n')
        for i, con in enumerate(frames):
            f.write(con)
            print(f'Outputted converted frame {i}/{len(frames)}', end="\r")
except KeyboardInterrupt:
    pass
