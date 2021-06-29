'''
Python script to read data from serial port and write to numpy array

This script is use to create Audio FFT dataset with arduino nano ble sense.

TODO: Continously capture the data and concate in a numpy array.
TODO: Later serialize the data as .np file for training the model
'''
import serial
import time
import numpy as np

ser = serial.Serial('/dev/ttyACM0', 115200, timeout=4)


def captureAudio():
    audio_data_str = ser.readline()
    audio_data_str = audio_data_str.decode('Ascii')
    audio_data_str = audio_data_str[1:len(audio_data_str)-6]
    audio_data_str = audio_data_str.split(",")
    audio_data_np = np.array(audio_data_str)
    audio_data_np = audio_data_np.astype(np.float)
    audio_data_np = audio_data_np.reshape(1,-1)
    print(audio_data_np.shape)
    

if __name__ == "__main__":
    time.sleep(1)
    
    for _ in range(5):
        ser.write(b'1')
        captureAudio()
    ser.close()
