import time

from ch9329 import keyboard
from ch9329 import mouse
from serial import Serial

MODIFIERS = {
    0x0001: "shift",
    0x0004: "ctrl",
    0x0008: "alt_left",  # does not work
    0x0080: "alt_right",  # does not work
    0x20000: "alt",
}

KEY_MAP = {
    # shift key
    "shift_l": "shift",
    "shift_r": "shift",
    "shift": "shift",
    # control key
    "control_r": "ctrl",
    "control_l": "ctrl",
    "ctrl": "ctrl",
    # alt key
    "alt_l": "alt",
    "alt_r": "alt",
    "alt": "alt",
    # window key
    "win_l": "win",
    "win_r": "win",
    # super key
    # SUPER KEY IS DIFFERENT FOR MACOS
    "super_l": "win",
    "super_r": "win",
    # other keys
    "space": " ",
    "period": ".",
    "backspace": "backspace",
    "enter": "\r\n",
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

    def press(self, key: str, state: int) -> None:
        """
        :param key: keysym attribute of tkinter key event
        :param state: state attribute of tkinter key event
        """
        modifiers = [v for k, v in MODIFIERS.items() if k & state]
        modifier = modifiers[0] if modifiers else ""
        key = key.lower()
        key = KEY_MAP.get(key, key)
        keyboard.press(self.serial, key, modifier)

    def release(self) -> None:
        keyboard.release(self.serial)

    def press_and_release(self, key: str, modifier: str = "") -> None:
        keyboard.press(self.serial, key, modifier)
        keyboard.release(self.serial)
