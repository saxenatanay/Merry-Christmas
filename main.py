import time
import sys
import os
import threading
import shutil
from colorama import init, Fore, Style

init(autoreset=True)

TREE = [
    "         *         ",
    "        ***        ",
    "       *****       ",
    "      *******      ",
    "     *********     ",
    "    ***********    ",
    "   *************   ",
    "  ***************  ",
    " ***************** ",
    "        |||        ",
    "        |||        "
]

COLORS = [Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.CYAN, Fore.MAGENTA, Fore.WHITE]


def clear():
    """Smooth screen refresh: move cursor to top instead of clearing."""
    sys.stdout.write("\033[H")
    sys.stdout.flush()


def get_terminal_width():
    try:
        return shutil.get_terminal_size().columns
    except:
        return 100


def print_tree_with_lyrics(frame, lyrics_lines):
    """Draw the color-changing tree with heading and lyrics."""
    terminal_width = get_terminal_width()
    max_tree_width = len(TREE[-1])
    gap = 10
    lyric_start_col = max_tree_width + gap
    max_lyric_width = max(10, terminal_width - lyric_start_col - 2)
    lyric_start_row = len(TREE) // 2 - 2

    output_lines = []

    heading = "Enjoy The Lyrics With The Christmas Tree"
    centered_heading = heading.center(max_tree_width)
    output_lines.append(Fore.YELLOW + Style.BRIGHT + centered_heading + Style.RESET_ALL)
    output_lines.append("") 

    for i, row in enumerate(TREE):
        line = ""
        for j, ch in enumerate(row):
            if ch == '*':
                color = COLORS[(j + frame) % len(COLORS)]
                line += color + ch + Style.RESET_ALL
            else:
                line += ch

        lyric_index = i - lyric_start_row
        if 0 <= lyric_index < len(lyrics_lines):
            lyric_text = lyrics_lines[lyric_index][:max_lyric_width]
            spaces = " " * (lyric_start_col - len(row))
            line += spaces + lyric_text

        output_lines.append(line)

    sys.stdout.write("\n".join(output_lines) + "\n")
    sys.stdout.flush()


def animate(shared, stop_event):
    frame = 0
    os.system('cls' if os.name == 'nt' else 'clear')
    sys.stdout.write("\033[?25l")
    try:
        while not stop_event.is_set():
            clear()
            print_tree_with_lyrics(frame, shared["lyrics_display"])
            frame += 1
            time.sleep(0.4)
    finally:
        sys.stdout.write("\033[?25h")
        sys.stdout.flush()


def type_lyrics(lyrics, shared):
    displayed = []
    for line in lyrics:
        current_line = ""
        for ch in line:
            current_line += ch
            displayed_partial = displayed + [current_line]
            shared["lyrics_display"] = displayed_partial
            time.sleep(0.05)
        displayed.append(line)
        shared["lyrics_display"] = displayed
        time.sleep(0.6)


def main():
    lyrics_path = "lyrics.txt"
    if not os.path.exists(lyrics_path):
        print("Please create a 'lyrics.txt' file with your lyrics.")
        return

    with open(lyrics_path, "r", encoding="utf-8") as f:
        lyrics = [line.strip() for line in f.readlines() if line.strip()]

    shared = {"lyrics_display": []}
    stop_event = threading.Event()

    anim_thread = threading.Thread(target=animate, args=(shared, stop_event), daemon=True)
    anim_thread.start()

    try:
        type_lyrics(lyrics, shared)
        time.sleep(2)
        stop_event.set()
        anim_thread.join()
        clear()
        print_tree_with_lyrics(0, shared["lyrics_display"])
        print("\n🎄 Merry Christmas 🎶")
    except KeyboardInterrupt:
        stop_event.set()
        print("\nExiting...")


if __name__ == "__main__":
    main()
