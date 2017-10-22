import tkinter as tk
import tkinter.ttk as ttk
import random as rnd

style = None


def random_color():
    """
    Returns a random color as a string
    :return: a color
    """
    def r():
        return rnd.randint(0, 0xffff)
    return '#{:04x}{:04x}{:04x}'.format(r(), r(), r())


def get_style(master=None):
    """
    Returns the style object instance for handling styles
    :param master: the parent component
    :return: the style
    """
    global style
    if not style:
        style = ttk.Style(master) if master else ttk.Style()

    return style


def get_style_name(widget):
    """
    Returns the the name of the current style applied on this widget
    :param widget: the widget
    :return: the name of the style
    """
    # .config('style') call returns the tuple
    # ( option name, dbName, dbClass, default value, current value)
    return widget.config('style')[-1]


def get_background_color(widget):
    """
    Returns a string representing the background color of the widget
    :param widget: a widget
    :return: the color of the widget
    """
    global style
    color = style.lookup(get_style_name(widget), 'background')
    return color


def highlighted_rgb(color_value):
    """
    Returns a slightly modified rgb value
    :param color_value: one of three possible rgb values
    :return: one of three possible rgb values, but highlighted
    """
    result = (color_value / 65535) * 255
    result += (255 - result) / 2
    return result


def highlighted_color(widget, color):
    """
    Returns a highlighted color from the original entered
    :param color: a color
    :return: a highlight color for the one entered
    """
    c = widget.winfo_rgb(color)
    r = highlighted_rgb(c[0])
    g = highlighted_rgb(c[1])
    b = highlighted_rgb(c[2])
    return ("#%2.2x%2.2x%2.2x" % (round(r), round(g), round(b))).upper()


def change_highlight_style(event=None):
    """
    Applies the highlight style for a color
    :param event: the event of the styled widget
    """
    global style
    widget = event.widget
    current_color = get_background_color(widget)
    color = highlighted_color(event.widget, current_color)
    style.map(get_style_name(widget), background=[('active', color)])


if __name__ == '__main__':
    root = tk.Tk()

    style = get_style()

    button = ttk.Button(root, text='Test')
    button.config(style='MyStyle.TButton')
    style.configure('MyStyle.TButton', background='red')

    button.unbind('<Enter>')
    button.bind('<Enter>', change_highlight_style)
    button.pack()

    style.configure('My1.TButton', background='yellow')
    but = ttk.Button(root, text='1', style='My1.TButton')
    but.unbind('<Enter>')
    but.bind('<Enter>', change_highlight_style)
    but.pack()

    style.configure('My2.TButton', background='purple')
    but = ttk.Button(root, text='2', style='My2.TButton')
    but.unbind('<Enter>')
    but.bind('<Enter>', change_highlight_style)
    but.pack()

    style.configure('My3.TButton', background='green')
    but = ttk.Button(root, text='3', style='My3.TButton')
    but.unbind('<Enter>')
    but.bind('<Enter>', change_highlight_style)
    but.pack()

    style.configure('My4.TButton', background='yellow')
    but = ttk.Button(root, text='4', style='My4.TButton')
    but.unbind('<Enter>')
    but.bind('<Enter>', change_highlight_style)
    but.pack()

    root.mainloop()
