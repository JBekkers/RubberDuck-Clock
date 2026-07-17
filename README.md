# Rubber Duck Clock

A small desktop clock written in Python using Tkinter.

The application displays the current time and date inside a simple rubber duck widget that sits on your desktop. It synchronizes with public NTP servers to keep the displayed time accurate, can be dragged anywhere on the screen.

---

## Features

- Accuratly Displays the current time and date
- Always stays on top of other windows
- Cute animations and lots of hats to collect
- Lightweight and simple

---

## Screenshot

> *Screenshot coming soon.*

---

## Requirements

- Python 3.11 or newer
- Windows


## Installation

Clone the repository

Install the dependencies:

```bash
pip install pillow ntplib pystray
```

Run the application:

```bash
python main.py
```

---

## Project Structure

```text
RubberDuckClock/
├── ClockSkins/
│   └── duck.png
├── Icon.png
├── main.py
└── README.md
```

---

## Configuration

The following values can be changed directly

### Timezone

```python
TIMEZONE = ZoneInfo("Europe/Amsterdam")
```

### Synchronization interval

```python
SYNC_INTERVAL = 60
```

The value is measured in seconds.

### Window size

```python
WINDOW_WIDTH = 150
WINDOW_HEIGHT = 150
```

---

## Future Improvements

Some ideas I'd like to add in the future:

- Support for different hats
- lootpackage to get a random hat ever 30m
- Animated events like sleeping, happy, loving, and more..
- duck slowly turn red and gets mad then cool down back to yellow again
- Menu when clicking on the clock instead of in tray icon
- link with google agenda - show notifications for meetings etc

---

## License

This project is licensed under the MIT License.
