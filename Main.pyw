from Source.Config_Manager import load_config
from Source.Animation_Manager import animate_sprite, choose_random_animation, duck_clicked
from Source.Menu_Manager import setup_menu
from Source.Window_Manager import root, canvas, set_position, start_move,move_window
from Source.Clock_Manager import setup_clock,start_clock

config = load_config()
settings = config["settings"]

setup_menu(settings, config)

set_position(
    config["position"]["x"],
    config["position"]["y"]
)

def on_click(event):
    start_move(event)
    duck_clicked(event)

def on_Move(event):
    move_window(event)

canvas.bind("<Button-1>", on_click)
canvas.bind("<B1-Motion>", on_Move)

setup_clock()
start_clock(settings)

animate_sprite()
choose_random_animation()

root.mainloop()