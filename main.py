import tkinter as tk
from tkinter import messagebox, filedialog


def info(event):
    messagebox.showinfo('Вейч', 'Введите через пробел числа при которых функция принимает значения 1, после чего '
                                'нажмите Ctrl+S.\nЧтобы очистить поле нажмите Esc, при повторном нажатии - окно '
                                'закроется.')


class CreateImage:
    def __init__(self):
        self.modes = ['Вейч', 'Карно']

        self.root = tk.Tk()
        self.change_mode()
        self.root.resizable(False, False)
        self.units = tk.Entry(self.root, font=('Arial', 15))
        self.units.pack()
        self.units.bind("<Control-s>", self.enter)
        self.root.bind("<Escape>", self.escape)
        self.root.bind("<F1>", info)
        self.root.bind("<Up>", self.change_mode)
        self.root.mainloop()

    def change_mode(self, event=None):
        """Change mode: Veych or Karno"""
        self.modes[0], self.modes[1] = self.modes[1], self.modes[0]
        self.root.title(self.modes[0])

    def escape(self, event):
        if self.units.get() == '':
            self.root.quit()
        else:
            self.units.delete(0, 'end')

    def enter(self, event):
        print(filedialog.asksaveasfilename(filetypes=[('PNG', '*.PNG')], defaultextension=[('PNG', '*.PNG')]))


x = CreateImage()
