import tkinter as tk
import tkinter.ttk as ttk

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
    """
    Frame containing the dice to show
    """
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        dice_buttons = []

        for i, _ in enumerate(range(5)):

            current_style = 'Die{}.TButton'.format(i)

            style = ttk.Style()
            style.configure(current_style,
                            borderwidth=6,
                            )

            button = DieButton(self, style=current_style)
            button.grid(row=0, column=i, padx=5, pady=5)
            # button.pack(side=tk.LEFT)
            dice_buttons.append(button)


class ButtonBar(ttk.Frame):
    """
    Frame containing the main buttons and controls for playing
    """
    def __init__(self, master=None, *args, **kwargs):
        super().__init__(master, **kwargs)


class App(ttk.Frame):
    """
    Frame containing the whole window app, the menu, and the subframes
    """
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.main = DiceFrame(self)
        self.buttonBar = ButtonBar(self)
        self.textarea = tk.Text(self)

        self.main.pack()
        self.buttonBar.pack()
        self.textarea.pack()
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
    App(root).pack(side="top", fill="both", expand=True)
    root.update()
    root.minsize(root.winfo_width(), root.winfo_height())
    root.mainloop()
