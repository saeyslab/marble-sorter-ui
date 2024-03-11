import streamlit
from common import *
import numpy
from scipy.spatial.distance import cosine
import seaborn
import matplotlib.pyplot as plt


def continue_sort():
    streamlit.session_state.sort = True

def set_centers():
    sorter = streamlit.session_state["sorter"]
    streamlit.session_state.centers = centers_dfs[sorter]
    print("Setting sorter:")
    print(sorter)
    print(streamlit.session_state.centers)

def start_sort():
    streamlit.session_state.tubes.append([])
    continue_sort()

def stop_sort():
    streamlit.session_state.sort = False

def clear_tubes():
    streamlit.session_state.tubes = []

def sort(rgb):
    centers = streamlit.session_state.centers
    # dists = numpy.linalg.norm(rgb-centers, axis=1)
    dists = numpy.array([cosine(rgb, centers.values[i]) for i in range(4)])
    color = centers.iloc[dists.argmin()].name
    return bucket_map[color], color

def position_red():
    select_bucket(streamlit.session_state.ser, bucket=bucket_map["rood"])
def position_green():
    select_bucket(streamlit.session_state.ser, bucket=bucket_map["groen"])
def position_blue():
    select_bucket(streamlit.session_state.ser, bucket=bucket_map["blauw"])


def order_count():
    streamlit.session_state.order = "count"
def order_time():
    streamlit.session_state.order = "time"

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
    streamlit.session_state.centers = centers_dfs["Sorter 1"]
if "tubes" not in streamlit.session_state:
    clear_tubes()
if "empty_tries" not in streamlit.session_state:
    streamlit.session_state.empty_tries = 0

config = get_config("sorter_config.yml")

# Setup serial connection to sorter
if "ser" not in streamlit.session_state:
    ser = get_connection(config["serial_port"])
    streamlit.session_state.ser = ser
else:
    ser = streamlit.session_state.ser

if "sort" not in streamlit.session_state:
    streamlit.session_state.sort = False

if "order" not in streamlit.session_state:
    streamlit.session_state.order = "time"


# Page layout
streamlit.title("Tubes")

with streamlit.sidebar:
    col1, col2 = streamlit.columns([1,1])
    with col1:
        streamlit.button(label="Start new tube", on_click=start_sort)
        streamlit.button(label="Stop sorting", on_click=stop_sort)
        streamlit.button(label="Order by count", on_click=order_count)
    with col2:
        streamlit.button(label="Continue tube", on_click=continue_sort)
        streamlit.button(label="Clear tubes", on_click=clear_tubes)
        streamlit.button(label="Order by time", on_click=order_time)

    col1, col2, col3 = streamlit.columns([1,1,1])
    with col1:
        streamlit.button(label="Position Red", on_click=position_red)
    with col2:
        streamlit.button(label="Position Green", on_click=position_green)
    with col3:
        streamlit.button(label="Position Blue", on_click=position_blue)

    streamlit.selectbox(label="Sorter", options=["Sorter 1", "Sorter 2"], on_change=set_centers, key="sorter")

if len(streamlit.session_state.tubes) > 0:
    for i, tube in enumerate(streamlit.session_state.tubes):
        if(len(tube) > 0):
            sample_to_plot(tube, order = streamlit.session_state.order)

# Sort loop
if streamlit.session_state.sort:
    rgb = read_marble(ser, do_eject=False)

    streamlit.sidebar.text(str(rgb))

    if rgb is not None:
        bucket, color = sort(rgb)
        streamlit.sidebar.text(color)

        if bucket < 0:
            streamlit.session_state.empty_tries += 1

            if streamlit.session_state.empty_tries >= config["empty_tries"]:
                stop_sort()
            else:
                streamlit.rerun()
        else:
            streamlit.session_state.empty_tries = 0
            streamlit.sidebar.text(len(streamlit.session_state.tubes))
            streamlit.session_state.tubes[-1].append(color)
            select_bucket(ser, bucket=bucket)
            eject(ser)
            streamlit.rerun()
    else:
        streamlit.rerun()
