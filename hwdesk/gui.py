import tkinter as tk
from typing import Any
from typing import Callable

import cv2
import keyboard
from cv2.typing import MatLike
from PIL import Image
from PIL import ImageTk

from hwdesk import logger
from hwdesk.camera.base import BaseCamera
from hwdesk.constants import HEIGHT
from hwdesk.constants import WIDTH
from hwdesk.controls.ch9329 import CH9329
from hwdesk.controls.ch9329 import MODIFIERS


class GUI(tk.Tk):

    # we need to keep track of hook callback to
    # unhook it
    _hook: list[Callable[[], None]] = []

    def __init__(
        self,
        camera: BaseCamera,
        ch9329: CH9329,
        title: str = "Window",
        exit_on_esc: bool = True,
        fps: bool = True,
    ):
        super().__init__()
        self.camera = camera
        self.ch9329 = ch9329
        self.title(title)
        self.resizable(False, False)
        self.exit_on_esc = exit_on_esc
        self.show_fps = fps
        self.fps_font_size = 16
        self.attributes("-fullscreen", True)  # type:ignore

        self.down_modifier: str = ""

        self.bind("<Button-1>", self.on_left_click)
        self.bind("<Button-3>", self.on_right_click)
        self.bind("<MouseWheel>", self.on_wheel)
        self.bind("<Motion>", self.on_move)
        self.canvas = tk.Canvas(self, width=WIDTH, height=HEIGHT)
        self.canvas.pack()

        self.after(int(1000 / self.camera.fps), self.gui_loop)

    def on_key_event(self, key_event: keyboard.KeyboardEvent):
        if key_event.name == "esc" and self.exit_on_esc:
            keyboard.unhook_all()
            self.destroy()
        if key_event.name and key_event.event_type == "down":
            modifier = [
                k for k, v in MODIFIERS.items() if v == self.down_modifier
            ]
            if modifier:
                self.ch9329.press(key_event.name, modifier[0])
            else:
                self.ch9329.press(key_event.name, 0)
            if keyboard.is_modifier(key_event.scan_code):
                self.down_modifier = key_event.name
        elif key_event.event_type == "up":
            if keyboard.is_modifier(key_event.scan_code):
                self.down_modifier = ""
            self.ch9329.release()

        logger.info(f"[EVENT]{key_event}")

    def gui_loop(self):
        if self.camera.img is not None:
            self.imshow(self.camera.img)
        if self and self.focus_displayof():
            self._hook.append(keyboard.hook(self.on_key_event, suppress=True))
        elif self._hook:
            keyboard.unhook_all()

        self.after(int(1000 / self.camera.fps), self.gui_loop)

    def imshow(self, img: MatLike):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.image = Image.fromarray(img)  # type: ignore
        self.tk_image = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, image=self.tk_image, anchor=tk.NW)  # type: ignore
        if self.show_fps:
            l = tk.Label(
                self,
                text=f"FPS:{self.camera.fps:.2f}",
                fg="lime green",
                bg="grey",
                font=f"monospace {self.fps_font_size}",
            )
            l.place(x=0, y=0)
        self.update()

    def on_move(self, event: Any):
        mere_pixel = 1
        x, y = event.x // mere_pixel, event.y // mere_pixel
        x *= mere_pixel
        y *= mere_pixel
        self.ch9329.move(x, y)

    def on_left_click(self, event: Any):
        self.ch9329.click(button="left")

    def on_right_click(self, event: Any):
        self.ch9329.click(button="right")

    def on_wheel(self, event: Any):
        self.ch9329.wheel(event.delta // 100)
