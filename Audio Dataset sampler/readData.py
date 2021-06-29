'''
Python script to read data from serial port and write to numpy array

This script is use to create Audio FFT dataset with arduino nano ble sense.

'''
import serial
import time

ser = serial.Serial('/dev/ttyACM0', 115200,)


def captureAudio():
    audio_data = ser.readline()
    print(audio_data.decode('Ascii'))
    

if __name__ == "__main__":
    time.sleep(1)
    
    for _ in range(6):
        ser.write(b'1')
        captureAudio()
    ser.close()
