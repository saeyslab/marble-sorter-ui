import streamlit
from marble_sorter_ui.common import *
import numpy
from scipy.spatial.distance import cosine
import seaborn
import matplotlib.pyplot as plt


def continue_sort():
    streamlit.session_state.sort = True

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
if "tubes" not in streamlit.session_state:
    clear_tubes()

config = get_config("sorter_config.yml")

# Setup serial connection to sorter
if "ser" not in streamlit.session_state:
    ser = get_connection(config["serial_port"])
else:
    ser = streamlit.session_state.ser

if "sort" not in streamlit.session_state:
    streamlit.session_state.sort = False

# Page layout
streamlit.title("Tubes")

with streamlit.sidebar:
    streamlit.button(label="Start new tube", on_click=start_sort)
    streamlit.button(label="Continue tube", on_click=continue_sort)
    streamlit.button(label="Stop sorting", on_click=stop_sort)
    streamlit.button(label="Clear tubes", on_click=clear_tubes)

    # col1, col2 = streamlit.columns(2)
    # with col1:
    #     streamlit.button(label="Start new tube", on_click=start_sort)
    #     streamlit.button(label="Continue tube", on_click=continue_sort)
    # with col2:
    #     streamlit.button(label="Stop sorting", on_click=stop_sort)
    #     streamlit.button(label="Clear tubes", on_click=clear_tubes)

if len(streamlit.session_state.tubes) > 0:

    dfs = []
    for i, tube in enumerate(streamlit.session_state.tubes):
        df = pandas.DataFrame(tube, columns=["Color"])
        df["Tube"] = i
        dfs.append(df)
    df = pandas.concat(dfs)
    df["Color"] = df["Color"].astype(
        pandas.CategoricalDtype(categories=["rood", "groen", "blauw"], ordered=True))

    if df.shape[0] > 0:
        grid = seaborn.FacetGrid(data=df, row="Tube", aspect=1.7, sharex=False)
        grid.map_dataframe(seaborn.countplot, x="Color", palette=colors.values())
        for ax in grid.axes.ravel():
            ax.set_ylim(0, config["per_tube"])
        streamlit.pyplot(grid.fig)

        # seaborn.countplot(data=df, x="Tube", hue="Color", palette=colors.values())
        # streamlit.pyplot(plt.gcf())

# Sort loop
if streamlit.session_state.sort:
    rgb = read_marble(ser, do_eject=False)

    streamlit.sidebar.text(str(rgb))

    if rgb is not None:
        bucket, color = sort(rgb)
        streamlit.sidebar.text(color)

        if bucket < 0:
            stop_sort()
        else:
            streamlit.sidebar.text(len(streamlit.session_state.tubes))
            streamlit.session_state.tubes[-1].append(color)
            select_bucket(ser, bucket=bucket)
            eject(ser)
            streamlit.experimental_rerun()
    else:
        streamlit.experimental_rerun()
