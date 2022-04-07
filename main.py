import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import curses
import logging
import time as t
from pygame import mixer
mixer.init()

logging.basicConfig(filename=".log", filemode="w+", format="%(asctime)s - %(message)s", level=logging.DEBUG)

audio = mixer.Sound(os.path.join('vid', 'audio.mp3'))

curses.initscr()
curses.curs_set(0)
curses.start_color()
curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_RED)
curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLUE)
curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_WHITE)

levels = {
    1: curses.color_pair(2),
    2: curses.color_pair(3),
    3: curses.color_pair(1),
}

render_error_msg = "Cannot fit/Rendering Error"
last_center = (0, 0)
frames = []

def video(src, first_lines, parsed):
    v_width, v_height = (int(x) for x in first_lines.split(','))
    f_width, f_height = v_width // 2, v_height // 2

    start_time = t.time()
    frame_count = 1
    length = len(parsed)
    audio.play()
    
    global last_center, frames

    while parsed:
        time = t.time() - start_time

        if parsed[0].get('time') > time:
            continue
                   
        d_start = t.perf_counter()
        hh, hw = (x//2 for x in src.getmaxyx())

        abs_y = hh - (f_height)
        abs_x = hw - (f_width)
        
        try:
            different_size = last_center != (hh, hw)

            if different_size:
                src.clear()

            first_time = not frames
            buffer = []
            nbuffer = {}

            for index, item in enumerate(parsed[0].get('lines')):
                mod_index = index % 3

                if mod_index == 0:
                    if index > 0:
                        if first_time or different_size:
                            frames.append(nbuffer['level'])
                        else:
                            frames[nbuffer['x'] + (v_width * nbuffer['y'])] = nbuffer['level']
                        
                        buffer.append(nbuffer)
                        nbuffer = {}
                        
                    
                    nbuffer['x'] = item
                elif mod_index == 1:
                    nbuffer['y'] = item
                elif mod_index == 2:
                    nbuffer['level'] = item
            
            src.addstr(0, 0, str(len(buffer)))
            src.addstr(1, 0, str(len(frames)))

            for index, item in enumerate(buffer):
                pair = levels.get(item.get('level') or 0)

                if pair:
                    src.attron(pair)
                
                src.addstr(abs_y + item.get('y'), abs_x + item.get('x'), " ")

                if pair:
                    src.attroff(pair)


            src.addstr(abs_y, abs_x, f'Frame: {frame_count}/{length}')
            src.addstr(abs_y + 1, abs_x, f'Time: {time:.3f}s | Draw: {int((t.perf_counter() - d_start) * 1000000)}ns')
        except curses.error:
            try:
                src.addstr(hh, hw - (len(render_error_msg) // 2), render_error_msg, curses.A_NORMAL)
            except curses.error:
                pass

        src.refresh()
        last_center = (hh, hw)

        frame_count += 1
        parsed.pop(0)
 
def main(src):
    with open('info_txt.inf', 'r') as f:
        lines = [x.strip() for x in f.readlines()]
        parsed = []
        n_item = {}
        mode = 0

        for i, line in enumerate(lines[1:-1]):
            if mode == 0:
                n_item['time'] = float(line)
                mode = 1
            elif mode == 1:
                if line == ',':
                    mode = 0
                    parsed.append(n_item)
                    n_item = {}
                    continue
                if not n_item.get('lines'):
                    n_item['lines'] = []

                    for x in line.split(','):
                        try:
                            n_item['lines'].append(int(x))
                        except ValueError:
                            n_item['lines'].append(0)
            
        # print(parsed[0])

        video(src, lines[0], parsed)

try:
    curses.wrapper(main)
except KeyboardInterrupt:
    pass
