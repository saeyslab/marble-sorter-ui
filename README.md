# Marble sorter UI

Streamlit app providing an interactive interface to the marble sorter.

## Installation

```
git clone git@github.com:saeyslab/marble-sorter-ui.git
cd marble-sorter-ui
conda env create -f environment.yml
conda activate sorter
pip install .
```

## Usage

Connect the sorter and fill in the serial port in [sorter_config.yml](sort_config.yml)

To start the app, run:
```
conda activate sorter
streamlit run src/marble_sorter_ui/Welcome.py
```

Be aware that any time when starting or stopping the streamlit connection, the sorter will flush out all marbles!
If you have multiple screens open, the serial port will give an access denied error. Make sure to close everything and try again.
