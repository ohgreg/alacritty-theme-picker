import curses
import yaml
import sys
import os

HOME_DIR = os.path.expanduser("~")
THEMES_DIR = HOME_DIR+"/.config/alacritty/themes/"
ALACRITTY_YAML_DIR = HOME_DIR+"/.config/alacritty/alacritty.yml"
ALACRITTY_YAML_BAK_DIR = HOME_DIR+"/.config/alacritty/alacritty.bak.yml"

def color_pair_init(stdscr):
    for i in range(1, 17):
        curses.init_pair(i, i, i)
    curses.init_pair(17, 14, 9)
    curses.init_pair(18, 16, 9)
    curses.init_pair(19, 13, 9)
    curses.init_pair(20, 12, 9)
    curses.init_pair(21, 10, 9)
    curses.init_pair(22, 15, 9)
    curses.init_pair(23, 1, 14)
    curses.init_pair(24, 14, 1)
    curses.init_pair(25, 16, 1)

def get_color(file, mode, color):
    red, green, blue = bytes.fromhex(file["colors"][mode][color][2:])
    return int(red*1000/255), int(green*1000/255), int(blue*1000/255)

def change_theme(stdscr, name):
    with open(THEMES_DIR+name) as f:
        file = yaml.load(f, Loader=yaml.FullLoader)
        colors = ["black", "red", "green", "yellow", "blue", "magenta", "cyan", "white"]
        modes = ["normal", "bright"]

        for i in range(0, len(modes)):
            for j in range(1, len(colors)+1):
                curses.init_color(i*8+j, *get_color(file, modes[i], colors[j-1]))

def get_theme(name):
    with open(THEMES_DIR+name) as f:
        file = yaml.load(f, Loader=yaml.FullLoader)
        f.close()
        return file["colors"]

def set_theme(name):
    if os.path.exists(ALACRITTY_YAML_BAK_DIR):
        file = yaml.safe_load(open(ALACRITTY_YAML_BAK_DIR, "r"))
        file["colors"] = get_theme(name)
        with open(ALACRITTY_YAML_DIR, "w") as f:
            f.truncate(0)
            f.write(yaml.dump(file))
        return
    if os.path.exists(ALACRITTY_YAML_DIR):
        os.system(f"cp {ALACRITTY_YAML_DIR} {ALACRITTY_YAML_BAK_DIR}")
        set_theme(name)

def print_colored_boxes(stdscr):
    h, w = stdscr.getmaxyx()
    y = 0
    x = w//2 - 21
    for i in range(1, 9):
        stdscr.addstr(1+y, 4*i+1+x, "....", curses.color_pair(i))
        stdscr.addstr(2+y, 4*i+1+x, "....", curses.color_pair(i))
    for i in range(1, 9):
        stdscr.addstr(3+y, 4*i+1+x, "....", curses.color_pair(i+8))
        stdscr.addstr(4+y, 4*i+1+x, "....", curses.color_pair(i+8))

def print_code_sample(stdscr):
    h, w = stdscr.getmaxyx()
    y = 0
    x = w//2 - 26
    stdscr.addstr(6+y, 1+x, " "*51, curses.color_pair(9))
    stdscr.addstr(7+y, 1+x, " import qualified"+" "*21+"as ", curses.color_pair(17))
    stdscr.addstr(7+y, 19+x, "Data.Vector.Generic", curses.color_pair(18))
    stdscr.addstr(7+y, 42+x, "V"+9*" ", curses.color_pair(18))
    stdscr.addstr(8+y, 1+x, " import qualified"+" "*29+"as ", curses.color_pair(17))
    stdscr.addstr(8+y, 19+x, "Data.Vector.Generic.Mutable ", curses.color_pair(18))
    stdscr.addstr(8+y, 50+x, "M ", curses.color_pair(18))
    stdscr.addstr(9+y, 1+x, " "*51, curses.color_pair(9))
    stdscr.addstr(10+y, 1+x, " qsort ", curses.color_pair(19))
    stdscr.addstr(10+y, 8+x, ":: ", curses.color_pair(17))
    stdscr.addstr(10+y, 11+x, "("+" "*12+","+" "*6+")", curses.color_pair(18))
    stdscr.addstr(10+y, 12+x, "V.Vector", curses.color_pair(20))
    stdscr.addstr(10+y, 26+x, "Ord", curses.color_pair(20))
    stdscr.addstr(10+y, 32+x, " =>"+" "*5+"-> ", curses.color_pair(17))
    stdscr.addstr(10+y, 21+x, "v a", curses.color_pair(21))
    stdscr.addstr(10+y, 30+x, "a", curses.color_pair(21))
    stdscr.addstr(10+y, 36+x, "v a", curses.color_pair(21))
    stdscr.addstr(10+y, 43+x, "v a"+" "*6, curses.color_pair(21))
    stdscr.addstr(11+y, 1+x, " qsort"+" "*3+"V.modify go"+" "*31, curses.color_pair(18))
    stdscr.addstr(11+y, 8+x, "=", curses.color_pair(17))
    stdscr.addstr(11+y, 22+x, "where", curses.color_pair(17))
    stdscr.addstr(12+y, 1+x, " "*6+"go xs"+" "*3+"M."+" "*7+"xs"+" "*26, curses.color_pair(18))
    stdscr.addstr(12+y, 17+x, "length", curses.color_pair(22))
    stdscr.addstr(12+y, 33+x, "return", curses.color_pair(22))
    stdscr.addstr(12+y, 13+x, "|", curses.color_pair(17))
    stdscr.addstr(12+y, 27+x, "<", curses.color_pair(17))
    stdscr.addstr(12+y, 31+x, "=", curses.color_pair(17))
    stdscr.addstr(12+y, 29+x, "2", curses.color_pair(20))
    stdscr.addstr(12+y, 40+x, "()", curses.color_pair(20))
    stdscr.addstr(13+y, 1+x, " "*12+"|"+" "*11+"= do"+" "*23, curses.color_pair(17))
    stdscr.addstr(13+y, 15+x, "otherwise", curses.color_pair(22))
    stdscr.addstr(14+y, 1+x, " "*14+"p"+" "*4+"M."+" "*5+"xs (M."+" "*7+"xs `   `  ) ", curses.color_pair(18))
    stdscr.addstr(14+y, 17+x, "<-", curses.color_pair(17))
    stdscr.addstr(14+y, 33+x, "length", curses.color_pair(22))
    stdscr.addstr(14+y, 22+x, "read", curses.color_pair(22))
    stdscr.addstr(14+y, 44+x, "div", curses.color_pair(21))
    stdscr.addstr(14+y, 49+x, "2", curses.color_pair(20))
    stdscr.addstr(15+y, 1+x, " "*14+"j"+" "*4+"M.unstablePartition (  p) xs"+" "*4, curses.color_pair(18))
    stdscr.addstr(15+y, 17+x, "<-", curses.color_pair(17))
    stdscr.addstr(15+y, 41+x, "<", curses.color_pair(17))
    stdscr.addstr(16+y, 1+x, " "*18+"(l, pr)   M."+" "*8+"j xs"+" "*9, curses.color_pair(18))
    stdscr.addstr(16+y, 15+x, "let", curses.color_pair(17))
    stdscr.addstr(16+y, 27+x, "=", curses.color_pair(17))
    stdscr.addstr(16+y, 31+x, "splitAt", curses.color_pair(22))
    stdscr.addstr(17+y, 1+x, " "*14+"k    M.unstablePartition (   p) pr"+" "*3, curses.color_pair(18))
    stdscr.addstr(17+y, 17+x, "<-", curses.color_pair(17))
    stdscr.addstr(17+y, 41+x, "==", curses.color_pair(17))
    stdscr.addstr(18+y, 1+x, " "*14+"go l; go   M.     k pr"+" "*15, curses.color_pair(18))
    stdscr.addstr(18+y, 24+x, "$", curses.color_pair(17))
    stdscr.addstr(18+y, 28+x, "drop", curses.color_pair(22))
    stdscr.addstr(19+y, 1+x, " "*51, curses.color_pair(9))

def print_themes(stdscr, themes, current_selected_theme, first_theme):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    message = "Press 'q' to exit or 'Enter' to save theme"
    stdscr.addstr(21, w//2 - len(message)//2, message, curses.color_pair(25))
    stdscr.addstr(23, w//2 + len(max(themes, key=len))//2 - 5, " "*(2-len(str(current_selected_theme+1)))+str(current_selected_theme+1), curses.color_pair(24))
    stdscr.addstr(23, w//2 + len(max(themes, key=len))//2 - 3, "/"+str(len(themes)), curses.color_pair(25))
    if first_theme != 0:
        stdscr.addstr(23, w//2 - len(max(themes, key=len))//2, "🡩", curses.color_pair(25))
    if first_theme < len(themes)-h+26:
        stdscr.addstr(h-2, w//2 - len(max(themes, key=len))//2, "🡫", curses.color_pair(25))

    for theme, row in enumerate(themes[first_theme:(first_theme+h-26)]):
        x = w//2 - len(row)//2
        y = 24 + theme
        if theme+first_theme == current_selected_theme:
            stdscr.addstr(y, x-3, "=>", curses.color_pair(25))
            stdscr.addstr(y, x, row, curses.color_pair(23))
        else:
            stdscr.addstr(y, x, row, curses.color_pair(24))
    stdscr.refresh()

def curses_entry(stdscr):
    stdscr.clear()
    curses.curs_set(0)
    curses.start_color()
    color_pair_init(stdscr)
    stdscr.bkgd(' ', curses.color_pair(1))

    raw_themes = sorted([filename for filename in os.listdir(THEMES_DIR)])
    themes = [os.path.splitext(theme)[0] for theme in raw_themes]
    maxlen = len(max(themes, key=len))
    themes = [" " + theme.replace("-", " ").replace("_", " ") + " "*(maxlen-len(theme)+1) for theme in themes]
    current_selected_theme = 0
    first_theme = 0

    change_theme(stdscr, raw_themes[current_selected_theme])
    print_themes(stdscr, themes, current_selected_theme, first_theme)
    print_colored_boxes(stdscr)
    print_code_sample(stdscr)

    try:
        while True:
            key = stdscr.getch()

            if key == curses.KEY_UP or key == ord("k"):
                h, w = stdscr.getmaxyx()
                if current_selected_theme > 0:
                    if current_selected_theme == first_theme:
                        first_theme -= 1
                    current_selected_theme -= 1
                else:
                    current_selected_theme = len(themes)-1
                    first_theme = len(themes)-h+26

                change_theme(stdscr, raw_themes[current_selected_theme])

            elif key == curses.KEY_DOWN or key == ord("j"):
                h, w = stdscr.getmaxyx()
                if current_selected_theme < len(themes)-1:
                    current_selected_theme += 1
                    if current_selected_theme == (h-26+first_theme):
                        first_theme += 1
                else:
                    current_selected_theme = 0
                    first_theme = 0

                change_theme(stdscr, raw_themes[current_selected_theme])

            elif key == ord("q"):
                break
            elif key == 13:
                raise KeyboardInterrupt
            elif key == curses.KEY_ENTER or key in [10, 13]:
                set_theme(raw_themes[current_selected_theme])
                break

            print_themes(stdscr, themes, current_selected_theme, first_theme)
            print_colored_boxes(stdscr)
            print_code_sample(stdscr)

    except KeyboardInterrupt:
        return

def main():
    curses.wrapper(curses_entry)
    sys.exit(os.EX_OK)

if __name__ == '__main__':
    main()
