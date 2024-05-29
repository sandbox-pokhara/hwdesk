import inspect
import os
import time
from random import randint
from typing import Any
from typing import ClassVar

from pydantic import BaseModel

from hwdesk.controls.base import BaseControls


class Action(BaseModel):
    source: list[str] = []
    last_moved: ClassVar[float] = 0

    def __init__(self, **data: Any):
        frame = inspect.currentframe()
        if frame:
            frame = frame.f_back
        data["source"] = []
        while frame:
            if frame.f_code.co_filename.endswith("__main__.py"):
                break
            location = (
                os.path.relpath(frame.f_code.co_filename)
                + ":"
                + str(frame.f_lineno)
            )
            data["source"].append(location)  # type:ignore
            frame = frame.f_back
        super().__init__(**data)

    def execute(
        self, controls: BaseControls, off_x: int = 0, off_y: int = 0
    ) -> None:
        raise NotImplementedError("Execute method is not implemented.")


class Move(Action):
    x: int
    y: int
    humanize_x: int = 5
    humanize_y: int = 5

    def execute(
        self, controls: BaseControls, off_x: int = 0, off_y: int = 0
    ) -> None:
        controls.move(
            self.x + off_x,
            self.y + off_y,
            self.humanize_x,
            self.humanize_y,
        )
        Action.last_moved = time.time()


class MoveAndClick(Action):
    x: int
    y: int
    humanize_x: int = 5
    humanize_y: int = 5
    button: str = "left"

    def execute(
        self, controls: BaseControls, off_x: int = 0, off_y: int = 0
    ) -> None:
        controls.move(
            self.x + off_x,
            self.y + off_y,
            self.humanize_x,
            self.humanize_y,
        )
        controls.click(self.button)
        Action.last_moved = time.time()


class Scroll(Action):
    delta: int = 1

    def execute(
        self, controls: BaseControls, off_x: int = 0, off_y: int = 0
    ) -> None:
        controls.scroll(self.delta)


class Click(Action):
    button: str = "left"

    def execute(
        self, controls: BaseControls, off_x: int = 0, off_y: int = 0
    ) -> None:
        controls.click(self.button)


class MoveAndClickOnRect(Action):
    rect: tuple[int, int, int, int]
    button: str = "left"
    padding: int = 0

    def execute(
        self, controls: BaseControls, off_x: int = 0, off_y: int = 0
    ) -> None:
        x, y, w, h = self.rect
        x = randint(x, x + w - self.padding * 2) + self.padding
        y = randint(y, y + h - self.padding * 2) + self.padding
        controls.move(
            x + off_x,
            y + off_y,
            humanize_x=0,
            humanize_y=0,
        )
        controls.click(self.button)
        Action.last_moved = time.time()


class PressAndRelease(Action):
    key: str
    modifier: str = ""

    def execute(
        self, controls: BaseControls, off_x: int = 0, off_y: int = 0
    ) -> None:
        controls.press_and_release(self.key, self.modifier)


class Write(Action):
    text: str

    def execute(
        self, controls: BaseControls, off_x: int = 0, off_y: int = 0
    ) -> None:
        controls.write(self.text)


class Sleep(Action):
    duration: float

    def execute(
        self, controls: BaseControls, off_x: int = 0, off_y: int = 0
    ) -> None:
        time.sleep(self.duration)
