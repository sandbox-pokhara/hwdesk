import atexit

import cv2
from cv2.typing import MatLike

from hwdesk import logger
from hwdesk.camera.base import BaseCamera


class MS2109(BaseCamera):
    def __init__(self, index: int, fps: int = 5):
        self.index = index
        self.cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)
        if not self.cap.isOpened():
            logger.info(f"Openning video capture device ({index})...")
            self.cap.open(index)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
        self.cap.set(cv2.CAP_PROP_BRIGHTNESS, 0)
        self.cap.set(cv2.CAP_PROP_CONTRAST, 128)
        self.cap.set(cv2.CAP_PROP_SATURATION, 128)
        self.cap.set(cv2.CAP_PROP_FPS, fps)
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        atexit.register(lambda: self.cap.release())
        super().__init__(is_software=False)

    def screenshot(self) -> MatLike | None:
        self.cap.read()
        return self.cap.read()[1]

    def release(self) -> None:
        self.cap.release()
