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

### Linux-specific instructions

#### dialout group
Add your user to the `dialout` group:
```
sudo adduser [USER] dialout
```
where you replace `[USER]` with your username.

#### brltty
If you are on Ubuntu, a specific library called `brltty` might interfere with the serial connection.
This is a library for [refreshable braille displays](https://brltty.app/).
Assuming you don't need this, uninstall it:
```
sudo apt remove brltty
```

#### Finding the correct device
1. Run `dmesg -wH` to view kernel messages.
2. Plug in the sorter.
3. Check which device is used (should be something like `ttyUSB0`)
4. Fill in this device in `sorter_config.yml`

## Usage

Connect the sorter and fill in the serial port in [sorter_config.yml](sort_config.yml)

To start the app, run:
```
conda activate sorter
streamlit run src/marble_sorter_ui/Welcome.py
```

Be aware that any time when starting or stopping the streamlit connection, the sorter will flush out all marbles!
If you have multiple screens open, the serial port will give an access denied error. Make sure to close everything and try again.
