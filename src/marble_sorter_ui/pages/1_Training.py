from textwrap import fill
import streamlit
import pandas
import numpy
import seaborn
import matplotlib.pyplot as plt
from marble_sorter_ui.common import *
from marble_sorter_ui.marble import Marble


def marbles_to_df(marbles):
    marbles_df = pandas.DataFrame(columns=['color','R','G','B'])
    for marble in marbles:
        color = marble.get_color()
        R = marble.get_red()
        G = marble.get_green()
        B = marble.get_blue()
        df = pandas.DataFrame([{'color' : color, 'R' : R, 'G' : G, 'B' : B}])
        marbles_df = pandas.concat([marbles_df, df], axis=0, ignore_index=True)

    return marbles_df


def update_training_state(color, r, g, b):
    state = streamlit.session_state.training_state
    state[color] = (state[color] + numpy.asarray([r, g, b])) / 2


def train_one():
    rgb = read_marble(ser)
    streamlit.write(rgb)
    streamlit.session_state.marbles.append(Marble(streamlit.session_state.input, *rgb))
    update_training_state(streamlit.session_state.input, *rgb)


streamlit.set_page_config(
    page_title="Training",
    page_icon="🚂"
)
streamlit.title("Training")

if "marbles" not in streamlit.session_state:
    streamlit.session_state["marbles"] = []
if "training_state" not in streamlit.session_state:
    streamlit.session_state["training_state"] = {
        "rood": numpy.array([128, 128, 128]),
        "groen": numpy.array([128, 128, 128]),
        "blauw": numpy.array([128, 128, 128])
    }

if "ser" not in streamlit.session_state:
    config = get_config("sorter_config.yml")
    ser = get_connection(config["serial_port"])
else:
    ser = streamlit.session_state.ser

with streamlit.form("form"):
    streamlit.text_input(label="Knikker kleur", value="kleur", key="input")
    streamlit.form_submit_button("Train", on_click=train_one)

streamlit.subheader("Getrainde knikkers")
df = marbles_to_df(streamlit.session_state.marbles)
streamlit.bar_chart(df.color.value_counts())

streamlit.subheader("Training state")

fig, ax = plt.subplots()
seaborn.heatmap(
    data=pandas.DataFrame(
        streamlit.session_state.training_state,
        index=["R", "G", "B"],
    ).T,
    vmin=0,
    vmax=255
)
streamlit.pyplot(fig)
streamlit.write(streamlit.session_state.training_state)
