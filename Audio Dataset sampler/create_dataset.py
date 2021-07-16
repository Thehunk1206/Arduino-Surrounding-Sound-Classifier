'''
Python script to read data from serial port and write to numpy array

This script is use to create Audio FFT dataset with arduino nano ble sense.

TODO: Automatically detect arduino port
'''

import serial
from serial.serialutil import SerialException

import sys
import os
import time
import argparse

import numpy as np
import pandas as pd

SERIAL_TIMEOUT = 4
DATASET_PATH = "Dataset/"

'''
Writing captured data into csv using pandas
'''
AUDIO_FFT_DATA_DICT = {
    "audio_spectrum_vec": [],
    "target": []
}

DESCRIPTION = """A python Script to create Audio FFT dataset using Arduino nana BLE sense.
                Capture the audio from on board Microphone of Arduino nano BLE sense, convert
                the raw audio from time domain to frequency domain using arduinoFFT"""


def init_argparser() -> argparse.Namespace:
    '''
    Initialize argparser to take arguments from command line
    '''

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


# ===========util func==========================
def clear_audio_dict():
    '''
    clear the dataframe dict before writing new captured data 
    to avoid duplicates and repetition of data in csv
    '''
    AUDIO_FFT_DATA_DICT["audio_spectrum_vec"].clear()
    AUDIO_FFT_DATA_DICT["target"].clear()


def write_to_csv(captured_data: str, class_label: str) -> bool:
    clear_audio_dict()
    AUDIO_FFT_DATA_DICT["audio_spectrum_vec"].append(captured_data)
    AUDIO_FFT_DATA_DICT["target"].append(class_label)
    df = pd.DataFrame(AUDIO_FFT_DATA_DICT)

    try:
        with open(f"{DATASET_PATH}/surrounding_audio_dataset_FFT.csv", 'a') as f:
            df.to_csv(f, header=f.tell() == 0)
            return True
    except:
        return False


def captureSerialData() -> str:
    '''
    This functions does the following
    1.Read data from serial port.
    2.Decode serial data as Ascii.
    3.return the serial data as string
    '''

    audio_data_str = ser.readline()
    audio_data_str = audio_data_str.decode('Ascii')
    audio_data_str = audio_data_str[1:len(audio_data_str)-6]
    return audio_data_str


def createDataset(class_label: str, number_of_data_instance: int = 100):
    '''
    Creates numpy dataset by appending each captured audio FFT data in python list.
    Converting that python list to numpy array.
    Finally saving numpy array as .npy bin file to use later

    args:
        class_label : str
            Label name(i.e class name) of data
        number_of_data_instancce : int = 100
            Number of data points to capture for given label
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
            f"[info]Capttured Sample no: {i+1} \nData shape {len(np_audio_data)}")

        has_wrtitten_to_csv = write_to_csv(
            captured_data=np_audio_data, class_label=class_label)

        if has_wrtitten_to_csv:
            print(
                f"[info] Captured audio FFT written to csv => {DATASET_PATH}/surrounding_audio_dataset_FFT.csv\n")
        else:
            print("[Error] Something went wrong while writting data to csv file")
            sys.exit()

        time.sleep(0.5)
    ser.close()


if __name__ == "__main__":

    # Initialize argparser
    args = init_argparser()

    if not os.path.exists(DATASET_PATH):
        os.mkdir(DATASET_PATH)

    # initialize serial communication
    init_serial_port(port=args.serialport, baudrate=args.baudrate)

    # start capturing Audio FFT(Fast fourier transform) data
    createDataset(
        class_label=args.label,
        number_of_data_instance=args.dsize
    )
