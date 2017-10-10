from tkinter import messagebox

class TextUi(object):
    def output(self, message):
        print(message)


class Gui(object):
    def output(self, message):
        messagebox.showinfo('', message)


output = TextUi().output
# output = Gui().output