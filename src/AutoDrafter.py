from tkinter import *
from tkinter import filedialog

# TODO: First, display blank menu. User must load csvs and set parameters
# TODO: Then a run button runs with the included params, displays output as labels

WINDOW_X = 500
WINDOW_Y = 500


class Window(Frame):
    def __init__(self, master=None):
        self.qb_csv = "standard_qbs.csv"
        self.rb_csv = "standard_rbs.csv"
        self.wr_csv = "standard_wrs.csv"
        self.te_csv = "standard_tes.csv"
        self.pick_index = 1
        self.num_rounds = 14
        self.num_teams = 10
        self.num_qbs = 1
        self.num_rbs = 6
        self.num_wrs = 5
        self.num_tes = 2
        self.league_type = "standard"
        self.randomness = 1

        Frame.__init__(self, master)
        self.master = master

        self.pack(fill=BOTH, expand=1)

        main_menu = Menu(self.master)
        self.master.config(menu=main_menu)

        file_menu = Menu(main_menu, tearoff=False)
        csv_menu = Menu(file_menu, tearoff=False)
        csv_menu.add_command(label="Set QB CSV", command=self.set_qb_csv)
        csv_menu.add_command(label="Set RB CSV", command=self.set_rb_csv)
        csv_menu.add_command(label="Set WR CSV", command=self.set_wr_csv)
        csv_menu.add_command(label="Set TE CSV", command=self.set_te_csv)
        file_menu.add_cascade(label="Set CSVs", menu=csv_menu)

        file_menu.add_command(label="Set Config")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=root.destroy)
        main_menu.add_cascade(label="File", menu=file_menu)

        main_menu.add_command(label="Run")

    def set_qb_csv(self):
        filename = filedialog.askopenfilename()
        self.qb_csv = filename

    def set_rb_csv(self):
        filename = filedialog.askopenfilename()
        self.rb_csv = filename

    def set_wr_csv(self):
        filename = filedialog.askopenfilename()
        self.wr_csv = filename

    def set_te_csv(self):
        filename = filedialog.askopenfilename()
        self.te_csv = filename


if __name__ == "__main__":
    root = Tk()
    app = Window(root)
    root.wm_title("Fantasy Football Auto Drafter")
    root.geometry(f"{WINDOW_X}x{WINDOW_Y}")
    root.mainloop()
