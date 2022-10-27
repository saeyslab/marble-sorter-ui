import streamlit
from marble_sorter_ui.common import *
import numpy
import pandas


def start_sort():
    streamlit.session_state.sort = True

def stop_sort():
    streamlit.session_state.sort = False

def sort(rgb):
    centers = streamlit.session_state.centers
    dists = numpy.linalg.norm(rgb-centers)
    mini = dists.argmin()

    return [5, 1, 2][mini], mini

# Setup page
streamlit.set_page_config(
    page_title="Sorting!",
    page_icon="🧮"
)

# Setup state
if ("marbles" in streamlit.session_state) and ("centers" not in streamlit.session_state):
    mean_RGB_df = pandas.DataFrame(columns=['color','R','G','B'])
    marbles_df = marbles_to_df(streamlit.session_state.marbles)
    list_of_colors = marbles_df['color'].unique()
    for color in list_of_colors:
        marble_class_df = marbles_df[marbles_df['color'] == color]
        a = marble_class_df.to_numpy()
        mean_RGB = numpy.mean(a[:,1:4].astype(float), axis=0)
        df = pandas.DataFrame(
            [{'color' : color, 'R' : mean_RGB[0], 'G' : mean_RGB[1], 'B' : mean_RGB[2]}])
        mean_RGB_df = pandas.concat([mean_RGB_df, df], axis=0, ignore_index=True)

    streamlit.session_state.centers = mean_RGB_df

# Setup serial connection to sorter
if "ser" not in streamlit.session_state:
    config = get_config("sorter_config.yml")
    ser = get_connection(config["serial_port"])
else:
    ser = streamlit.session_state.ser

# Sort loop
if streamlit.session_state.sort:
    rgb = read_marble(ser, eject=False)
    if empty(rgb):
        streamlit.session_state.sort = False
    else:
        bucket, index = sort(rgb)
        select_bucket(ser, bucket=bucket)
        eject(ser)

# Page layout

streamlit.title("Sorteren")

streamlit.button(label="Start", on_click=start_sort)
