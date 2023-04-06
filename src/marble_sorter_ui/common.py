import serial
from serial import SerialException

import yaml
import time
import pandas
import numpy
import streamlit
from typing import List
import matplotlib.colors

from serial_stub import SerialStub

colors = {
    "rood": "#EC5B60",
    "groen": "#41B4A1",
    "blauw": "#456990"
}
custom_cmap = matplotlib.colors.ListedColormap(
    colors=colors.values(), N=len(colors)
)

bucket_map = {
    "blauw": 1,
    "rood": 2,
    "groen": 5,
    "leeg": -1
}

default_mean_RGB_df = pandas.DataFrame(
    [
        {'R': 118.2, 'G': 67., 'B': 59.},
        {'R': 87.6, 'G': 85, 'B': 66.},
        {'R': 76.5, 'G': 83.75, 'B': 80.75},
        {'R' : 93., 'G' : 79., 'B' : 66.25}
    ],
    index=['rood', 'groen', 'blauw', 'leeg']
)


def get_config(path):
    with open(path, "r") as fh:
        return yaml.load(fh, Loader=yaml.Loader)


def get_connection(serial_port):
    try: ser = serial.Serial(serial_port, 9600)
    except SerialException:
        ser = SerialStub(serial_port)
        print('No connection to real device, using SerialStub instead')
    return ser

# def get_connection(serial_port):
#     return serial.Serial(serial_port, 9600)


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
        try:
            RGB = [float(i) for i in rgb_raw.split(',')]
        except ValueError:
            return None

    return numpy.asarray(RGB)


def eject(ser):
    time.sleep(.5)
    ser.write(str.encode('e'))


def select_bucket(ser, bucket=1):
    ser.write(str.encode(str(bucket)))


def read_marble(ser, do_eject=True):

    # clear in/out buffers
    ser.flushInput()
    ser.flushOutput()

    load(ser)
    time.sleep(1)
    rgb = get_RGB(ser)

    if do_eject and (rgb is not None):
        time.sleep(.5)
        eject(ser)

    return rgb


def marbles_to_df(marbles: List) -> pandas.DataFrame:
    """Converts list of marbles to dataframe of marbles"""

    marbles_df = pandas.DataFrame(columns=['color','R','G','B'])
    for marble in marbles:
        color = marble.get_color()
        R = marble.get_red()
        G = marble.get_green()
        B = marble.get_blue()
        df = pandas.DataFrame([{'color' : color, 'R' : R, 'G' : G, 'B' : B}])
        marbles_df = pandas.concat([marbles_df, df], axis=0, ignore_index=True)

    return marbles_df


url_dict = {'rood' : 'app/static/red_macrophage.png',
            'groen' : 'app/static/green_Bcell_v2.png',
            'blauw' : 'app/static/blue_Tcell_v2.png'}

def sample_to_plot(sample, order = "count"):

    if order == "count":
        sample = numpy.sort(sample) # Sort not working?
        count = (list(range((sample == 'blauw').sum())) + 
                  list(range((sample == 'groen').sum())) + 
                  list(range((sample == 'rood').sum())))    
    elif order == "time":
        count = range(len(sample))
    
    count = [x+1 for x in count]
    urls = [url_dict[col] for col in sample]
    
    chart_data = pandas.DataFrame({'color': sample,
                                   'count': count,
                                   'img': urls})
    streamlit.vega_lite_chart(chart_data, 
                              {'height' : 400,
                               'width' : 500,
                               'mark': {'type': 'image', 'width': 100, 'height': 100},
                               'encoding': {
                                  'x': {'field': 'count', 'type': 'quantitative',
                                        'scale': {'domain': [1, 15]}},
                                  'y': {'field': 'color', 'type': 'ordinal',
                                        'scale': {'domain': ["rood", "groen", "blauw"]}},
                                  'url': {'field': 'img', 'type': 'nominal'},
                                },
                              })
