from parser import Parser, parse_line
import customtkinter as ct
from chlorophyll import CodeView
import platform, subprocess
from tkinter import INSERT, Tk
from prescribe_lexer import PrescribeLexer, PrescribeStyle
import re, os
from ordered_set import OrderedSet
from CTkMenuBar import *
from tkinter import filedialog, StringVar
from generator import generate_examples

def get_keywords():
    custom_parser = Parser()
    keywords = []
    for param, value in custom_parser.independent_params.items():
        keywords.append(param)
    return keywords


def get_current_screen_geometry():
    temp_root = Tk()
    temp_root.update_idletasks()
    #temp_root.attributes('-fullscreen', True)
    temp_root.state('zoomed')
    #print(temp_root.winfo_screenheight(), temp_root.winfo_screenwidth())
    geometry = f"{temp_root.winfo_screenwidth()}x{temp_root.winfo_screenheight()}"
    temp_root.destroy()
    return geometry


class custom_gui(ct.CTk):
    def __init__(self):
        super().__init__()

        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()

        self._geometry = get_current_screen_geometry()
        _x, _y = self._geometry.split("x")
        self.x = int(_x)
        self.y = int(_y)
        #print(x, y)

        self.title("Prescribe IDE (lite)")
        self.geometry(f"{self.x}x{self.y}")
        self.minsize(1000, 500)
        self.maxsize(self.x, self.y)
        self.after(1, self.wm_state, 'zoomed')

        self.parser = Parser()

        try:
            self.directory_path = os.path.join(os.environ['USERPROFILE'], 'Kyocera_commands')
        except KeyError:
            self.directory_path = os.path.join(os.environ['HOME'], 'Kyocera_commands')

        if not os.path.exists(self.directory_path):
            os.makedirs(self.directory_path, exist_ok=True)

        generate_examples(self.directory_path)

        self.last_space = "2.0"
        self.current_space = "2.0"
        self.separator_fg_color = "#1D1E1E"

        self.menubar = CTkMenuBar(self)
        self.file_button = self.menubar.add_cascade("File")
        self.format_button = self.menubar.add_cascade("Format")
        self.format_button.configure(command=self.format_prescribe_commands)
        self.open_directory_button = self.menubar.add_cascade("Open Command Folder")
        self.open_directory_button.configure(command=self.open_directory)

        self.file_dropdown = CustomDropdownMenu(widget=self.file_button)
        self.file_dropdown.add_option(option="New File", command=self.new_file)
        self.file_dropdown.add_option(option="Open File", command=self.open_file)
        self.file_dropdown.add_option(option="Save", command=self.save_file)
        self.file_dropdown.add_option(option="Save As", command=self.saveas_file)
        self.file_dropdown.add_separator()
        self.file_dropdown.add_option(option="Exit", command=self.destroy)

        self.menubar.configure(fg_color="#1D1E1E", corner_radius=0, border_width=4, border_color="#1D1E1E")

        self.codebox_width = int(self.x * 0.75)
        self.codebox_height = int(self.y * 0.25)
        self.codebox_frame = ct.CTkFrame(self, corner_radius=0)
        #self.codebox_frame.configure(fg_color="#282A36", border_width=15, border_color="#1D1E1E")
        self.codebox_frame.pack(side="left", anchor="n", expand=True, fill="both")

        self.lex = PrescribeLexer()
        self.style = PrescribeStyle()

        self.codebox = CodeView(self.codebox_frame, lexer=self.lex, color_scheme=self.style.style)
        self.codebox.bind("<KeyRelease>", self.key_handler)
        self.codebox.bind("<ButtonRelease-1>", self.key_handler)
        #self.codebox.configure(height=self.codebox_height)
        self.codebox.pack(expand=True, fill="both")

        self.codebox.insert("0.0", "!R!\n")
        self.codebox.insert("2.0", "\nEXIT;\n")
        self.codebox.delete("4.0", "5.0")
        #self.textbox.mark_set("insert", "%d.%d" % (2,0))
        #self.protected_lines = [1, 3]

        self.separator = ct.CTkFrame(self, corner_radius=0)
        self.separator.configure(width=4, fg_color=self.separator_fg_color)
        self.separator.pack(side="left", expand=False, fill="y")

        self.sidebar_width = int(self.x * 0.25)
        self.sidebar_height = int(self.y * 0.46)
        self.sidebar = ct.CTkFrame(self, width=self.sidebar_width, height=self.y, corner_radius=0)
        self.sidebar.pack(side="right", anchor="ne", expand=False, fill="none")

        self.search_box = ct.CTkTextbox(self.sidebar, width=self.sidebar_width, height=self.sidebar_height,
                                        corner_radius=0)
        self.search_box.insert("0.0", "- - - Command Parameters - - -")
        self.search_box.insert("2.0", self.parser.get_available_commands())
        self.search_box.configure(state="disabled", fg_color="#282A36")
        self.search_box.configure(fg_color="#282A36")
        self.search_box.pack(expand=False, fill="both")

        self.sidebar_separator = ct.CTkFrame(self.sidebar, corner_radius=0)
        self.sidebar_separator.configure(height=4, fg_color=self.separator_fg_color)
        self.sidebar_separator.pack(expand=False, fill="x")

        self.error_box = ct.CTkTextbox(self.sidebar, width=self.sidebar_width, height=self.sidebar_height,
                                       corner_radius=0)
        self.error_box.insert("0.0", "- - - Command Errors - - -\n")
        self.error_box.configure(state="disabled", fg_color="#282A36")
        self.error_box.configure(fg_color="#282A36")
        self.error_box.pack(expand=False, fill="both")

        self.codebox_separator = ct.CTkFrame(self.codebox_frame, corner_radius=0)
        self.codebox_separator.configure(height=4, fg_color=self.separator_fg_color)
        self.codebox_separator.pack(expand=False, fill="x")

        self.sending_box_height = int(self.y * 0.75)
        self.sending_box = ct.CTkFrame(self.codebox_frame, corner_radius=0, height=self.sending_box_height)
        self.sending_box.configure(fg_color="#282A36")
        self.sending_box.pack(expand=True, fill="both")
        self.sending_box.grid_propagate(False)

        self.ip_label = ct.CTkLabel(self.sending_box, corner_radius=0, text="IP(s):")
        #self.ip_label.pack(side="top", anchor="nw", padx=(10,0), pady=(10,0))
        self.ip_label.grid(row=0, column=0, sticky="nw", padx=(10,0), pady=(10,0))

        self.ip_text_var = StringVar()
        self.ip_text_var.trace_add("write", self.ip_entry_focus)
        self.ip_entry = ct.CTkEntry(self.sending_box, textvariable=self.ip_text_var, corner_radius=0, width=int(self.x * 0.75 * 0.94))
        #self.ip_entry.pack(side="top", anchor="nw", padx=(10,20), pady=(10,0), expand=True, fill="x")
        self.ip_entry.grid(row=0, column=1, sticky="nw", padx=(10, 10), pady=(10, 0), columnspan=5)
        self.ip_entry.bind("<FocusOut>", self.ip_entry_focus)

        self.ip_note = ct.CTkLabel(self.sending_box, corner_radius=0,
                                   text="(If entering multiple IPs, please use a semicolon ';' to separate them.)")
        #self.ip_note.pack(side="left", anchor="nw", padx=(10,0), pady=(10,0))
        self.ip_note.grid(row=1, column=0, sticky="nw", padx=(10, 0), pady=(0, 10), columnspan=5)

        self.lpr_status_label = ct.CTkLabel(self.sending_box, corner_radius=0, text=f"LPR Status: {self.get_lpr_status()}")
        self.lpr_status_label.grid(row=2, column=0, sticky="nw", padx=(10, 0), pady=(0, 10), columnspan=2)

        self.send_file = ct.CTkButton(self.sending_box, corner_radius=2, text="Send")
        self.send_file.grid(row=3, column=0, sticky="nw", padx=(10, 0), pady=(0, 10), columnspan=2)
        self.send_file.configure(state="disabled")

        self.line = None
        self.last_token = None
        self.current_keyword = None
        self.current_param = None
        self.current_value_1 = None
        self.current_value_2 = None
        self.current_value_3 = None
        self.frpo_loads = None
        self.param_load = None
        self.tab_width = 5
        self.prescribe_keys = self.parser.prescribe_params.keys()
        self.formatable = False

        self.current_file = None

    def open_directory(self):
        os.startfile(self.directory_path)

    def save_file(self):
        if self.current_file:
            with open(self.current_file, "w") as f:
                f.write(self.codebox.get("0.0", "end").strip())
        else:
            self.saveas_file()

    def open_file(self):
        file_path = filedialog.askopenfilename(
            initialdir=self.directory_path,
            filetypes=[("Text Files", "*.txt"), ("All files", "*.*")]
        )
        if file_path:
            self.current_file = file_path
            with open(file_path, "r") as f:
                text = f.read()

            self.codebox.delete("0.0", "end")
            self.codebox.insert("0.0", text.strip())
            self.codebox.insert(INSERT, "\n")
            self.codebox.delete(INSERT, "end")

            self.formatable = True
            self.format_prescribe_commands()

            f_name = file_path.split('/')[-1]
            self.title(f"Prescribe IDE (lite) -- {f_name}")

    def new_file(self):
        self.codebox.delete("0.0", "end")
        self.codebox.insert("0.0", "!R!\n\nEXIT;\n")
        self.codebox.delete("4.0", "end")

        self.current_file = None
        self.title("Prescribe IDE (lite)")

    def saveas_file(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            initialdir=self.directory_path,
            filetypes=[("Text Files", "*.txt"), ("All files", "*.*")],
        )
        if file_path:
            self.current_file = file_path
            with open(self.current_file, "w") as f:
                f.write(self.codebox.get("0.0", "end").strip())

            f_name = file_path.split('/')[-1]
            self.title(f"Prescribe IDE (lite) -- {f_name}")

    def get_lpr_status(self):
        system = platform.system().lower()

        if system == "windows":
            try:
                subprocess.call(['where', 'lpr'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            except subprocess.CalledProcessError:
                return "Not Enabled - Please Enable LPR"
        else:
            try:
                subprocess.call(['which', 'lpr'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            except subprocess.CalledProcessError:
                return "Not Enabled - Please Enable LPR"

        return "Enabled"

    def optionmenu_callback(self, choice):
        print("optionmenu_callback: ", choice)

    def format_prescribe_commands(self):
        if self.formatable:
            _preparsed = self.codebox.get("0.0", "end").replace(";", ";~~")
            _preparsed = _preparsed.replace("!R!", "!R!~~")
            _preparsed = _preparsed.replace("EXIT;", "~~EXIT;")

            _new_tokens = list(filter(None, _preparsed.split("\n")))
            _check_command_count = list(
                filter(None, [command.strip() for c in _new_tokens for command in c.split("~~")]))
            self.codebox.delete("0.0", "end")
            self.codebox.insert("0.0", "\n".join(_check_command_count))
            self.codebox.insert(INSERT, "\n")
            self.codebox.delete(INSERT, "end")

            self.error_box.configure(state="normal")
            self.error_box.delete("2.0", "3.0")
            self.error_box.configure(state="disabled")

            self.formatable = False
            self.handle_error_msg()

    def ip_entry_focus(self, event=None, *args):
        ip_addresses = self.ip_entry.get().strip()
        if ip_addresses:
            self.send_file.configure(state="normal")
        else:
            self.send_file.configure(state="disabled")

    def handle_error_msg(self):
        errors = parse_line(self.codebox.get("0.0", "end"))
        if errors:
            error_msg = "\n"
            for indx, error in errors:
                line_indx = self.codebox.search(indx, "0.0", stopindex="end")

                if not line_indx:
                    error_msg += "\nError at End of File\n"
                    error_msg += f"{'':>{self.tab_width}}Command: {indx}\n"
                    error_msg += f"{'':>{self.tab_width}}Error: {error}\n"
                    continue

                row = int(line_indx.split(".")[0])
                col = int(line_indx.split(".")[1])
                error_msg += f"\nError at Line {row} Char {col}\n"
                error_msg += f"{'':>{self.tab_width}}Command: {indx}\n"
                error_msg += f"{'':>{self.tab_width}}Error: {error}\n"
            if error_msg != "\n":
                self.error_box.configure(state="normal")
                self.error_box.delete("3.0", "end")
                self.error_box.insert("3.0", error_msg)
                self.error_box.configure(state="disabled")
        else:
            self.error_box.configure(state="normal")
            self.error_box.delete("3.0", "end")
            self.error_box.configure(state="disabled")

    def key_handler(self, event):

        self.current_space = self.codebox.index(INSERT)
        row, _ = self.current_space.split(".")

        end_caps = OrderedSet(["!R!", "EXIT"])
        self.line = self.codebox.get("0.0", "end").split("\n")[int(row) - 1]
        delimiters = r',|;|"| '
        tokens = OrderedSet(filter(None, re.split(delimiters, self.line))) - end_caps

        temp_tokens = self.codebox.get("0.0", "end").replace(";", ";~~").split("\n")
        _new_tokens = list(filter(None, [command.rstrip() for command in temp_tokens]))
        _check_command_count = list(filter(None, [command.rstrip() for c in _new_tokens for command in c.split("~~")]))

        if len(_new_tokens) != len(_check_command_count) and not self.formatable:
            self.error_box.configure(state="normal")
            self.error_box.insert("2.0", "Please click 'Format' for better syntax checking\n")
            self.error_box.configure(state="disabled")
            self.formatable = True

        if len(tokens) > 0:
            for indx, token in enumerate(tokens):
                if indx == 0:
                    self.current_keyword = token
                elif indx == 1:
                    self.current_param = token
        elif len(tokens) == 0:
            self.current_keyword = None
            self.current_param = None

        arrow_keys_nums = [37, 38, 39, 40]
        arrow_keys_names = ["Left", "Up", "Right", "Down"]

        separator_nums = [32, 186, 188]
        separator_names = ["space", "semicolon", "comma"]

        if event.keycode in arrow_keys_nums and event.keysym in arrow_keys_names:
            self.handle_error_msg()
        elif event.keycode in separator_nums and event.keysym in separator_names:
            self.handle_error_msg()
            self.handle_error_msg()
        elif event.keycode == 13 and event.keysym == "Return":
            row = int(row) + 1
            self.last_space = f"{row}.0"
            self.handle_error_msg()

        if self.current_keyword == "FRPO" and self.current_param is None:
            self.load_keywords_params(self.parser.frpo_params)
        elif self.current_keyword == "KCFG" and self.current_param is None:
            self.load_keywords_params(self.parser.kcfg_params)
        elif self.current_keyword in self.prescribe_keys:
            self.load_param_args(self.parser.prescribe_params)
        elif self.current_keyword is None:
            self.search_box.configure(state="normal")
            self.search_box.delete("2.0", "end")
            self.search_box.insert("2.0", self.parser.get_available_commands())
            self.search_box.configure(state="disabled")

        if self.current_keyword == "FRPO" and self.current_param is not None:
            self.load_param_args(self.parser.frpo_params)
        elif self.current_keyword == "KCFG" and self.current_param is not None:
            self.load_param_args(self.parser.kcfg_params)

    def load_keywords_params(self, keyword):
        self.param_load = "\n\n"

        for _, param in keyword.items():
            self.param_load += f"{param.get('Parameter')} - {param.get('Environment')}\n"

        self.search_box.configure(state="normal")
        self.search_box.delete("2.0", "end")
        self.search_box.insert("2.0", self.param_load)
        self.search_box.configure(state="disabled")

    def load_conditional_args(self, param_args):
        cursor_line = int(self.codebox.index(INSERT).split(".")[0])
        curr_line = self.codebox.get(f"{cursor_line}.0", f"{cursor_line + 1}.0").split("\n")[0].split(",")

        #if len(curr_line) == 1 or (len(curr_line) == 2 and curr_line[1] == ""):
        #    self.search_box.configure(state="normal")
        #    self.search_box.delete("2.0", "end")

        values = list(filter(None, curr_line[1:]))
        curr_value_options = "\n"
        curr_value_options += f"{param_args.get('Parameter')} - {param_args.get('Environment')}\n"
        curr_value_options += "-" * 50 + "\n"
        curr_value_options += f"Factory Setting: {param_args.get('Factory Setting')}\n"
        curr_value_options += f"Interface: {param_args.get('Interface')}\n"
        curr_value_options += f"Format: {param_args.get('Format')}\n"
        curr_value_options += "Values:\n"

        curr_cond_args_loaded = []

        for option in param_args["Values"]:
            if option.get("Position", -1) == 1:
                curr_value_options += self.format_options(param_args, option, 1)
                curr_cond_args_loaded.append(option)
                break

        #print(values)
        if not values:
            self.search_box.configure(state="normal")
            self.search_box.delete("2.0", "end")
            self.search_box.insert("2.0", curr_value_options)
            self.search_box.configure(state="disabled")
            return

        for pos, val in enumerate(values):
            for option in param_args["Values"]:
                if (option.get("Position", -1) == (pos + 2) and option.get("Type", "") == "enum" and
                        option.get("Parent Position", -1) == (pos + 1) and str(option.get("Parent Option", -1)) == val):
                    curr_value_options += self.format_options(param_args, option, (pos + 2))
                    curr_cond_args_loaded.append(option)
                    break
                elif (option.get("Position", -1) == (pos + 2) and option.get("Type", "") == "range" and
                        option.get("Parent Position", -1) == (pos + 1) and str(option.get("Parent Option", -1)) == val and
                        str(option.get("Grandparent Option", -1)) == values[pos - 1]):
                    curr_value_options += self.format_options(param_args, option, (pos + 2))
                    curr_cond_args_loaded.append(option)
                    break

        self.search_box.configure(state="normal")
        self.search_box.delete("2.0", "end")
        self.search_box.insert("2.0", curr_value_options)
        self.search_box.configure(state="disabled")

    def format_options(self, param_args, val, position):
        current_frpo_arg = ""
        if param_args.get("Multi-Paramater", 0) == 1:
            current_frpo_arg += f"{'':>{self.tab_width}}Parameter #{position}\n"
            self.tab_width *= 2
        if val["Type"] == "Integer":
            current_frpo_arg += f"{'':>{self.tab_width}}{val.get('Comment')}\n"
        elif val["Type"] == "enum":
            for opt_key, opt_val in val["Options"].items():
                current_frpo_arg += f"{'':>{self.tab_width}}{opt_key}: {opt_val}\n"
        elif val["Type"] == "range":
            current_frpo_arg += f"{'':>{self.tab_width}}Comment: {val.get('Comment')}\n"
            current_frpo_arg += f"{'':>{self.tab_width}}Min: {val.get('min')}\n"
            current_frpo_arg += f"{'':>{self.tab_width}}Max: {val.get('max')}\n"

        if param_args.get("Multi-Paramater", 0) == 1:
            self.tab_width /= 2

        return current_frpo_arg

    def load_param_args(self, param):
        if self.current_param in param.keys():
            self.search_box.configure(state="normal")
            self.search_box.delete("2.0", "end")
            param_args = param[self.current_param]

            if param[self.current_param].get("Conditional", 0) == 1:
                self.load_conditional_args(param_args)
                return

            current_frpo_arg = "\n\n"
            current_frpo_arg += f"{param_args.get('Parameter')} - {param_args.get('Environment')}\n"
            current_frpo_arg += "-" * 50 + "\n"
            current_frpo_arg += f"Factory Setting: {param_args.get('Factory Setting')}\n"
            current_frpo_arg += f"Interface: {param_args.get('Interface')}\n"
            current_frpo_arg += f"Format: {param_args.get('Format')}\n"
            current_frpo_arg += "Values:\n"
            for val in param_args.get("Values"):
                if param_args.get("Multi-Paramater", 0) == 1:
                    index_ = param_args["Values"].index(val) + 1
                    current_frpo_arg += f"{'':>{self.tab_width}}Parameter #{index_}\n"
                    self.tab_width *= 2
                if val["Type"] == "Integer":
                    current_frpo_arg += f"{'':>{self.tab_width}}{val.get('Comment')}\n"
                elif val["Type"] == "enum":
                    for opt_key, opt_val in val["Options"].items():
                        current_frpo_arg += f"{'':>{self.tab_width}}{opt_key}: {opt_val}\n"
                elif val["Type"] == "range":
                    current_frpo_arg += f"{'':>{self.tab_width}}Comment: {val.get('Comment')}\n"
                    current_frpo_arg += f"{'':>{self.tab_width}}Min: {val.get('min')}\n"
                    current_frpo_arg += f"{'':>{self.tab_width}}Max: {val.get('max')}\n"

                if param_args.get("Multi-Paramater", 0) == 1:
                    self.tab_width /= 2

            self.search_box.insert("2.0", current_frpo_arg)
            self.search_box.configure(state="disabled")
        elif self.current_param is None:
            self.search_box.configure(state="normal")
            self.search_box.delete("2.0", "end")
            param_args = param[self.current_keyword]

            current_frpo_arg = "\n\n"
            current_frpo_arg += f"{param_args.get('Parameter')} - {param_args.get('Environment')}\n"
            current_frpo_arg += "-" * 50 + "\n"
            current_frpo_arg += f"Factory Setting: {param_args.get('Factory Setting')}\n"
            current_frpo_arg += f"Interface: {param_args.get('Interface')}\n"
            current_frpo_arg += f"Format: {param_args.get('Format')}\n"
            current_frpo_arg += "Values:\n"
            for val in param_args.get("Values"):
                if param_args.get("Multi-Paramater", 0) == 1:
                    index_ = param_args["Values"].index(val) + 1
                    current_frpo_arg += f"{'':>{self.tab_width}}Parameter #{index_}\n"
                    self.tab_width *= 2
                if val["Type"] == "Integer":
                    current_frpo_arg += f"{'':>{self.tab_width}}{val.get('Comment')}\n"
                elif val["Type"] == "enum":
                    for opt_key, opt_val in val["Options"].items():
                        current_frpo_arg += f"{'':>{self.tab_width}}{opt_key}: {opt_val}\n"
                elif val["Type"] == "range":
                    current_frpo_arg += f"{'':>{self.tab_width}}Comment: {val.get('Comment')}\n"
                    current_frpo_arg += f"{'':>{self.tab_width}}Min: {val.get('min')}\n"
                    current_frpo_arg += f"{'':>{self.tab_width}}Max: {val.get('max')}\n"

                if param_args.get("Multi-Paramater", 0) == 1:
                    self.tab_width /= 2

            self.search_box.insert("2.0", current_frpo_arg)
            self.search_box.configure(state="disabled")
        else:
            self.load_keywords_params(param)


if __name__ == "__main__":
    app = custom_gui()
    app.mainloop()
