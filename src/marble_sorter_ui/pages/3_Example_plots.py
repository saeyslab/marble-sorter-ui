import numpy
from common import *

streamlit.set_page_config(
    page_title="Example plots"
)

def order_count():
    streamlit.session_state.order = "count"

def order_time():
    streamlit.session_state.order = "time"

if "order" not in streamlit.session_state:
    streamlit.session_state.order = "time"

with streamlit.sidebar:
      streamlit.button(label="Order by count", on_click=order_count)
      streamlit.button(label="Order by time", on_click=order_time)
      number = streamlit.number_input('Seed', value = 1)


n_plots = 10
n_cells = 15

names = ["healthy", "diseased"]
probabilities = numpy.asarray([
        [1, 1, 1],
        [1, .1, .1]
    ])
probabilities /= probabilities.sum(axis=1)[..., numpy.newaxis]

rng = numpy.random.default_rng(number)
for i, probability in enumerate(probabilities):
        for j in range(n_plots):
            sample = rng.choice(['rood', 'groen', 'blauw'], 
                                size = n_cells, 
                                p = probability)
            sample_to_plot(sample, order = streamlit.session_state.order)