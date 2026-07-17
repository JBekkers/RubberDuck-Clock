from source.window import Window
from source.animation import AnimationEngine
from source.clock import ClockEngine
from source.tray import Tray
from source.context_menu import ContextMenu

window = Window()
animation = AnimationEngine(window)
clock = ClockEngine(window, animation)
tray = Tray(window, animation, clock)
ContextMenu(window, animation)

window.root.mainloop()