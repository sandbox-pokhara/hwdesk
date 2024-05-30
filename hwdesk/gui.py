import tkinter as tk
from typing import Any

import cv2
import keyboard
from ch9329.exceptions import InvalidKey
from cv2.typing import MatLike
from PIL import Image
from PIL import ImageTk

from hwdesk import logger
from hwdesk.camera.base import BaseCamera
from hwdesk.constants import HEIGHT
from hwdesk.constants import WIDTH
from hwdesk.controls.ch9329 import CH9329


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
        self.attributes("-fullscreen", True)  # type:ignore

        self.bind("<Button-1>", self.on_left_click)
        self.bind("<Button-3>", self.on_right_click)
        self.bind("<MouseWheel>", self.on_wheel)
        self.bind("<Motion>", self.on_move)

        self.bind("<Win_L>", self.no_bubble_key_event)
        self.bind("<Win_R>", self.no_bubble_key_event)
        self.bind("<Alt-F4>", self.no_bubble_key_event)

        self.bind("<KeyPress>", self.on_key_down)
        self.bind("<KeyRelease>", self.on_key_up)

        # "<Alt-Tab>" doesnot seems to be handled properly by tkinter
        # it allows pass thorugh, that's why we need keyboard module for
        # that to suppress the event
        keyboard.add_hotkey("alt + tab", self.alt_tab_press, suppress=True)
        self.canvas = tk.Canvas(self, width=WIDTH, height=HEIGHT)
        self.canvas.pack()

        self.after(int(1000 / self.camera.fps), self.gui_loop)

    def gui_loop(self):
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

    def no_bubble_key_event(self, event: Any):
        try:
            self.ch9329.press(event.keysym, event.state)
        except InvalidKey as e:
            logger.error(f"Invalidkey: {e.args}")
        else:
            self.ch9329.release()
        finally:
            # this prevents from events bubbling
            return "break"

    def alt_tab_press(self, _: Any | None = None):
        try:
            ALT_KEY = 0x20000
            self.ch9329.press("tab", ALT_KEY)
        except InvalidKey as e:
            logger.error(f"Invalidkey: {e.args}")

    def win_key_press(self, _: Any | None = None):
        try:
            self.ch9329.press("gui", 0)
        except InvalidKey as e:
            logger.error(f"Invalidkey: {e.args}")
        else:
            self.ch9329.release()

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

    def on_key_down(self, event: Any):
        try:
            self.ch9329.press(event.keysym, event.state)
        except InvalidKey as e:
            logger.error(f"Invalidkey: {e.args}")

    def on_key_up(self, event: Any):
        self.ch9329.release()
        if self.exit_on_esc and event.keysym.lower() == "escape":
            self.destroy()

    def on_wheel(self, event: Any):
        self.ch9329.wheel(event.delta // 100)
