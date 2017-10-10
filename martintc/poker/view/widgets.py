import os
import tkinter as tk
import tkinter.ttk as ttk
from PIL.ImageTk import PhotoImage

# TODO For making this, we should accomplish a class that can inherit from this and ttk.Button both
from martintc.poker.model.die import Die
from martintc.poker.view import styleUtils


class PokerWidget(ttk.Widget):
    pass


class ImgButton(ttk.Button):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)
        self._img = kw.get('image')
        # Temporal test handler for testing highlight color
        self.bind('<Button-1>', self.change_color)

    def change_color(self, __=None):
        import random as rnd
        self.event_generate('<Leave>')
        self.set_background_color(rnd.choice(['black', 'white', 'red', 'blue',
                                              'cyan', 'purple', 'green', 'brown',
                                              'gray', 'yellow', 'orange', 'cyan',
                                              'pink', 'purple', 'violet']))
        self.event_generate('<Enter>')

    def get_style_name(self):
        return styleUtils.get_style_name(self)

    def set_background_color(self, color):
        styleUtils.get_style().configure(self.get_style_name(), background=color)
        self.unbind('<Enter>')
        self.bind('<Enter>', self.change_highlight_style)

    def get_background_color(self):
        """
        Returns a string representing the background color of the widget
        :return: the color of the widget
        """
        return styleUtils.get_style().lookup(self.get_style_name(), 'background')

    def change_highlight_style(self, __=None):
        """
        Applies the highlight style for a color
        :param event: the event of the styled widget
        """
        current_color = self.get_background_color()
        color = styleUtils.highlighted_color(self, current_color)
        styleUtils.get_style().map(self.get_style_name(), background=[('active', color)])



#TODO Whole class
class DieButton(ImgButton):
    """
    Button for holding a die
    """

    DIE_IMG_NAME = 'miniDado{}.jpg'
    IMAGES_DIR = os.path.sep + os.path.sep.join(['home', 'madtyn', 'PycharmProjects', 'poker', 'resources', 'images'])
    UNKNOWN_IMG = os.path.sep.join([IMAGES_DIR, DIE_IMG_NAME.format(0)])

    IMAGES = (lambda IMAGES_DIR=IMAGES_DIR, DIE_IMG_NAME=DIE_IMG_NAME: [os.path.sep.join([IMAGES_DIR, DIE_IMG_NAME.format(face)]) for face in Die.FACES])()

    def __init__(self, master=None, value=None, **kw):
        # Default image when hidden or without value

        current_img = PhotoImage(file=DieButton.UNKNOWN_IMG)
        super().__init__(master, image=current_img, **kw)
        if not value:
            pass
        elif not isinstance(value, (int, Die)):
            pass
        elif isinstance(value, Die):
            self.die = value
        elif isinstance(value, int):
            self.die = Die(value)
        else:
            raise ValueError()
        self.set_background_color('green')


    def select(self):
        pass

    def throw(self):
        pass

    if __name__ == '__main__':
        root = tk.Tk()
        ImgButton(root).pack()
