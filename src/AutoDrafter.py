from tkinter import *
from tkinter import filedialog
from _tkinter import TclError
import Drafter
import math

WINDOW_X = 500
WINDOW_Y = 500
POPUP_X = int(WINDOW_X // 1.5)
POPUP_Y = int(WINDOW_Y // 1)


class Window(Frame):
    def __init__(self, master=None):
        self.qb_csv = "None set"
        self.rb_csv = "None set"
        self.wr_csv = "None set"
        self.te_csv = "None set"
        self.pick_index = ""
        self.num_rounds = ""
        self.num_teams = ""
        self.num_qbs = ""
        self.num_rbs = ""
        self.num_wrs = ""
        self.num_tes = ""
        self.league_type = ""
        self.randomness = ""
        self.config = IntVar()
        self.type = IntVar()
        self.qb_var = IntVar()
        self.rb_var = IntVar()
        self.wr_var = IntVar()
        self.round_var = IntVar()
        self.conf_info = ""
        self.conf_message = ""

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

        main_menu.add_command(label="Run", command=self.run)

        self.qb_label = Label(
            text="QB CSV:"
        )  # TODO: Make viterbi dependent on these inputs
        self.qb_label.place(
            x=0, y=0
        )  # TODO: Add fields to view and modify pick indices
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
        self.popup.geometry(f"{POPUP_X}x{POPUP_Y}")
        config_selection = Checkbutton(
            self.popup,
            text="Load from config?",
            variable=self.config,
            onvalue=1,
            offvalue=0,
            command=self.fetch_config,
        )
        self.config_info_label = Label(self.popup, text="")
        pick_index_label = Label(self.popup, text="Pick index:")
        round_label = Label(self.popup, text="Number of rounds: ")
        teams_label = Label(self.popup, text="Number of teams: ")
        qbs_label = Label(
            self.popup, text="Weight for QB selection (recommended - 1): "
        )
        self.rbs_label = Label(self.popup, text="Weight for RB selection: ")
        self.wrs_label = Label(self.popup, text="Weight for WR selection: ")
        self.tes_label = Label(self.popup, text="Weight for TE selection: ")
        league_type = Label(self.popup, text="League type: ")
        randomness = Label(self.popup, text="Randomness (1 lowest, 10 highest): ")
        self.e1 = Entry(self.popup)
        self.e2 = Entry(self.popup, textvariable=self.round_var)
        self.round_var.trace_add("write", self.update_config_labels)
        self.e3 = Entry(self.popup)
        self.e4 = Entry(self.popup, textvariable=self.qb_var)
        self.qb_var.trace_add("write", self.update_config_labels)
        self.e5 = Entry(self.popup, textvariable=self.rb_var)
        self.rb_var.trace_add("write", self.update_config_labels)
        self.e6 = Entry(self.popup, textvariable=self.wr_var)
        self.wr_var.trace_add("write", self.update_config_labels)
        self.e7 = Entry(self.popup)
        self.e8 = Entry(self.popup)

        ppr_button = Radiobutton(
            self.popup, text="PPR", var=self.type, value=1, command=self.set_type
        )
        standard_button = Radiobutton(
            self.popup, text="Standard", var=self.type, value=2, command=self.set_type
        )
        done_button = Button(self.popup, text="Done", command=self.submit_config)
        cancel_button = Button(self.popup, text="Cancel", command=self.popup.destroy)

        config_selection.pack()
        self.config_info_label.pack()
        pick_index_label.pack()
        self.e1.pack()
        round_label.pack()
        self.e2.pack()
        teams_label.pack()
        self.e3.pack()
        qbs_label.pack()
        self.e4.pack()
        self.rbs_label.pack()
        self.e5.pack()
        self.wrs_label.pack()
        self.e6.pack()
        self.tes_label.pack()
        self.e7.pack()
        league_type.pack()
        ppr_button.pack()
        standard_button.pack()
        randomness.pack()
        self.e8.pack()
        done_button.pack(side=LEFT, padx=POPUP_X / 6)
        cancel_button.pack(side=RIGHT, padx=POPUP_X / 6)

    def run(self):
        picks = Drafter.generate_picks(
            int(self.pick_index), int(self.num_rounds), int(self.num_teams)
        )
        players = Drafter.ff_viterbi(
            int(self.num_qbs),
            int(self.num_rbs),
            int(self.num_wrs),
            int(self.num_tes),
            picks,
            self.league_type,
            int(self.randomness),
        )
        if len(players) != len(picks):
            raise IndexError("Mismatched pick and player amounts.")
        for idx, pick in enumerate(picks):
            print(
                f"Your optimal selection for Round {idx+1}, Pick {pick}: {players[idx].name} (ADP: {players[idx].adp}, Projected Points: {players[idx].proj_points})"
            )

    def set_type(self):
        if self.type.get() == 1:
            self.league_type = "ppr"
        else:
            self.league_type = "standard"

    def submit_config(self):
        self.pick_index = self.e1.get()
        self.num_rounds = self.e2.get()
        self.num_teams = self.e3.get()
        self.num_qbs = self.e4.get()
        self.num_rbs = self.e5.get()
        self.num_wrs = self.e6.get()
        self.num_tes = self.e7.get()
        self.randomness = self.e8.get()
        self.wr_var.set(0)
        self.rb_var.set(0)
        self.qb_var.set(0)
        self.round_var.set(0)
        self.randomness = 11 - (int(self.randomness) % 11)
        self.num_rounds = int(self.num_rounds) - 2
        self.num_qbs = int(self.num_qbs) - 1 if int(self.num_qbs) > 1 else 1
        self.popup.destroy()

    def fetch_config(self):
        if self.config.get() == 1:
            conf_location = filedialog.askopenfilename()
            check = Drafter.load_config(conf_location)
            conf_data = check[1]
            if check[0]:
                try:
                    self.conf_message = "Config loaded successfully."
                    self.conf_info = conf_data["config"][0]
                    self.e1.delete(0, END)
                    self.e1.insert(0, self.conf_info["draft_slot"])
                    self.e2.delete(0, END)
                    self.e2.insert(0, self.conf_info["num_rounds"])
                    self.e3.delete(0, END)
                    self.e3.insert(0, self.conf_info["num_teams"])
                    self.e4.delete(0, END)
                    self.e4.insert(0, self.conf_info["qb_weight"])
                    self.e5.delete(0, END)
                    self.e5.insert(0, self.conf_info["rb_weight"])
                    self.e6.delete(0, END)
                    self.e6.insert(0, self.conf_info["wr_weight"])
                    self.e7.delete(0, END)
                    self.e7.insert(0, self.conf_info["te_weight"])

                    self.league_type = self.conf_info["league_type"]
                    if self.league_type.lower() == "standard":
                        self.type.set(2)
                    elif self.league_type.lower() == "ppr":
                        self.type.set(1)
                    else:
                        raise KeyError(
                            f"League type '{self.league_type}' invalid, should be either ppr or standard"
                        )

                    self.e8.delete(0, END)
                    self.e8.insert(0, self.conf_info["randomness"])
                    self.update_config_labels()
                except KeyError as e:
                    self.conf_message = (
                        f"Error parsing config: {e}, check that correct labels are used"
                    )
                    self.update_config_labels()
            else:
                self.conf_message = "Failed to load config - check file type."
                self.config.set(0)
                self.update_config_labels()

    def update_config_labels(self, *args):
        try:
            self.config_info_label.configure(
                text=self.conf_message, wraplength=POPUP_X, justify=CENTER
            )
            try:
                self.rbs_label.configure(
                    text=f"Weight for RB selection: (recommended - {math.ceil((int(self.round_var.get()) - 2 - int(self.qb_var.get())) / 2)})",
                    wraplength=POPUP_X,
                    justify=CENTER,
                )
                self.wrs_label.configure(
                    text=f"Weight for WR selection: (recommended - {math.floor((int(self.round_var.get()) - 2 - int(self.qb_var.get())) // 2)})",
                    wraplength=POPUP_X,
                    justify=CENTER,
                )
                self.tes_label.configure(
                    text=f"Weight for TE selection: (recommended - {int(self.round_var.get()) - int(self.qb_var.get()) - int(self.wr_var.get()) - int(self.rb_var.get())})",
                    wraplength=POPUP_X,
                    justify=CENTER,
                )
            except ValueError:
                pass
            self.after(1000, self.update_config_labels)
        except TclError:
            pass

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
