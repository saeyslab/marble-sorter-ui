import numpy
from common import *

streamlit.set_page_config(
    page_title="Example plots"
)

n_plots = 10
n_cells = 15

names = ["healthy", "diseased"]
probabilities = numpy.asarray([
        [1, 1, 1],
        [1, .1, .1]
    ])
probabilities /= probabilities.sum(axis=1)[..., numpy.newaxis]

for i, probability in enumerate(probabilities):
        for j in range(n_plots):
            sample = numpy.random.choice(['rood', 'groen', 'blauw'], 
                                         size = n_cells, 
                                         p = probability)
            print(type(sample))
            sample_to_plot(sample)