from typing import List
import streamlit
import pandas
import numpy
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.pyplot as plt
from marble_sorter_ui.common import *
from marble_sorter_ui.marble import Marble

maps = [
    LinearSegmentedColormap.from_list("red", [(0.3,0.3,0.3,1), (1.0,0,0,1)]),
    LinearSegmentedColormap.from_list("green", [(0.3,0.3,0.3,1), (0,1.0,0,1)]),
    LinearSegmentedColormap.from_list("blue", [(0.3,0.3,0.3,1), (0,0,1.0,1)])
]
w = 30


def train_one() -> None:
    """Runs training loop for one marble"""

    # Read rgb value from marble
    rgb = read_marble(ser)

    if rgb is None:
        return

    streamlit.session_state.marbles.append(Marble(streamlit.session_state.input, *rgb))

    # Updates center of color in training state
    color = streamlit.session_state.input
    state = streamlit.session_state.training_state
    state[color] = (state[color] + (numpy.asarray(rgb) / 255)) / 2


def state_to_color() -> numpy.ndarray:
    """Convert training state to color grid"""

    state = streamlit.session_state.training_state
    arr = numpy.empty(shape=(90, 90, 4), dtype=float)
    for c, i in zip(state.keys(), range(3)):
        for j in range(3):
            arr[i*w:(i+1)*w, j*w:(j+1)*w] = maps[j](state[c][j])

    return arr


# Page setup
streamlit.set_page_config(
    page_title="Training",
    page_icon="🚂"
)

# State setup
if "marbles" not in streamlit.session_state:
    streamlit.session_state["marbles"] = []
if "training_state" not in streamlit.session_state:
    streamlit.session_state["training_state"] = {
        "rood": numpy.array([0, 0, 0]),
        "groen": numpy.array([0, 0, 0]),
        "blauw": numpy.array([0, 0, 0])
    }

# Serial connection to sorter
if "ser" not in streamlit.session_state:
    config = get_config("sorter_config.yml")
    ser = get_connection(config["serial_port"])
else:
    ser = streamlit.session_state.ser

# Page layout

streamlit.title("Training")

with streamlit.form("form"):
    streamlit.selectbox(label="Knikker", options=["rood", "groen", "blauw"], key="input")
    streamlit.form_submit_button("Train", on_click=train_one)

streamlit.subheader("Getrainde knikkers")
df = marbles_to_df(streamlit.session_state.marbles)
streamlit.bar_chart(df.color.value_counts())

streamlit.subheader("Training state")
fig, ax = plt.subplots()
ax.imshow(state_to_color())
ax.set_axis_off()
streamlit.pyplot(fig)
streamlit.write(streamlit.session_state.training_state)
