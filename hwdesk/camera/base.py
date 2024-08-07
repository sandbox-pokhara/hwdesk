import atexit
import sys
import time
from threading import Event

import cv2
import numpy as np
from cv2.typing import MatLike

from hwdesk import logger
from hwdesk.constants import HEIGHT
from hwdesk.constants import WIDTH


class BaseCamera:
    def __init__(
        self,
        camera: cv2.VideoCapture,
        fps: int = 10,
        exit_flag: Event | None = None,
    ):
        logger.info("Initializing camera...")
        self.img: MatLike | None = np.zeros((HEIGHT, WIDTH, 3), np.uint8)
        self.exit_flag = exit_flag
        self.fps = fps
        self.current_fps = fps
        self.cap = camera
        assert self.cap.isOpened()
        assert self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
        assert self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)
        assert self.cap.set(cv2.CAP_PROP_FPS, fps)
        video_format = self.cap.get(cv2.CAP_PROP_FOURCC)
        video_format = int(video_format).to_bytes(4, sys.byteorder).decode()
        logger.info(f"MS2130 video format: {video_format}")
        atexit.register(lambda: self.cap.release())

    def screenshot(self):
        self.img = self.cap.read()[1]

    def screenshot_loop(self, auto_release: bool):
        while True:
            if self.exit_flag and self.exit_flag.is_set():
                if auto_release:
                    logger.info("Releasing camera...")
                    self.release()
                break
            start = time.time()
            self.screenshot()
            elapsed = time.time() - start
            self.fps = 1 / elapsed

    def release(self) -> None:
        self.cap.release()
