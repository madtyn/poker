import os

import tkinter as tk
import tkinter.ttk as ttk
from random import randint, random

from widgets import ImgButton


from martintc.poker.model.die import Die
from martintc.poker.view.widgets import DieButton

"""
Define some classes for compounding the gui
class Navbar(tk.Frame):
class Toolbar(tk.Frame):
class Statusbar(tk.Frame):

"""

# import glob
# Todas las rutas de imagenes:
# glob.glob(os.path.join(IMAGES_DIR, '*.jpg'))


class DiceFrame(ttk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        dice_buttons = []

        for i, _ in enumerate(range(5)):

            current_style = 'Die{}.TButton'.format(i)

            style = ttk.Style()
            style.configure(current_style,
                            borderwidth=6,
                            )

            button = DieButton(master, style=current_style)
            button.pack(side=tk.LEFT)
            dice_buttons.append(button)


class ButtonBar(ttk.Frame):
    def __init__(self, master=None, *args, **kwargs):
        super().__init__(master, **kwargs)


class App(ttk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self. main = DiceFrame(self)
        self.buttonBar = ButtonBar(self)
        """
        self.parent = parent # Only if needed
        self.statusbar = Statusbar(self, ...)
        self.toolbar = Toolbar(self, ...)
        self.navbar = Navbar(self, ...)
        self.main = Main(self, ...)

        self.statusbar.pack(side="bottom", fill="x")
        self.toolbar.pack(side="top", fill="x")
        self.navbar.pack(side="left", fill="y")
        self.main.pack(side="right", fill="both", expand=True)
        """


if __name__ == "__main__":
    root = tk.Tk()
    DiceFrame(root).pack(side="top", fill="both", expand=True)
    root.mainloop()