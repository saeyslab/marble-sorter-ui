import serial
import yaml
import time


def get_config(path):
    with open(path, "r") as fh:
        return yaml.load(fh, Loader=yaml.Loader)


def get_connection(serial_port):
    return serial.Serial(serial_port, 9600, timeout=1)


def load(ser):
    ser.write(str.encode('l'))


def get_RGB(ser):
    rgb_raw = ''
    while len(rgb_raw) < 3:
        ser.write(str.encode('p'))
        # Reading all available bytes till EOL
        rgb_raw = str(ser.readline())
        # Cleaning up the string
        rgb_raw = rgb_raw.replace('b\'','')
        rgb_raw = rgb_raw.replace('\\r\\n\'','')
        # Conversion to list with R,G,B values
        RGB = rgb_raw.split(',')

    return RGB


def eject(ser):
    ser.write(str.encode('e'))


def select_bucket(ser, bucket=1):
    ser.write(str.encode(str(bucket)))


def read_marble(ser):

    # clear in/out buffers
    ser.flushInput()
    ser.flushOutput()

    load(ser)
    time.sleep(.5)
    rgb = get_RGB(ser)
    time.sleep(.5)
    eject(ser)

    return rgb


def empty(rgb):
    if 92 <= int(rgb[0]) <= 95:
        if 78 <= int(rgb[1]) <= 80:
            if 65 <= int(rgb[2]) <=67:
                return True
