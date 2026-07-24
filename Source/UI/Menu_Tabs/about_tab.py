import tkinter as tk


def build_about_tab(parent, settings, config):

    tk.Label(
        parent,
        text="About",
        font=("Segoe UI", 14, "bold")
    ).pack(pady=20)

    tk.Label(
        parent,
        text="Version 1.0"
    ).pack()

    tk.Label(
        parent,
        text="Created by Epicstargamer (Esg)"
    ).pack(
        pady=20
    )