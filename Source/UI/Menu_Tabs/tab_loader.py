import tkinter as tk
from Source.Config import style
from Source.Window_Manager import set_menu_window, set_menu_callback

from Source.UI.Menu_Tabs.cosmetics_tab import build_cosmetics_tab
from Source.UI.Menu_Tabs.settings_tab import build_settings_tab
from Source.UI.Menu_Tabs.about_tab import build_about_tab
from Source.UI.Menu_Tabs.exchange_tab import build_exchange_tab

window = None

def close_menu():
    global window

    if window is None:
        return

    try:
        if window.winfo_exists():
            window.destroy()
    finally:
        window = None
        set_menu_window(None)

def open_settings(root,settings,config,stats,actions):

    global window

    if window is not None and window.winfo_exists():
        close_menu()
        return

    window = tk.Toplevel(root)

    window.protocol(
    "WM_DELETE_WINDOW",
    close_menu
    )

    set_menu_window(window)
    window.overrideredirect(True)
    window.configure(bg=style.BACKGROUND)

    window.attributes("-topmost",settings["always_on_top"])
    window.lift()

    window.option_add("*Background", style.BACKGROUND)
    window.option_add("*Foreground", style.TEXT_COLOR)

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

    tab_bar = tk.Frame(
        window,
        bg=style.BUTTON_NORMAL,
        height=style.MENU_HEADER_HEIGHT
    )
    tab_bar.pack_propagate(False)

    tab_bar.pack(fill="x")

    content = tk.Frame(
        window,
    )

    content.pack(
        fill="both",
        expand=True,
        padx=style.MENU_PADDING,
        pady=style.MENU_PADDING
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
            buttons[i].config(
                bg=style.BUTTON_NORMAL,
                relief="flat"
            )

        buttons[index].config(
            bg=style.BUTTON_SELECTED,
            relief="flat"
        )

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
            font=style.MENU_TAB_FONT,
            borderwidth=0,
            highlightthickness=0,
            bg=style.BUTTON_NORMAL,
            fg=style.TEXT_COLOR,
            activebackground=style.BUTTON_CLICKED,
            activeforeground=style.TEXT_COLOR,
            cursor="hand2",
            padx=style.MENU_TAB_PADDING_X,
            pady=style.MENU_TAB_PADDING_Y,
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
            builder(frame,settings,config,actions)
        elif builder is build_about_tab:
            builder(frame,settings,config,stats)
        else:
            builder(frame,settings,config)

    close_button = tk.Button(
        tab_bar,
        text="×",
        command=close_menu,
        relief="flat",
        bg=style.CLOSE_BUTTON,
        fg="#FFFFFF",
        activebackground=style.CLOSE_BUTTON_HOVER,
        activeforeground="#FFFFFF",
        font=("Segoe UI", 14, "bold"),
        borderwidth=0,
        highlightthickness=0,
        cursor="hand2",
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

    menu_width = style.MENU_WIDTH
    menu_height = style.MENU_HEIGHT

    duck_x = root.winfo_x()
    duck_y = root.winfo_y()

    duck_width = root.winfo_width()
    duck_height = root.winfo_height()

    screen_height = root.winfo_screenheight()

    menu_x = duck_x + (duck_width // 2) - (menu_width // 2)
    menu_y = duck_y + duck_height

    if menu_y + menu_height > screen_height:
        menu_y = duck_y - menu_height

    window.geometry(f"{menu_width}x{menu_height}+{menu_x}+{menu_y}")

set_menu_callback(position_menu)