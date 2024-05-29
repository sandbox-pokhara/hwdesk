import time
from random import uniform

from ch9329 import keyboard
from ch9329 import mouse
from serial import Serial

from hwdesk.controls.base import BaseControls


class CH9329(BaseControls):

    def __init__(self, port: str) -> None:
        self.port = port
        self.serial = Serial(port, 9600, timeout=0.05)
        super().__init__()

    def base_move(self, x: int, y: int) -> None:
        mouse.move(self.serial, x, y)

    def click(self, button: str = "left") -> None:
        mouse.press(self.serial, button)
        time.sleep(uniform(0.02, 0.05))
        mouse.release(self.serial)

    def scroll(self, delta: int = 1) -> None:
        mouse.wheel(self.serial, delta)

    def press_and_release(self, key: str, modifier: str = "") -> None:
        if modifier == "win":
            modifier = "gui"
        keyboard.press(self.serial, key, modifier)
        time.sleep(uniform(0.02, 0.05))
        keyboard.release(self.serial)

    def write(self, text: str) -> None:
        for key in text:
            self.press_and_release(key)
            time.sleep(uniform(0.02, 0.05))

    def release(self) -> None:
        self.serial.close()
