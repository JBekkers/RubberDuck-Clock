from Source.Config import load_config
from Source.Animation_Manager import animate_sprite, choose_random_animation, duck_clicked
from Source.Menu import setup_menu
from Source.Window_Manager import root, canvas, set_position
from Source.Clock import setup_clock,start_clock

config = load_config()
settings = config["settings"]

setup_menu(settings, config)

set_position(
    config["position"]["x"],
    config["position"]["y"]
)

canvas.bind("<Button-1>", duck_clicked)

setup_clock()
start_clock(settings)

animate_sprite()
choose_random_animation()

root.mainloop()