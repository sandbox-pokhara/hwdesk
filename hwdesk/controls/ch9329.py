import time

from ch9329 import keyboard
from ch9329 import mouse
from ch9329.keyboard import Modifier
from serial import Serial

KEY_MAP = {
    "left windows": "win",
    "right windows": "win",
    "left shift": "shift",
    "right shift": "shift",
    "left ctrl": "ctrl",
    "right ctrl": "ctrl",
    "space": " ",
    "decimal": ".",
    "period": ".",
    "backspace": "backspace",
    "enter": "\n",
    "escape": "\x1b",
    "quotedbl": '"',
    "quote": "'",
    "grave": "`",
    "minus": "-",
    "equal": "=",
    "asciitilde": "~",
    "exclam": "!",
    "at": "@",
    "numbersign": "#",
    "dollar": "$",
    "percent": "%",
    "asciicircum": "^",
    "ampersand": "&",
    "asterisk": "*",
    "parenleft": "(",
    "parenright": ")",
    "underscore": "_",
    "plus": "+",
    "tab": "\t",
    "caps_lock": "caps_lock",
    "caps lock": "caps_lock",
    "bracketleft": "[",
    "bracketright": "]",
    "braceleft": "{",
    "braceright": "}",
    "semicolon": ";",
    "colon": ":",
    "apostrophe": "'",
    "backslash": "\\",
    "bar": "|",
    "comma": ",",
    "less": "<",
    "greater": ">",
    "slash": "/",
    "question": "?",
    "return": "\n",
    "prior": "page_up",
    "next": "page_down",
    "page up": "page_up",
    "page down": "page_down",
    "print screen": "print_screen",
    "scroll lock": "scroll_lock",
}

MODIFIER_MAP: dict[str, Modifier] = {
    "windows": "win",
    "left windows": "win_left",
    "right windows": "win_right",
    "alt": "alt",
    "left alt": "alt_left",
    "right alt": "alt_right",
    "ctrl": "ctrl",
    "left ctrl": "ctrl_left",
    "right shift": "shift_right",
    "shift": "shift",
    "left shift": "shift_left",
    "right ctrl": "ctrl_right",
}


class CH9329:
    def __init__(self, port: str) -> None:
        self.port = port
        self.serial = Serial(port, 9600, timeout=0.05)
        self.last_moved = time.time()
        super().__init__()

    def move(self, x: int, y: int) -> None:
        # avoid spamming move
        if time.time() - self.last_moved < 0.05:
            return
        # ignor negative values
        if x < 0 or y < 0:
            return
        mouse.move(self.serial, x, y)
        self.last_moved = time.time()

    def click(self, button: str = "left") -> None:
        mouse.press(self.serial, button)
        mouse.release(self.serial)

    def wheel(self, delta: int = 1) -> None:
        mouse.wheel(self.serial, delta)

    def press(self, key: str, modifiers: list[Modifier] = []) -> None:
        key = key.lower()
        key = KEY_MAP.get(key, key)
        keyboard.press(self.serial, key, modifiers)

    def release(self) -> None:
        keyboard.release(self.serial)

    def press_and_release(
        self, key: str, modifiers: list[Modifier] = []
    ) -> None:
        keyboard.press(self.serial, key, modifiers)
        keyboard.release(self.serial)
