from typing import Literal

MODIFERS_TABLE = {
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
}

KEY_TABLE = {
    "space": " ",
    "period": ".",
    "backspace": "backspace",
    "enter": "\r",
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
}


def get_key_with_type(key: str) -> tuple[Literal[0] | Literal[1], str]:
    """
    returns tuple of Literal 1 for modifiers with it's mapping
    and return 0, for other non special keys
    """
    _type = 0
    nkey = MODIFERS_TABLE.get(key, key)
    if nkey == key:
        nkey = KEY_TABLE.get(key, key)
        return (_type, nkey)
    return (1, nkey)
