'''
Python script to read data from serial port and write to numpy array

This script is use to create Audio FFT dataset with arduino nano ble sense.

TODO: Automatically detect arduino port
TODO: Handle SerialException wile reading data. In case the device disconnect while reading, the numpy should save
'''

import serial
from serial.serialutil import SerialException

import sys
import os
import time
import argparse

import numpy as np


# NOTE serial port here is for linux machine, do check out for windows and MAC
PORT = '/dev/ttyACM0'
BAUD_RATE = 115200
SERIAL_TIMEOUT = 4
DATASET_PATH = "Dataset/"

DESCRIPTION = """A python Script to create Audio FFT dataset using Arduino nana BLE sense.
                Capture the audio from on board Microphone of Arduino nano BLE sense, convert
                the raw audio from time domain to frequency domain using arduinoFFT"""


def init_argparser() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=DESCRIPTION,
    )

    parser.add_argument(
        "--dsize", "-ds",
        type=int,
        required=True,
        help="Audio FFT dataset size",
        default=100
    )

    parser.add_argument(
        "--label", "-l",
        type=str,
        required=True,
        help="label for Audio data"
    )

    args = parser.parse_args()

    return args


def init_serial_port():
    global ser
    try:
        ser = serial.Serial(PORT, baudrate=BAUD_RATE, timeout=SERIAL_TIMEOUT)
    except SerialException as e:
        print(e.strerror)
        sys.exit()


def save_numpy_array(arr: np.ndarray, filename: str):
    try:
        np.save(f"{DATASET_PATH}{filename}", arr=arr)
        print(f"[info] Data saved at {DATASET_PATH}{filename}.npy")
    except:
        print("Cannot save the numpy array")


def captureSerialData() -> np.ndarray:
    '''
    The functions does the following
    1.Read data from serial port.
    2.Decode serial data as Ascii.
    3.Create list of string data points by split() with Deliminator as ','.
    4.Convert to numpy array and return as float numpy array
    '''

    audio_data_str = ser.readline()
    audio_data_str = audio_data_str.decode('Ascii')
    audio_data_str = audio_data_str[1:len(audio_data_str)-6]
    audio_data_str = audio_data_str.split(",")
    audio_data_np = np.array([audio_data_str])
    audio_data_np = audio_data_np.astype(np.float)

    return audio_data_np


def createDataset(
    class_label: str,
    number_of_data_instance: int = 100,
    dataset: list = []
):

    for i in range(number_of_data_instance):
        ser.write(b'1')
        np_audio_data = captureSerialData()
        print(
            f"[info]Capttured Sample no: {i+1} \nData shape {np_audio_data.shape}\n")
        dataset.append(np_audio_data)
        time.sleep(0.5)
    ser.close()
    dataset_np = np.array(dataset)
    save_numpy_array(dataset_np, class_label)


if __name__ == "__main__":

    args = init_argparser()

    if not os.path.exists(DATASET_PATH):
        os.mkdir(DATASET_PATH)

    init_serial_port()

    createDataset(
        class_label=args.label,
        number_of_data_instance=args.dsize
    )
