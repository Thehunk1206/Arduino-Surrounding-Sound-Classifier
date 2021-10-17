import serial
from serial.serialutil import SerialException

import sys
import os
import time

SERIAL_TIMEOUT = 4
SERIAL_PORT = '/dev/ttyACM0'
BAUD_RATE = 9600


def init_serial_port(port: str, baudrate: int = 9600):
    '''
    initialize serial port using pyserial to communicate with arduino.
    Check if the port is correct or not. If not the programs exits.

    args:
        port: str
            The port at which your arduino is connected
            NOTE: For windows check your port in your device manager
        baudrate: int = 9600
            The speed at which communication is going to happen

    '''
    global ser
    try:
        ser = serial.Serial(port, baudrate=baudrate, timeout=SERIAL_TIMEOUT)
        print(
            f"[info] Serial port opened \nPORT: {port}\nBaud rate: {baudrate}\n\n")
    except SerialException as e:
        print("[Error] "+e.strerror)
        sys.exit()


def captureSerialData() -> str:
    '''
    This functions does the following
    1.Read data from serial port.
    2.Decode serial data as Ascii.
    3.return the serial data as string
    '''

    serial_data = ser.readline(-1)
    serial_data = serial_data.decode('UTF-8')
    return serial_data




if __name__ == "__main__":
    init_serial_port(port=SERIAL_PORT,baudrate=BAUD_RATE)
    while True:
        serial_data = captureSerialData()
        print(serial_data, end='\r')
        ser.flush()
        
