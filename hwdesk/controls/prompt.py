from tkinter.messagebox import showerror  # type:ignore
from tkinter.simpledialog import askstring

import serial.serialutil
import serial.tools.list_ports
from ch9329.config import get_serial_number
from serial import Serial


def ask_ch9329_port():
    prompt: list[str] = []
    prompt.append("Please enter the index of CH9329 you want to access:")
    valid_ports: list[str] = []
    for i in serial.tools.list_ports.comports():
        try:
            if i.vid == 6790 and i.pid == 29987:
                ser = Serial(i.name, 9600, timeout=0.05)
                serial_number = get_serial_number(ser)
                prompt.append(f"Port={i.name}, Serial={serial_number}")
                valid_ports.append(i.name)
        except serial.serialutil.SerialException:
            pass
    if valid_ports == []:
        showerror("HwDesk Error", "No CH9329 devices found.")
        return ""
    port = askstring(
        "CH9329 Selection", "\n".join(prompt), initialvalue=valid_ports[0]
    )
    if port not in valid_ports:
        showerror("HwDesk Error", "Please select a valid CH9329 port.")
        return ""
    return port
