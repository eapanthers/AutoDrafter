from tkinter import *
from tkinter import filedialog
import Drafter

# TODO: First, display blank menu. User must load csvs and set parameters
# TODO: Then a run button runs with the included params, displays output as labels

WINDOW_X = 500
WINDOW_Y = 500


class Window(Frame):
    def __init__(self, master=None):
        self.qb_csv = "None set"
        self.rb_csv = "None set"
        self.wr_csv = "None set"
        self.te_csv = "None set"
        self.pick_index = 1
        self.num_rounds = 14
        self.num_teams = 10
        self.num_qbs = 1
        self.num_rbs = 6
        self.num_wrs = 5
        self.num_tes = 2
        self.league_type = "standard"
        self.randomness = 1
        self.config = IntVar()
        self.conf_info = ""

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

        file_menu.add_command(label="Set Config...", command=self.manage_config)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=root.destroy)
        main_menu.add_cascade(label="File", menu=file_menu)

        main_menu.add_command(label="Run")

        self.qb_label = Label(text="QB CSV:")
        self.qb_label.place(x=0, y=0)
        self.rb_label = Label(text="RB CSV:")
        self.rb_label.place(x=0, y=40)
        self.wr_label = Label(text="WR CSV:")
        self.wr_label.place(x=0, y=80)
        self.te_label = Label(text="TE CSV:")
        self.te_label.place(x=0, y=120)

        self.qb_csv_label = Label(text="", bg="#f5f5f5", bd=2)
        self.qb_csv_label.place(x=0, y=20)

        self.rb_csv_label = Label(text="")
        self.rb_csv_label.place(x=0, y=60)

        self.wr_csv_label = Label(text="")
        self.wr_csv_label.place(x=0, y=100)

        self.te_csv_label = Label(text="")
        self.te_csv_label.place(x=0, y=140)
        self.update_labels()

    def manage_config(self):
        self.popup = Toplevel(self.master)
        self.popup.title("Configure")
        self.popup.geometry(f"{int(WINDOW_X//1.5)}x{int(WINDOW_Y//1.5)}")
        config_selection = Checkbutton(self.popup, text="Load from config?", variable=self.config, onvalue=1, offvalue=0, command=self.fetch_config)
        self.config_info_label = Label(self.popup, text="")
        config_selection.pack()
        self.config_info_label.pack()

    def fetch_config(self):
        if self.config.get() == 1:
            conf_location = filedialog.askopenfilename()
            check = Drafter.load_config(conf_location)
            conf_data = check[1]
            if check[0]:
                config_info = conf_data["config"][0]
                self.conf_info = config_info
                self.update_config_labels()

    def update_config_labels(self):
        self.config_info_label.configure(text=self.conf_info)
        self.after(1000, self.update_config_labels)

    def update_labels(self):
        self.qb_csv_label.configure(text=self.qb_csv)
        self.rb_csv_label.configure(text=self.rb_csv)
        self.wr_csv_label.configure(text=self.wr_csv)
        self.te_csv_label.configure(text=self.te_csv)
        self.after(1000, self.update_labels)

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
    root.after(1000, app.update_labels)
    root.mainloop()
