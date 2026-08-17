# Rubber Duck Clock

A small desktop clock written in Python using Tkinter.

The application displays the current time and date inside a simple rubber duck widget that sits on your desktop. It synchronizes with public NTP servers to keep the displayed time accurate, can be dragged anywhere on the screen.

---

## Features

- Accuratly Displays the current time and date
- Custom menu with customization settings.
- Cute animations and lots of hats to collect
- Lightweight and simple

---

## Screenshot

> *Screenshot coming soon.*

---

## Requirements

- Python 3.13.x
- Windows


## Installation

Clone the repository

Install the following dependencies:

pygame
pillow
ntplib
pystray
tzdata
tzlocal

```bash
pip install pygame pillow ntplib pystray tzdata
py -m pip install pygame pillow ntplib pystray tzdata tzlocal
python -m pip install pygame pillow ntplib pystray tzdata tzlocal
```

Run the application:

```bash
python main.py
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

## Future Improvements

Some ideas I'd like to add in the future:

- More animated events like happy, loving, and more..
- link with google agenda - show notifications for meetings etc

- hat packages -> get a random hat ever 30m with different rarities (common, uncommon, rare, ulra rare, legendary) (maybe also have a timer somewhere)
- new hat drop -> bubble forms with a unknown hat icon in it -> user clicks bubble (bubble pop animation plays) new hat is given
- exchange -> sacrifice x amount of hats of same rarity to get a new hat from a higher rarity

- automatically detect seasons like Christmas' new year, Easter etc and have special events happen based on this (snow with Christmas, or special event related hats)

---

## License

This project is licensed under the MIT License.
