"""
Name: Script Autolauncher
Description: ...
Author: Belp2801
Created: 09.11.2024
"""

import customtkinter
import sys, os, csv, time, datetime

customtkinter.set_appearance_mode("light")

os.chdir(os.path.dirname(os.path.realpath(__file__)))


class ScriptAutoLauncher(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Script AutoLauncher")
        self.resizable(False, False)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1), weight=1)

        self.init_constants()
        self.init_data()
        self.init_vars()
        self.init_ctk_vars()

        self.build_widgets()
        self.countdown()

    # region init
    def init_constants(self):
        self.scripts_filename = "scripts.csv"
        self.latest_running_time_filename = "latest_running_time.csv"

        self.time_gap = 5
        self.page_size = 15

    def init_data(self):
        self.load_scripts_data()
        self.load_latest_running_time()

        # init data
        self.data = {}
        for script in self.scripts.keys():
            self.data[script] = {
                "start_time": float(self.latest_running_time[script]),
                "success_count": 0,
                "wait_time": int(self.scripts[script]["wait_time"]),
            }

            self.data[script]["remain_time"] = self.data[script]["wait_time"] - (
                time.time() - self.data[script]["start_time"]
            )

        self.save_latest_running_time()

    def load_scripts_data(self):
        self.scripts = {}

        with open(self.scripts_filename, "r") as f:
            reader = csv.DictReader(f)
            for line in reader:
                if not int(line["is_end"] if line["is_end"] != "" else 0):
                    line["wait_time"] = (float(line["cycle"]) * 60 + self.time_gap) * 60
                    self.scripts[line["name"]] = line

    def load_latest_running_time(self):
        self.latest_running_time = {}
        if not os.path.exists(self.latest_running_time_filename):
            with open(self.latest_running_time_filename, mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["key"])
                writer.writerow(["value"])

        try:
            with open(self.latest_running_time_filename, "r") as f:
                reader = csv.DictReader(f)
                row = next(reader)
                self.latest_running_time = row
        except:
            pass

        for script in self.scripts.keys():
            if script not in self.latest_running_time:
                self.latest_running_time[script] = time.time()

    def init_vars(self):
        self.time_var = {}
        self.success_count_var = {}

    def init_ctk_vars(self):
        self.script_var = customtkinter.StringVar()
        for script in self.scripts.keys():
            self.time_var[script] = customtkinter.StringVar()
            self.success_count_var[script] = customtkinter.StringVar()

            self.time_var[script].set(
                self.format_time(self.data[script]["remain_time"])
            )
            self.success_count_var[script].set(
                str(self.data[script]["success_count"]).rjust(2, "0")
            )

    # endregion

    # region build ui
    def build_widgets(self):
        self.build_toolbar_frame()
        self.build_grid_frame()
        self.build_footers()

    def build_toolbar_frame(self):
        self.toolbar_frame = customtkinter.CTkFrame(
            self,
            corner_radius=10,
        )
        self.toolbar_frame.pack(
            fill=customtkinter.BOTH, expand=True, padx=5, pady=(5, 0)
        )

        # combobox
        self.combobox_frame = customtkinter.CTkFrame(
            self.toolbar_frame, bg_color="transparent", fg_color="transparent"
        )
        script_label = customtkinter.CTkLabel(self.combobox_frame, text="Script: ")
        script_combobox = customtkinter.CTkOptionMenu(
            self.combobox_frame,
            variable=self.script_var,
            values=sorted(self.scripts.keys()),
            fg_color=["#F9F9FA", "#343638"],
            text_color=["#000", "#fff"],
            width=220,
        )
        script_combobox.set(sorted(self.scripts.keys())[0])
        script_button = customtkinter.CTkButton(
            self.combobox_frame,
            command=lambda: self.run(self.script_var.get()),
            text="RUN",
            width=60,
        )

        script_label.grid(row=0, column=0, padx=(5, 0), pady=2)
        script_combobox.grid(row=0, column=1, padx=(10, 0), pady=2)
        script_button.grid(row=0, column=2, padx=(5, 2), pady=2)

        self.combobox_frame.pack(side=customtkinter.LEFT)

        # function button
        self.function_frame = customtkinter.CTkFrame(
            self.toolbar_frame, bg_color="transparent", fg_color="transparent"
        )

        reset_button = customtkinter.CTkButton(
            self.function_frame,
            text="Reset all time",
            command=lambda: self.reset_all_time(),
            width=120,
        )
        reset_button.grid(row=0, column=1, padx=(10, 5), pady=2)

        self.function_frame.pack(side=customtkinter.RIGHT)

    def build_grid_frame(self):
        self.grid_frame = customtkinter.CTkFrame(self, corner_radius=5)
        self.grid_frame.pack(padx=5, pady=5)

        headers = ["No", "Script", "Wait", "V", "Remain", "Func"]
        column_widths = [24, 220, 40, 32, 72, 50]

        self.data_grid = []
        for i, (script, value) in enumerate(self.scripts.items()):
            if i % self.page_size == 0:
                self.data_grid.append(headers)
            self.data_grid.append(
                [i + 1, script, f"{value['cycle'].rjust(2, '0')}", "", "", ""]
            )

        for row_index, row_data in enumerate(self.data_grid):
            for col_index, cell_data in enumerate(row_data):
                _row = row_index % (self.page_size + 1)
                _col = col_index + len(headers) * (row_index // (self.page_size + 1))

                frame = customtkinter.CTkFrame(
                    self.grid_frame, corner_radius=0, border_width=1
                )

                if _row == 0:
                    frame.configure(bg_color="#bbb", fg_color="#bbb")
                elif _row % 2 == 0:
                    frame.configure(bg_color="#ddd", fg_color="#ddd")
                else:
                    frame.configure(bg_color="#f0f0f0", fg_color="#f0f0f0")

                frame.grid(
                    row=_row,
                    column=_col,
                    padx=(15, 0) if _col > 0 and _col % len(headers) == 0 else 0,
                )
                if _row == 0:
                    entry = customtkinter.CTkLabel(
                        frame,
                        text=cell_data,
                        width=column_widths[col_index],
                        padx=2,
                        pady=2,
                        font=customtkinter.CTkFont(weight="bold", size=12),
                    )
                else:
                    # Function
                    if col_index == headers.index("Func"):
                        entry = customtkinter.CTkButton(
                            frame,
                            command=lambda x=row_data[1]: self.reset_time(x),
                            text="Reset",
                            width=column_widths[col_index],
                        )

                    # Time countdown
                    elif col_index == headers.index("Remain"):
                        entry = customtkinter.CTkEntry(
                            frame,
                            textvariable=self.time_var[row_data[1]],
                            justify=customtkinter.CENTER,
                            width=column_widths[col_index],
                            font=customtkinter.CTkFont(size=14),
                        )
                        entry.configure(state="disabled")
                    # Success count
                    elif col_index == headers.index("V"):
                        entry = customtkinter.CTkEntry(
                            frame,
                            textvariable=self.success_count_var[row_data[1]],
                            justify=customtkinter.CENTER,
                            width=column_widths[col_index],
                            font=customtkinter.CTkFont(size=14),
                        )
                        entry.configure(state="disabled")
                    # Cycle
                    elif col_index == headers.index("Wait"):
                        entry = customtkinter.CTkLabel(
                            frame,
                            text=self.format_time(cell_data, type="hm"),
                            justify=customtkinter.CENTER,
                            width=column_widths[col_index],
                        )
                        entry.configure(state="disabled")
                    else:
                        entry = customtkinter.CTkLabel(
                            frame,
                            text=cell_data,
                            padx=2,
                            pady=2,
                            width=column_widths[col_index],
                        )

                entry.pack(side=customtkinter.RIGHT, padx=5, pady=4)

        for i in range(len(self.data_grid[0])):
            self.grid_frame.grid_columnconfigure(i, weight=1)
        for i in range(len(self.data_grid)):
            self.grid_frame.grid_rowconfigure(i, weight=1)

    def build_footers(self):
        cer = customtkinter.CTkLabel(self, text="@Powered by: Belp2801")
        cer.pack(padx=10, pady=4)

    # endregion

    # region utils
    def format_time(self, time, type="hms"):
        if type == "hms":
            total_seconds = int(time)
            hours = total_seconds // 3600
            remaining_seconds = total_seconds % 3600
            minutes = remaining_seconds // 60
            seconds = remaining_seconds % 60

            return f"{hours:02}:{minutes:02}:{seconds:02}"
        else:
            total_seconds = float(time) * 60 * 60
            hours = int(total_seconds // 3600)
            remaining_seconds = int(total_seconds % 3600)
            minutes = remaining_seconds // 60
            seconds = remaining_seconds % 60

            return f"{hours:02}:{minutes:02}"

    def save_latest_running_time(self):
        values = {
            key: inner_dict["start_time"] for key, inner_dict in self.data.items()
        }
        with open(self.latest_running_time_filename, "w", newline="") as f:
            writer = csv.writer(f)

            writer.writerow(values.keys())
            writer.writerow(values.values())

    def reset_all_time(self):
        for script in self.scripts.keys():
            _script = self.data[script]
            _script["start_time"] = time.time()
            _script["remain_time"] = _script["wait_time"]
            self.time_var[script].set(self.format_time(_script["remain_time"]))
        self.save_latest_running_time()

    def reset_time(self, script):
        _script = self.data[script]
        _script["start_time"] = time.time()
        _script["remain_time"] = _script["wait_time"]
        self.time_var[script].set(self.format_time(_script["remain_time"]))
        self.save_latest_running_time()

    def countdown(self):
        current_time = time.time()
        for script in self.scripts.keys():
            _script = self.data[script]
            remain = _script["wait_time"] - (current_time - _script["start_time"])
            _script["remain_time"] = remain

            if remain <= 0:
                _script["start_time"] = time.time()
                _script["remain_time"] = _script["wait_time"]
                _script["success_count"] += 1

                print("Run:", script)

                # Update latest_running_time.csv
                self.save_latest_running_time()

                # Run
                self.run(script)

            self.time_var[script].set(self.format_time(_script["remain_time"]))
            self.success_count_var[script].set(
                str(self.data[script]["success_count"]).rjust(2, "0")
            )

        self.after(1000, self.countdown)

    # endregion

    # region run
    def handle_command_execute(self, script):
        command_type = self.scripts[script]["command"]
        command_file = self.scripts[script]["file"]

        return f"{command_type} {command_file}"

    def run(self, script):
        command = self.handle_command_execute(script)
        print(command)
        os.system(f"start cmd /c {command}")

    # endregion


if __name__ == "__main__":
    app = ScriptAutoLauncher()
    app.mainloop()
