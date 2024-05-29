from argparse import ArgumentParser
from threading import Event
from threading import Thread

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
    ch9329 = CH9329(ch9329_port)
    camera = MS2130(camera_idx, args.fps, exit_flag)
    gui = GUI(camera, ch9329, title=f"HwDesk - {camera_name} - {ch9329_port}")
    Thread(target=camera.screenshot_loop).start()
    gui.mainloop()
    exit_flag.set()
    logger.info("Closing CH9329 port...")
    ch9329.serial.close()


if __name__ == "__main__":
    main()
