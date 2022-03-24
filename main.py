import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import curses
import time as t
from pygame import mixer
mixer.init()

audio = mixer.Sound(os.path.join('vid', 'audio.mp3'))

curses.initscr()
curses.curs_set(0)
curses.start_color()
curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_RED)
curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLUE)
curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_WHITE)

levels = {
    '1': curses.color_pair(2),
    '2': curses.color_pair(3),
    '3': curses.color_pair(1),
}

render_error_msg = "Cannot fit/Rendering Error"
last_center = (0, 0)

def video(src, first_lines, parsed):
    f_width, f_height = (int(x)//2 for x in first_lines.split(','))
    start_time = t.time()
    frame_count = 1
    length = len(parsed)
    audio.play()
    
    global last_center

    while parsed:
        time = t.time() - start_time

        if parsed[0].get('time') > time:
            continue
                   
        d_start = t.perf_counter()
        hh, hw = (x//2 for x in src.getmaxyx())

        abs_y = hh - (f_height)
        abs_x = hw - (f_width)
        
        try:
            if last_center != (hh, hw):
                src.clear()

            for y, column in enumerate(parsed[0].get('lines')):
                for x, row in enumerate(column):
                    pair = levels.get(row)

                    if pair: 
                        src.attron(pair)
                    src.addstr(abs_y + y, abs_x + x, " ")
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
                n_item['lines'].append(line)
            
        # print(parsed[0])

        video(src, lines[0], parsed)

try:
    curses.wrapper(main)
except KeyboardInterrupt:
    pass
