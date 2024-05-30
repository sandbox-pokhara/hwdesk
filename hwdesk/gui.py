import tkinter as tk
from threading import Event
from typing import Any

import cv2
import keyboard
from ch9329.exceptions import InvalidKey
from ch9329.keyboard import Modifier
from cv2.typing import MatLike
from PIL import Image
from PIL import ImageTk

from hwdesk import logger
from hwdesk.camera.base import BaseCamera
from hwdesk.constants import HEIGHT
from hwdesk.constants import WIDTH
from hwdesk.controls.ch9329 import CH9329
from hwdesk.controls.ch9329 import MODIFIER_MAP


class GUI(tk.Tk):
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
        self.exit_flag = Event()
        self.modifiers: set[str] = set()

        self.bind("<Button-1>", self.on_left_click)
        self.bind("<Button-3>", self.on_right_click)
        self.bind("<MouseWheel>", self.on_wheel)
        self.bind("<Motion>", self.on_move)

        self.attributes("-fullscreen", True)  # type:ignore
        self.canvas = tk.Canvas(self, width=WIDTH, height=HEIGHT)
        self.canvas.pack()

        self.after(int(1000 / self.camera.fps), self.gui_loop)

    def on_key_event(self, key_event: keyboard.KeyboardEvent):
        if key_event.name == "esc" and self.exit_on_esc:
            self.exit_flag.set()
            return
        is_modifier = keyboard.is_modifier(key_event.scan_code)
        if key_event.name and key_event.event_type == "down":
            try:
                if is_modifier:
                    self.modifiers.add(key_event.name)
                    self.ch9329.press(key_event.name)
                else:
                    modifiers: list[Modifier] = []
                    for m in self.modifiers:
                        if m in MODIFIER_MAP:
                            modifiers.append(MODIFIER_MAP[m])
                    self.ch9329.press(key_event.name, modifiers)
            except InvalidKey as e:
                logger.error(f"Invalidkey: {e.args}")

        elif key_event.name and key_event.event_type == "up":
            if is_modifier and key_event.name in self.modifiers:
                self.modifiers.remove(key_event.name)
            self.ch9329.release()

    def gui_loop(self):
        if self.exit_flag.is_set():
            self.destroy()
            return
        if self.focus_displayof():
            keyboard.hook(self.on_key_event, suppress=True)
        else:
            keyboard.unhook_all()
        if self.camera.img is not None:
            self.imshow(self.camera.img)
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
