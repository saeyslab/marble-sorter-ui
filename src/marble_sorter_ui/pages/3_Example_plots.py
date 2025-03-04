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

names = ["B-cell-ALL", "T-cell-ALL", "AML"]
celltypes = ['rood', 'groen', 'blauw']
abundance = 1.5
probabilities_diseased = numpy.asarray([
        [1, abundance, 1],  # Too many B cells: B-cell-ALL
        [1, 1, abundance],  # Too many T cells: T-cell-ALL
        [abundance, 1, 1],  # Not enough white blood cells in general: AML
    ], dtype=float)
probabilities_diseased /= probabilities_diseased.sum(axis=1)[..., numpy.newaxis]
rng = numpy.random.default_rng(number)

# Healthy plots contain EXACTLY 5 cells of each type
streamlit.subheader("Healthy")
for i in range(n_plots):
    sample = numpy.array(celltypes * 5)
    rng.shuffle(sample)
    sample_to_plot(sample, order = streamlit.session_state.order)

for i, probability in enumerate(probabilities_diseased):
        streamlit.subheader(names[i])
        for j in range(n_plots):
            # Make sure that the cell abundant cell type indeed has strictly more occurrences
            # than all other cell types
            sample_ok = False
            while not sample_ok:
                sample = rng.choice(celltypes, 
                                    size = n_cells, 
                                    p = probability)
                abundant_type = celltypes[numpy.argmax(probability)]
                counts = dict(zip(*numpy.unique(sample, return_counts=True)))
                other_types = [t for t in celltypes if t is not abundant_type and t in counts.keys()]
                sample_ok = all([counts[abundant_type] > counts[other_type] for other_type in other_types])

            sample_to_plot(sample, order = streamlit.session_state.order)
