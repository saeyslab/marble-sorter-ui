# Marble sorter UI

Streamlit app providing an interactive interface to the marble sorter.

## Installation

```
git clone git@github.com:saeyslab/marble-sorter-ui.git
cd marble-sorter-ui
conda env create -f environment.yml
pip install .
```

## Usage

Connect the sorter and fill in the serial port in [sorter_config.yml](sort_config.yml)

To start the app, run:
```
streamlit run src/marble_sorter_ui/Welcome.py
```
