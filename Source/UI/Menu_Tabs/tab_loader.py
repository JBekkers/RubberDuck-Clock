import tkinter as tk
from Source.Config import style
from Source.Window_Manager import set_menu_window, set_menu_callback

from Source.UI.Menu_Tabs.cosmetics_tab import build_cosmetics_tab
from Source.UI.Menu_Tabs.settings_tab import build_settings_tab
from Source.UI.Menu_Tabs.about_tab import build_about_tab
from Source.UI.Menu_Tabs.exchange_tab import build_exchange_tab

window = None
window_width = 400

def close_menu():
    global window

    if window is None:
        return

    if window.winfo_exists():
        window.destroy()

    window = None
    set_menu_window(None)

def open_settings(root, settings, config, actions):

    global window

    if window is not None and window.winfo_exists():
        close_menu()
        return

    window = tk.Toplevel(root)
    set_menu_window(window)
    window.overrideredirect(True)
    window.configure(bg=style.BACKGROUND)

    window.attributes("-topmost", True)
    window.lift()

    window.option_add("*Background", style.BACKGROUND)
    window.option_add("*Foreground", style.TEXT_COLOR)

    window.option_add("*Checkbutton.ActiveBackground", style.BACKGROUND)
    window.option_add("*Button.Background", style.BUTTON_NORMAL)
    window.option_add("*Button.Foreground", style.TEXT_COLOR)
    window.option_add("*Button.ActiveBackground", style.BUTTON_CLICKED)
    window.option_add("*Button.ActiveForeground", style.TEXT_COLOR)
    window.option_add("*Button.HighlightThickness", 0)

    position_menu(root)

    window.resizable(False, False)

    background = tk.Frame(
        window,
        bg=style.BACKGROUND
    )

    background.place(
        x=0,
        y=0,
        relwidth=1,
        relheight=1
    )

    background.lower()

    tab_bar = tk.Frame(window)
    tab_bar.pack(fill="x")

    content = tk.Frame(window)
    content.pack(
        fill="both",
        expand=True,
        padx=5,
        pady=5
    )

    tabs = [
        ("Cosmetics", build_cosmetics_tab),
        ("Exchange", build_exchange_tab),
        ("Settings", build_settings_tab),
        ("About", build_about_tab),
    ]

    frames = []
    buttons =[]


    def show_tab(index):
        for i, frame in enumerate(frames):
            frame.pack_forget()
            buttons[i].config(bg=style.BUTTON_NORMAL)

        buttons[index].config(bg=style.BUTTON_SELECTED)

        frames[index].pack(
            fill="both",
            expand=True,
        )

    for index, (title, builder) in enumerate(tabs):

        tab_bar.columnconfigure(index, weight=1)

        button = tk.Button(
            tab_bar,
            text=title,
            command=lambda i=index: show_tab(i),
            relief="flat",
            font=style.TITLE_FONT,
            borderwidth=0,
            highlightthickness=0,
        )
        buttons.append(button)

        button.grid(
            row=0,
            column=index,
            sticky="ew",
        )

        frame = tk.Frame(content)
        frames.append(frame)

        if builder is build_settings_tab:
            builder(frame, settings, config, actions)
        else:
            builder(frame, settings, config)

    close_button = tk.Button(
        tab_bar,
        text="X",
        command=close_menu,
        relief="flat",
        bg="#CF5029",
        font=style.TITLE_FONT,
        borderwidth=0,
        highlightthickness=0,
    )

    close_button.grid(
        row=0,
        column=len(tabs),
        sticky="ew",
    )

    show_tab(0)

def position_menu(root):

    if window is None or not window.winfo_exists():
        return

    menu_width = window_width
    menu_height = 450

    duck_x = root.winfo_x()
    duck_y = root.winfo_y()

    duck_width = root.winfo_width()
    duck_height = root.winfo_height()

    screen_height = root.winfo_screenheight()

    menu_x = duck_x + (duck_width // 2) - (menu_width // 2)

    # Prefer below the duck
    menu_y = duck_y + duck_height

    # If it won't fit, place it above instead
    if menu_y + menu_height > screen_height:
        menu_y = duck_y - menu_height

    window.geometry(f"{menu_width}x{menu_height}+{menu_x}+{menu_y}")

set_menu_callback(position_menu)