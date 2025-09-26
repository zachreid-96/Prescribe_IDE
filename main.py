from parser import Parser
import customtkinter as ct
from chlorophyll import CodeView
import pygments.lexers
from tkinter import INSERT, Tk
from prescribe_lexer import PrescribeLexer, PrescribeStyle

def get_keywords():
    custom_parser = Parser()
    keywords = []
    for param, value in custom_parser.independent_params.items():
        keywords.append(param)
    return keywords


def get_current_screen_geometry():
    temp_root = Tk()
    temp_root.update_idletasks()
    temp_root.attributes('-fullscreen', True)
    temp_root.state('iconic')
    geometry = temp_root.winfo_geometry()
    temp_root.destroy()
    return geometry


class custom_gui(ct.CTk):
    def __init__(self):
        super().__init__()

        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()

        self._geometry = get_current_screen_geometry()
        _x, _y = self._geometry.split("+")[0].split("x")
        x = int(_x)
        y = int(_y)
        #print(x, y)

        self.title("Digital Log Book")
        self.geometry(f"{x}x{y}")
        self.minsize(1000, 500)
        self.maxsize(x, y)
        self.after(1, self.wm_state, 'zoomed')

        self.last_space = "2.0"
        self.current_space = "2.0"

        self.sidebar_frame = ct.CTkFrame(self, height=500, width=1000, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(10, weight=1)

        self.lex = PrescribeLexer()
        self.style = PrescribeStyle()

        self.textbox = CodeView(self.sidebar_frame, lexer=self.lex, color_scheme=self.style.style)
        self.textbox.pack(fill="both", expand=True)
        self.textbox.bind("<Key>", self.key_handler)

        self.textbox.insert("0.0", "!R!\n")
        self.textbox.insert("2.0", "\nEXIT;\n")
        #self.textbox.delete("4.0", "5.0")
        #self.textbox.mark_set("insert", "%d.%d" % (2,0))

        #self.protected_lines = [1, 3]

    def key_handler(self, event):
        self.current_space = self.textbox.index(INSERT)
        row, col = self.current_space.split(".")
        '''bypass_keys = ["Left", "Up", "Right", "Down"]
        if int(row) in self.protected_lines and event.keysym not in bypass_keys:
            print(self.textbox.get("0.0", "end"))
            return "break"'''

        if event.keycode == 32 and event.keysym == "space":
            #self.current_space = self.textbox.index(INSERT)
            print("token: ", self.textbox.get(self.last_space, self.current_space))
            self.last_space = self.textbox.index(INSERT)
        elif event.keycode == 188 and event.keysym == "comma":
            print("token: ", self.textbox.get(self.last_space, self.current_space))
            pass
        elif event.keycode == 186 and event.keysym == "semicolon":
            pass
        elif event.keycode == 13 and event.keysym == "Return":
            row = int(row) + 1
            self.last_space = f"{row}.0"
            #self.protected_lines[1] += 1

if __name__ == "__main__":
    app = custom_gui()
    app.mainloop()