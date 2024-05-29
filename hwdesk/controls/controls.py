import serial.serialutil
import serial.tools.list_ports
from ch9329.config import get_serial_number
from serial import Serial

from hwdesk import logger
from hwdesk.controls.base import BaseControls
from hwdesk.controls.ch9329 import CH9329


def find_ch9329_port_by_name(name: str) -> str:
    logger.info(f"Searching CH9329 device by name {name}...")
    # search the name in serial number omitting the words
    # andreu and @ad
    search_str = name.replace("andreu", "").replace("@ad", "")
    while True:
        for i in serial.tools.list_ports.comports():
            try:
                if i.vid == 6790 and i.pid == 29987:
                    logger.info(f"CH929 found at port {i.name}.")
                    logger.info("Verifying serial number...")
                    ser = Serial(i.name, 9600, timeout=0.05)
                    serial_number = get_serial_number(ser)
                    logger.info(f"Serial number: {serial_number}")
                    if search_str in serial_number.lower():
                        logger.info("Success.")
                        return i.name
                    else:
                        logger.error("Serial number verification failed.")
                    ser.close()
            except serial.serialutil.SerialException as e:
                logger.error(e)
        logger.error("Retrying after 30 seconds.")


def get_controls_module(server_name: str = "", port: str = "") -> BaseControls:
    if server_name:
        port = find_ch9329_port_by_name(server_name)
        return CH9329(port)
    elif port.startswith("COM"):
        return CH9329(port)
    else:
        raise RuntimeError(f"Unknown ch9329 identify {server_name} | {port}.")
