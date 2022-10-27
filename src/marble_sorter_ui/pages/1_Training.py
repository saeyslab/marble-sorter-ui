import streamlit
import pandas
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


def train_one():
    rgb = read_marble(ser)
    streamlit.session_state.marbles.append(
        Marble(streamlit.session_state.input, *rgb)
    )


streamlit.set_page_config(
    page_title="Training",
    page_icon="🚂"
)
streamlit.title("Training")

if "marbles" not in streamlit.session_state:
    streamlit.session_state["marbles"] = []

config = get_config("sorter_config.yml")
ser = get_connection(config["serial_port"])

streamlit.text_input(label="Knikker kleur", value="kleur", key="input", on_change=train_one)

streamlit.subheader("Getrainde knikkers")
df = marbles_to_df(streamlit.session_state.marbles)
streamlit.bar_chart(df.color.value_counts())
