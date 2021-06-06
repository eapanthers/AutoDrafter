import math
from _tkinter import TclError
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from tkinter import messagebox

import pandas as pd

import Drafter
from PlayerList import PlayerList
from Player import Player

WINDOW_X = 500
WINDOW_Y = 500
POPUP_X = int(WINDOW_X // 1.5)
POPUP_Y = int(WINDOW_Y // 1)
LIVE_DRAFT_X = 1000
LIVE_DRAFT_Y = 750


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
        self.randomness = ""
        self.config = IntVar()
        self.type = IntVar()
        self.qb_var = IntVar()
        self.rb_var = IntVar()
        self.wr_var = IntVar()
        self.round_var = IntVar()
        self.conf_info = ""
        self.conf_message = ""
        self.qbs = {}
        self.rbs = {}
        self.wrs = {}
        self.tes = {}
        self.all = {}

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
        main_menu.add_command(label="View Board", command=self.live_draft)

        self.qb_label = Label(text="QB CSV:")
        self.qb_label.place(
            x=0, y=0
        )  # TODO: Add live draft feature, list all players from CSV and add checkbox to mark selected. Run viterbi when user pick reached.
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

        run_button = Button(text="Run", command=self.run)
        run_button.place(x=WINDOW_X // 2, y=WINDOW_Y - 50)
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
        pick_index_label = Label(self.popup, text="Picks: (Comma separated, or a single number if no trades)")
        round_label = Label(self.popup, text="Number of rounds: ")
        teams_label = Label(self.popup, text="Number of teams: ")
        qbs_label = Label(self.popup, text="Weight for QB selection (recommended: 1) ")
        self.rbs_label = Label(self.popup, text="Weight for RB selection: ")
        self.wrs_label = Label(self.popup, text="Weight for WR selection: ")
        self.tes_label = Label(self.popup, text="Weight for TE selection: ")
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
        randomness.pack()
        self.e8.pack()
        done_button.pack(side=LEFT, padx=POPUP_X / 6)
        cancel_button.pack(side=RIGHT, padx=POPUP_X / 6)

    def run(self):
        if type(self.pick_index) == str and len(self.pick_index) > 1:
            self.pick_index = self.pick_index.strip("[](){} ").split(",")
        if len(self.pick_index) > 1:
            picks = [int(pick) for pick in self.pick_index]
        else:
            picks = Drafter.generate_picks(
                int(self.pick_index), int(self.num_rounds), int(self.num_teams)
            )
        players = Drafter.ff_viterbi(
            int(self.num_qbs),
            int(self.num_rbs),
            int(self.num_wrs),
            int(self.num_tes),
            picks,
            self.qb_csv,
            self.rb_csv,
            self.wr_csv,
            self.te_csv,
            int(self.randomness),
        )
        if len(players) != len(picks):
            raise IndexError("Mismatched pick and player amounts.")
        self.display_results(picks, players)

    def display_results(self, selections, players):
        result_popup = Toplevel(self.master)
        result_popup.title("Draft results")
        if len(self.pick_index) == 1:
            result_popup.geometry(f"{POPUP_X * 2}x{35*self.num_rounds}")
        else:
            result_popup.geometry(f"{POPUP_X * 2}x{35*len(self.pick_index)}")
        text = Label(
            result_popup, pady=10, padx=10, wraplength=POPUP_X * 2, font=("Arial", 10)
        )
        output = ""
        for idx, pick in enumerate(selections):
            output += f"Your optimal selection for Round {idx + 1}, Pick {pick}: {players[idx].name} (ADP: {players[idx].adp}, Projected Points: {players[idx].proj_points})\n\n"
        text.configure(text=output)
        text.pack()

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

                    self.e8.delete(0, END)
                    self.e8.insert(0, self.conf_info["randomness"])

                    if self.conf_info["qb_csv"] != "":
                        self.qb_csv = self.conf_info["qb_csv"]
                    if self.conf_info["rb_csv"] != "":
                        self.rb_csv = self.conf_info["rb_csv"]
                    if self.conf_info["wr_csv"] != "":
                        self.wr_csv = self.conf_info["wr_csv"]
                    if self.conf_info["te_csv"] != "":
                        self.te_csv = self.conf_info["te_csv"]
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
                    text=f"Weight for RB selection: (recommended: {math.ceil((int(self.round_var.get()) - 2 - int(self.qb_var.get())) / 2)})",
                    wraplength=POPUP_X,
                    justify=CENTER,
                )
                self.wrs_label.configure(
                    text=f"Weight for WR selection: (recommended: {math.floor((int(self.round_var.get()) - 2 - int(self.qb_var.get())) // 2)})",
                    wraplength=POPUP_X,
                    justify=CENTER,
                )
                self.tes_label.configure(
                    text=f"Weight for TE selection: (recommended: {int(self.round_var.get()) - int(self.qb_var.get()) - int(self.wr_var.get()) - int(self.rb_var.get())})",
                    wraplength=POPUP_X,
                    justify=CENTER,
                )
            except ValueError:
                pass
            self.after(1000, self.update_config_labels)
        except TclError:
            pass

    def live_draft(self):
        draft_window = Toplevel(self.master)
        draft_window.title("Live Draft")
        draft_window.geometry(f"{LIVE_DRAFT_X}x{LIVE_DRAFT_Y}")
        tab_control = ttk.Notebook(draft_window)
        all_tab = Frame(tab_control)
        qb_tab = ttk.Frame(tab_control)
        rb_tab = ttk.Frame(tab_control)
        wr_tab = ttk.Frame(tab_control)
        te_tab = ttk.Frame(tab_control)

        tab_control.add(all_tab, text="All")
        tab_control.add(qb_tab, text="QB List")
        tab_control.add(rb_tab, text="RB List")
        tab_control.add(wr_tab, text="WR List")
        tab_control.add(te_tab, text="TE List")
        tab_control.pack(expand=1, fill="both")

        qb_df = pd.read_csv(self.qb_csv, delimiter=",")
        rb_df = pd.read_csv(self.rb_csv, delimiter=";")
        wr_df = pd.read_csv(self.wr_csv, delimiter=";")
        te_df = pd.read_csv(self.te_csv, delimiter=",")

        all_df = rb_df
        all_df = all_df.append(qb_df).append(wr_df).append(te_df)
        sorted_df = all_df.sort_values(by="ADP")

        self.list_box = ttk.Treeview(
            all_tab, columns=sorted_df.columns.values, show="headings", height=33
        )
        # self.list_box.bind("<Double-1>", self.display_selected)
        width_list = [100, 250, 50, 50, 50, 50, 100, 100, 75]
        sorted_df.columns.values[0] = "Availability"
        qb_df.columns.values[0] = "Availability"
        rb_df.columns.values[0] = "Availability"
        wr_df.columns.values[0] = "Availability"
        te_df.columns.values[0] = "Availability"
        for i, col in enumerate(sorted_df.columns.values):
            self.list_box.column(i, width=width_list[i], anchor=CENTER)
            self.list_box.heading(i, text=col)

        for i, player in enumerate(sorted_df.values):
            self.list_box.insert(
                "",
                END,
                values=(
                    "Available",
                    player[1],
                    player[2],
                    player[3],
                    player[4],
                    player[5],
                    player[6],
                    player[7],
                    player[8],
                ),
            )
        self.list_box.grid(row=1, column=0, sticky=NSEW)
        scrollbar = ttk.Scrollbar(all_tab, orient=VERTICAL, command=self.list_box.yview)
        self.list_box.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=1, column=1, sticky="ns")

        # qb tab

        qb_list_box = ttk.Treeview(
            qb_tab, columns=qb_df.columns.values, show="headings", height=33
        )
        for i, col in enumerate(qb_df.columns.values):
            qb_list_box.column(i, width=width_list[i], anchor=CENTER)
            qb_list_box.heading(i, text=col)

        for i, player in enumerate(qb_df.values):
            qb_list_box.insert(
                "",
                END,
                values=(
                    "Available",
                    player[1],
                    player[2],
                    player[3],
                    player[4],
                    player[5],
                    player[6],
                    player[7],
                    player[8],
                ),
            )
        qb_list_box.grid(row=1, column=0, sticky=NSEW)
        qb_scrollbar = ttk.Scrollbar(qb_tab, orient=VERTICAL, command=qb_list_box.yview)
        qb_list_box.configure(yscroll=qb_scrollbar.set)
        qb_scrollbar.grid(row=1, column=1, sticky="ns")

        # rb tab

        rb_list_box = ttk.Treeview(
            rb_tab, columns=rb_df.columns.values, show="headings", height=33
        )
        for i, col in enumerate(rb_df.columns.values):
            rb_list_box.column(i, width=width_list[i], anchor=CENTER)
            rb_list_box.heading(i, text=col)

        for i, player in enumerate(rb_df.values):
            rb_list_box.insert(
                "",
                END,
                values=(
                    "Available",
                    player[1],
                    player[2],
                    player[3],
                    player[4],
                    player[5],
                    player[6],
                    player[7],
                    player[8],
                ),
            )
        rb_list_box.grid(row=1, column=0, sticky=NSEW)
        rb_scrollbar = ttk.Scrollbar(rb_tab, orient=VERTICAL, command=rb_list_box.yview)
        rb_list_box.configure(yscroll=rb_scrollbar.set)
        rb_scrollbar.grid(row=1, column=1, sticky="ns")

        # wr tab

        wr_list_box = ttk.Treeview(
            wr_tab, columns=wr_df.columns.values, show="headings", height=33
        )
        for i, col in enumerate(wr_df.columns.values):
            wr_list_box.column(i, width=width_list[i], anchor=CENTER)
            wr_list_box.heading(i, text=col)

        for i, player in enumerate(wr_df.values):
            wr_list_box.insert(
                "",
                END,
                values=(
                    "Available",
                    player[1],
                    player[2],
                    player[3],
                    player[4],
                    player[5],
                    player[6],
                    player[7],
                    player[8],
                ),
            )
        wr_list_box.grid(row=1, column=0, sticky=NSEW)
        wr_scrollbar = ttk.Scrollbar(wr_tab, orient=VERTICAL, command=wr_list_box.yview)
        wr_list_box.configure(yscroll=wr_scrollbar.set)
        wr_scrollbar.grid(row=1, column=1, sticky="ns")

        # wr tab

        te_list_box = ttk.Treeview(
            te_tab, columns=te_df.columns.values, show="headings", height=33
        )
        for i, col in enumerate(te_df.columns.values):
            te_list_box.column(i, width=width_list[i], anchor=CENTER)
            te_list_box.heading(i, text=col)

        for i, player in enumerate(te_df.values):
            te_list_box.insert(
                "",
                END,
                values=(
                    "Available",
                    player[1],
                    player[2],
                    player[3],
                    player[4],
                    player[5],
                    player[6],
                    player[7],
                    player[8],
                ),
            )
        te_list_box.grid(row=1, column=0, sticky=NSEW)
        te_scrollbar = ttk.Scrollbar(te_tab, orient=VERTICAL, command=te_list_box.yview)
        te_list_box.configure(yscroll=te_scrollbar.set)
        te_scrollbar.grid(row=1, column=1, sticky="ns")

        all_list = self.get_players(all_df)
        qb_list = self.get_players(qb_df)
        rb_list = self.get_players(rb_df)
        wr_list = self.get_players(wr_df)
        te_list = self.get_players(te_df)

        for player in qb_list.players:
            self.qbs[player.name] = player
            self.all[player.name] = player
        for player in rb_list.players:
            self.rbs[player.name] = player
            self.all[player.name] = player
        for player in wr_list.players:
            self.wrs[player.name] = player
            self.all[player.name] = player
        for player in te_list.players:
            self.tes[player.name] = player
            self.all[player.name] = player

    def get_players(self, df):
        all_players = PlayerList()
        for i, row in df.iterrows():
            new_player = Player(row[8], row[7], row[1])
            all_players.add(new_player)
        return all_players

    def display_selected(self, event):
        for selected in self.list_box.selection():
            player_name = self.list_box.item(selected)["values"][1]
            if not self.all[player_name].picked:
                messagebox.showinfo(
                    title="Player selected", message=f"{player_name} marked as selected"
                )
                self.all[player_name].picked = True
            else:
                messagebox.showinfo(
                    title="Player unselected",
                    message=f"{player_name} marked as available",
                )
                self.all[player_name].picked = False

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
