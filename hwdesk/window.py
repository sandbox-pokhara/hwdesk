import queue
import time
import tkinter as tk
from dataclasses import dataclass
from typing import Any

import cv2
from cv2.typing import MatLike
from numpy.typing import NDArray
from PIL import Image
from PIL import ImageTk

from hwdesk.actions.actions import Action
from hwdesk.actions.actions import Click
from hwdesk.actions.actions import Move
from hwdesk.actions.actions import PressAndRelease
from hwdesk.controls.key_map import get_key_with_type


@dataclass()
class MouseEvent:
    MOVE: int = 0b00

    LDOWN: int = 0b01
    LUP: int = 0b10
    # L DOWN|UP

    RDOWN: int = 0b0100
    RUP: int = 0b1000
    # R DOWN|UP

    SCROLLD: int = 0b010000
    SCROLLU: int = 0b100000
    # S DOWN|UP


@dataclass()
class KeyEvent:
    MultiPress: int = 0b00

    Press: int = 0b01
    Release: int = 0b10


class ImgWindow:
    """
    Creates a first base_root window; that all other topLevel window can stack on.
    :param title: Name of the TopLevel window
    :type title: str
    :param exit_on_esc: handel exit on esc `default=True`
    :type exit_on_esc: bool

    For Keyboard and Mouse Events, user must overload the
    default mouse/keyboard callbacks ;
    example:-
    ```py
    w = Window("Window_Name")
    w.keyboard_callback = my_key_cllbck # my_key_cllbck; callable
    w.mouse_callback = my_mouse_cllbck # my_mouse_cllbck;callable

    def my_key_cllbck(keys: list[str], event: KeyEvent):
        ...
    def my_mouse_cllbck(x: int, y: int, event: MouseEvent, delta: int = 0):
        ...
    ```

    When typing to handle mainloop yourself,
    some keypress/mouse events might be skipped,
    So if you have single window with static items, I suggest you use mainloop,
    Fewer the delay_ms in imshow the more accurates are the keypress/mouse events.


    """

    base_root: tk.Tk | None = None

    def __new__(
        cls, title: str = "Window", exit_on_esc: bool = True, fps: bool = True
    ):
        if not ImgWindow.base_root:
            # Create base window and hide it
            ImgWindow.base_root = tk.Tk()
            ImgWindow.base_root.geometry("0x0")
            ImgWindow.base_root.resizable(False, False)
        return super().__new__(cls)

    def __init__(
        self, title: str = "Window", exit_on_esc: bool = True, fps: bool = True
    ):
        self.root = tk.Toplevel(ImgWindow.base_root)
        self.root.title(title)
        self.root.resizable(False, False)
        self.exit_on_esc = exit_on_esc
        self.show_fps = fps
        self.fps_font_size = 16

        self.root.bind(
            "<Button-1>",
            lambda x: self.mouse_callback(x, "left"),  # type:ignore
        )
        self.root.bind(
            "<Button-3>",
            lambda x: self.mouse_callback(x, "right"),  # type:ignore
        )
        self.root.bind("<Motion>", self._on_move)  # type:ignore
        self.root.bind("<KeyPress>", self._on_key_down)  # type:ignore
        self.root.bind("<KeyRelease>", self._on_key_up)  # type:ignore

        self.down_keys: dict[str, Any] = {}
        self.down_mouse: dict[int, Any] = {}

        self.canvas = tk.Canvas(
            self.root, width=self.root.size()[0], height=self.root.size()[1]
        )
        self.last_time = time.time()
        self.canvas.pack()

        # is active to handle canvas destroy
        self.width = -1
        self.height = -1

        # list of actions registered
        self.actions: queue.Queue[Action] = queue.Queue()

    def imshow(self, img: MatLike | NDArray[Any], delay_ms: int = 100):
        """
        Shows image-array in tkinter canvas
        :param img: image array
        :type img: MatLike | NDArray[Any]
        :param delay_ms: amount of milliseconds to sleep after showing
        :type delay_ms: int
        """
        if not self.root.winfo_exists():
            return
        width, height = img.shape[:2][::-1]
        if width != self.width or height != self.height:
            self.root.resizable(True, True)
            self.root.geometry(f"{width}x{height}")
            self.width = width
            self.height = height
            self.root.resizable(False, False)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.image = Image.fromarray(img)  # type: ignore
        self.tk_image = ImageTk.PhotoImage(self.image)
        self.canvas.config(width=width, height=height)
        self.canvas.create_image(0, 0, image=self.tk_image, anchor=tk.NW)  # type: ignore
        now = time.time()
        self.fps = 1 / (now - self.last_time)
        self.last_time = now

        if self.show_fps:
            l = tk.Label(
                self.root,
                text=f"FPS:{self.fps:.2f}",
                fg="lime green",
                bg="grey",
                font=f"monospace {self.fps_font_size}",
            )
            l.place(x=0, y=0)

        self.root.update()

        """
            If their was mouse/keydown but window was unfocused
            before the up event could be registered,
            then simply remove the down events,
        """
        if self.root.winfo_exists() and not self.root.focus_displayof():
            if self.down_keys and self.down_mouse:
                self.down_keys.clear()
                self.down_mouse.clear()
            self.actions = queue.Queue()

    def mainloop(self):
        """
        Default mainloop from tkinter,
        Use this if you have single window
        """
        self.root.mainloop()

    def mouse_callback(self, event: tk.Event, e_type: str):  # type:ignore
        relx, rely = event.x, event.y
        if e_type == "left":
            self.actions.put(Click(button="left"))
        elif e_type == "right":
            self.actions.put(Click(button="right"))
        elif e_type == "move":
            self.actions.put(Move(x=relx, y=rely, humanize_x=0, humanize_y=0))
        else:
            print(f"Unknown type{e_type}")

    def _on_move(self, event: tk.Event):  # type:ignore
        mere_pixel = 1
        x, y = event.x // mere_pixel, event.y // mere_pixel
        x *= mere_pixel
        y *= mere_pixel
        event.x = x

        event.y = y
        self.mouse_callback(event, "move")  # type:ignore

    def keyboard_callback(self, keys: list[str], event: int):
        action: Action = Action()
        if event == KeyEvent.MultiPress:
            modif: str = ""
            nkey: str = ""
            for key in keys:
                mdf, key = get_key_with_type(key)
                if mdf:
                    modif = key
                else:
                    nkey = key

            action = PressAndRelease(key=nkey, modifier=modif)
        elif event == KeyEvent.Press and keys:
            modif = ""
            mdf, nkey = get_key_with_type(keys[0])
            if mdf:
                modif = nkey
                nkey = ""
            action = PressAndRelease(key=nkey, modifier=modif)
        self.actions.put(action)

    def _on_key_down(self, event: tk.Event):  # type:ignore
        keys = (
            [i for i in self.down_keys] + [event.keysym.lower()]
            if event.keysym not in self.down_keys
            else []
        )
        event_type: int = KeyEvent.Press

        if len(keys) > 1:
            event_type: int = KeyEvent.MultiPress

        self.down_keys[event.keysym.lower()] = event
        self.keyboard_callback(keys, event_type)

    def _on_key_up(self, event: tk.Event):  # type:ignore
        if self.exit_on_esc and event.keysym.lower() == "escape":
            self.root.destroy()
        self.down_keys.clear()
