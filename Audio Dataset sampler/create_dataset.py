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
        "--serialport", "-sp",
        type=str,
        required=True,
        help="Serial Port of arduino"
    )

    parser.add_argument(
        "--baudrate", "-b",
        type=str,
        required=False,
        help="Baudrate of Serial communication",
        default=9600
    )

    parser.add_argument(
        "--dsize", "-ds",
        type=int,
        required=False,
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


def init_serial_port(port: str, baudrate: int = 9600):
    global ser
    try:
        ser = serial.Serial(port, baudrate=baudrate, timeout=SERIAL_TIMEOUT)
        print(
            f"[info] Serial port opened \nPORT: {port}\nBaud rate: {baudrate}\n\n")
    except SerialException as e:
        print(e.strerror)
        sys.exit()


def save_numpy_array(arr: np.ndarray, filename: str):
    '''
    saves the numpy array in .npy binary file
    '''
    try:
        np.save(f"{DATASET_PATH}{filename}", arr=arr)
        print(f"[info] Data saved at {DATASET_PATH}{filename}.npy")
    except:
        print("Cannot save the numpy array")


def captureSerialData() -> np.ndarray:
    '''
    This functions does the following
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
    '''
    Creates numpy dataset by appending each captured audio FFT data in python list.
    Converting that python list to numpy array.
    Finally saving numpy array as .npy bin file to use later

    args:
        class_label : str
            Label name(i.e class name) of data
        number_of_data_instancce : int = 100
            Number of data points to capture for given label
        dataset : list = []
            An epmty python list where data is appended
    '''
    print(
        f"=============Capturing Audio FFT data=========\n \
        [info] NUMBER OF SAMPLE: {number_of_data_instance}\n \
        [info] LABEL: {class_label}\n\n"
    )
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

    # Initialize argparser
    args = init_argparser()

    if not os.path.exists(DATASET_PATH):
        os.mkdir(DATASET_PATH)

    #initialize serial communication
    init_serial_port(port=args.serialport, baudrate=args.baudrate)

    createDataset(
        class_label=args.label,
        number_of_data_instance=args.dsize
    )
