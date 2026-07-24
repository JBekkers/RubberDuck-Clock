from Source.Config.constants import CENTER_X, CENTER_Y
from Source.Window_Manager import root, canvas
from Source.animation import play_animation, is_idle

from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo
import time
import ntplib

TIMEZONE = ZoneInfo("Europe/Amsterdam") 
SYNC_INTERVAL = 60   
CLOCK_Y_OFFSET = 30

last_hour_quacked = None
network_time = None
sync_monotonic = None

NTP_SERVERS = [
    "time.cloudflare.com",
    "time.google.com",
    "time.windows.com",
    "time.apple.com",
    "pool.ntp.org",
]

settings = {}
time_display = None
date_display = None

def start_clock(clock_settings):
    global settings
    settings = clock_settings

    synchronize_time()
    update_clock_display()

def setup_clock():
    global time_display, date_display

    time_display = canvas.create_text(
        CENTER_X,
        CENTER_Y + CLOCK_Y_OFFSET - 10,
        text="--:--",
        font=("Segoe UI", 11, "bold"),
        fill="black",
        anchor="center"
    )

    date_display = canvas.create_text(
        CENTER_X,
        CENTER_Y + CLOCK_Y_OFFSET + 10,
        text="--/--",
        font=("Segoe UI", 8),
        fill="black",
        anchor="center"
    )

def synchronize_time():

    global network_time, sync_monotonic

    try:
        client = ntplib.NTPClient()

        for server in NTP_SERVERS:
            try:
                response = client.request(server, version=3, timeout=3)
                break
            except Exception:
                response = None

        if response is None:
            raise Exception("All NTP servers failed.")

        utc_now = datetime.fromtimestamp(
        response.tx_time,
        tz=timezone.utc
        )

        network_time = utc_now.astimezone(TIMEZONE)

        sync_monotonic = time.monotonic()

    except Exception:
        pass

    root.after(SYNC_INTERVAL * 1000, synchronize_time)


def update_clock_display():

    if network_time is not None:

        elapsed = time.monotonic() - sync_monotonic

        current_time = network_time + timedelta(seconds=elapsed)

        global last_hour_quacked

        if (
            settings["hourly_quack"] and
            current_time.minute == 0 and
            is_idle() and
            last_hour_quacked != current_time.hour
        ):
            last_hour_quacked = current_time.hour
            play_animation("Quack")


        elif current_time.minute != 0:
            last_hour_quacked = None



        canvas.itemconfig(
            time_display,
            text=current_time.strftime("%H:%M")
        )

        canvas.itemconfig(
            date_display,
            text=current_time.strftime("%d-%m-%Y")
        )

    else:

        canvas.itemconfig(
            time_display,
            text="Offline"
        )

        canvas.itemconfig(
            date_display,
            text=""
        )
    root.after(200, update_clock_display)
