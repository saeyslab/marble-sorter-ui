import streamlit
from marble_sorter_ui.common import *
import numpy


def start_sort():
    streamlit.session_state.sort = True

def stop_sort():
    streamlit.session_state.sort = False

def sort(rgb):
    centers = streamlit.session_state.centers
    dists = numpy.linalg.norm(rgb-centers, axis=1)
    color = centers.iloc[dists.argmin()].name
    return bucket_map[color], color

# Setup page
streamlit.set_page_config(
    page_title="Sorting!",
    page_icon="🧮"
)

# Setup state
if ("marbles" in streamlit.session_state) and ("centers" not in streamlit.session_state):
    marbles_df = marbles_to_df(streamlit.session_state.marbles)
    streamlit.session_state.centers = marbles_df.groupby("color").mean()
if ("marbles" not in streamlit.session_state) and ("centers" not in streamlit.session_state):
    streamlit.session_state.centers = default_mean_RGB_df

# Setup serial connection to sorter
if "ser" not in streamlit.session_state:
    config = get_config("sorter_config.yml")
    ser = get_connection(config["serial_port"])
else:
    ser = streamlit.session_state.ser

if "sort" not in streamlit.session_state:
    streamlit.session_state.sort = False

# Page layout

streamlit.title("Sorteren")

streamlit.button(label="Start", on_click=start_sort)
streamlit.button(label="Stop", on_click=stop_sort)

# Sort loop
if streamlit.session_state.sort:
    rgb = read_marble(ser, do_eject=False)

    if rgb is not None:
        if empty(rgb):
            streamlit.session_state.sort = False
        else:
            bucket, color = sort(rgb)
            select_bucket(ser, bucket=bucket)
            eject(ser)
            streamlit.experimental_rerun()
    else:
        streamlit.experimental_rerun()
