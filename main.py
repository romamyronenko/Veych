###################################################
#                                                 #
# author: Roman Myronenko                         #
#                                                 #
# program which make Veych and Karno diagram      #
#                                                 #
###################################################
import tkinter as tk
from tkinter import messagebox, filedialog


class GUI:
    def __init__(self):
        self.modes = ['Карно', 'Вейч']

        self.root = tk.Tk()
        self.change_mode()
        self.root.resizable(False, False)

        self.units = tk.Entry(self.root, font=('Arial', 15))
        self.units.pack()

        # set hot keys
        self.units.bind("<Control-s>", self.save)
        self.root.bind("<Escape>", self.escape)
        self.root.bind("<F1>", self.info)
        self.root.bind("<Up>", self.change_mode)

        self.root.mainloop()

    def change_mode(self, event=None):
        """Change mode: Veych or Karno"""
        self.modes[0], self.modes[1] = self.modes[1], self.modes[0]
        self.root.title(self.modes[0])

    def escape(self, event):
        """Method that handles press Escape. If Entry not empty clear, else close window."""
<<<<<<< HEAD
        if not self.units.get():
=======
        if self.units.get() == '':
>>>>>>> ec83abbaafca3eb1843a799c96b3a4c507d4a1bc
            self.root.quit()
        else:
            self.units.delete(0, 'end')

    def save(self, event):
        """Specified file save path"""
<<<<<<< HEAD
        print(filedialog.asksaveasfilename(filetypes=[('PNG', '*.PNG')],
                                           defaultextension=[('PNG', '*.PNG')]))

    def info(self, event):
        """Showed info how to use program"""
        messagebox.showinfo('Вейч',
                            'Введите через пробел числа при которых функция принимает значения 1, после чего '
                            'нажмите Ctrl+S.\nЧтобы очистить поле нажмите Esc, при повторном нажатии - окно закроется.'
                            )
=======
        print(filedialog.asksaveasfilename(filetypes=[('PNG', '*.PNG')], defaultextension=[('PNG', '*.PNG')]))
>>>>>>> ec83abbaafca3eb1843a799c96b3a4c507d4a1bc

    def info(self, event):
        """Showed info how to use program"""
        messagebox.showinfo('Вейч',
                            'Введите через пробел числа при которых функция принимает значения 1, после чего '
                            'нажмите Ctrl+S.\nЧтобы очистить поле нажмите Esc, при повторном нажатии - окно закроется.'
                            )


x = GUI()
