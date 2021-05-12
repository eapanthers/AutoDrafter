from tkinter import *
import time


class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master

        self.pack(fill=BOTH, expand=1)
        exit_button = Button(self, text="Exit", command=self.click_exit_button)
        exit_button.place(x=0, y=0)

        menu = Menu(self.master)
        self.master.config(menu=menu)

        file_menu = Menu(menu)
        file_menu.add_command(label="Item")
        file_menu.add_command(label="Exit", command=self.click_exit_button)
        menu.add_cascade(label="File", menu=file_menu)

        edit_menu = Menu(menu)
        edit_menu.add_command(label="Edit")
        menu.add_cascade(label="Edit", menu=edit_menu)

        self.clock = Label(text="", fg="Red", font=("Helvetica", 18))
        self.clock.place(x=80, y=90)
        self.update_clock()

    def update_clock(self):
        now = time.strftime("%H:%M:%S")
        self.clock.configure(text=now)
        self.after(1000, self.update_clock)

    def click_exit_button(self):
        exit()


if __name__ == "__main__":
    root = Tk()
    app = Window(root)
    root.wm_title("test window")
    root.geometry("300x200")
    root.after(1000, app.update_clock)
    root.mainloop()
