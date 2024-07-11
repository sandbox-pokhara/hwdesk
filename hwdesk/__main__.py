from argparse import ArgumentParser
from threading import Event
from threading import Thread

import cv2
from serial import Serial

from hwdesk import logger
from hwdesk.camera.ms2130 import MS2130
from hwdesk.camera.prompt import ask_camera_idx
from hwdesk.controls.ch9329 import CH9329
from hwdesk.controls.prompt import ask_ch9329_port
from hwdesk.gui import GUI


def main():
    parser = ArgumentParser()
    parser.add_argument("--fps", default=30, type=int)
    args = parser.parse_args()
    camera_idx, camera_name = ask_camera_idx()
    if camera_idx == -1:
        exit(1)
    ch9329_port = ask_ch9329_port()
    if not ch9329_port:
        exit(1)
    exit_flag = Event()
    serial = Serial(ch9329_port, 9600, timeout=0.05)
    video_capture = cv2.VideoCapture(camera_idx, cv2.CAP_DSHOW)
    if not video_capture.isOpened():
        logger.info(f"Openning video capture device ({camera_idx})...")
        video_capture.open(camera_idx)
    ch9329 = CH9329(serial)
    camera = MS2130(video_capture, args.fps, exit_flag)
    gui = GUI(camera, ch9329, title=f"HwDesk - {camera_name} - {ch9329_port}")
    Thread(
        target=camera.screenshot_loop, kwargs={"auto_release": True}
    ).start()
    gui.mainloop()
    exit_flag.set()
    logger.info("Closing CH9329 port...")
    ch9329.serial.close()


if __name__ == "__main__":
    main()
