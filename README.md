# Rubber Duck Clock

A small desktop clock written in Python using Tkinter.

The application displays the current time and date inside a simple rubber duck widget that sits on your desktop. It synchronizes with public NTP servers to keep the displayed time accurate, can be dragged anywhere on the screen, and runs quietly in the system tray.

---

## Features

- Displays the current time and date
- Synchronizes with multiple NTP servers for accurate time
- Always stays on top of other windows
- Draggable desktop widget
- System tray icon with a menu
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

- Save the window position between launches
- Support for different hats
- Animated events like sleeping, happy, idle and more..
- Quack sound every full hour
- Menu when clicking on the clock

---

## License

This project is licensed under the MIT License.
