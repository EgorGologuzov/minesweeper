import tkinter as tk


class SettingsMenu():
    def __init__(self):
        self.window = tk.Tk()
        tk.Label(self.window, text='Mode').place(x=10, y=10)
        tk.Label(self.window, text='Number of mines').place(x=10, y=115)
        tk.Label(self.window, text='Area width').place(x=10, y=140)
        tk.Label(self.window, text='Area height').place(x=10, y=165)

        self.window.wm_title('Settings')
        self.window.geometry("290x230")

        settings = open("settings.txt", "r")
        mode, num_mines, width, height = settings.read().split("\n")
        settings.close()

        self.mode_var = tk.StringVar(value=mode)
        self.btn_e = tk.Radiobutton(self.window, text="Easy", value="easy", variable=self.mode_var,
                                    command=lambda: self.set_mode("easy"))
        self.btn_e.place(x=10, y=30)
        self.btn_m = tk.Radiobutton(self.window, text="Medium", value="med", variable=self.mode_var,
                                    command=lambda: self.set_mode("med"))
        self.btn_m.place(x=10, y=50)
        self.btn_h = tk.Radiobutton(self.window, text="Hard", value="hard", variable=self.mode_var,
                                    command=lambda: self.set_mode("hard"))
        self.btn_h.place(x=10, y=70)
        self.btn_a = tk.Radiobutton(self.window, text="Author mode", value="author", variable=self.mode_var,
                                    command=lambda: self.set_mode("author"))
        self.btn_a.place(x=10, y=90)

        self.btn_save = tk.Button(text='SAVE', command=self.save)
        self.btn_save.place(x=10, y=190)

        def validate(new_value):
            self.btn_save["state"] = "normal"
            return new_value == "" or new_value.isnumeric()

        vcmd = (self.window.register(validate), '%P')

        self.entry_mine = tk.Entry(self.window, textvariable=tk.StringVar(value=num_mines),
                                   validate='key', validatecommand=vcmd, state="disabled")
        self.entry_mine.place(x=120, y=115)
        self.entry_mine.bind("<FocusOut>", self.check_value)
        self.lable_entry_mine = tk.Label(self.window)
        self.lable_entry_mine.place(x=250, y=115)

        self.entry_width = tk.Entry(self.window, textvariable=tk.StringVar(value=width),
                                    validate='key', validatecommand=vcmd, state="disabled")
        self.entry_width.place(x=120, y=140)
        self.entry_width.bind("<FocusOut>", self.check_value)

        self.entry_height = tk.Entry(self.window, textvariable=tk.StringVar(value=height),
                                     validate='key', validatecommand=vcmd, state="disabled")
        self.entry_height.place(x=120, y=165)
        self.entry_height.bind("<FocusOut>", self.check_value)

        self.check_value(None)
        self.set_mode(mode)
        self.btn_save["state"] = "disabled"
        tk.mainloop()

    def set_mode(self, mode):
        self.btn_save["state"] = "normal"
        if mode == "easy":
            self.activate_author_mode(False)
            self.entry_height["textvariable"] = tk.StringVar(value="20")
            self.entry_width["textvariable"] = tk.StringVar(value="20")
            self.entry_mine["textvariable"] = tk.StringVar(value="50")
        elif mode == "med":
            self.activate_author_mode(False)
            self.entry_height["textvariable"] = tk.StringVar(value="35")
            self.entry_width["textvariable"] = tk.StringVar(value="35")
            self.entry_mine["textvariable"] = tk.StringVar(value="230")
        elif mode == "hard":
            self.activate_author_mode(False)
            self.entry_height["textvariable"] = tk.StringVar(value="60")
            self.entry_width["textvariable"] = tk.StringVar(value="60")
            self.entry_mine["textvariable"] = tk.StringVar(value="720")
        else:
            self.activate_author_mode(True)

        self.check_value(None)

    def activate_author_mode(self, activate):
        if activate:
            self.entry_height["state"] = "normal"
            self.entry_width["state"] = "normal"
            self.entry_mine["state"] = "normal"
        else:
            self.entry_height["state"] = "disabled"
            self.entry_width["state"] = "disabled"
            self.entry_mine["state"] = "disabled"

    def check_value(self, event):
        width = int(self.entry_width.get() + "0")//10
        if width < 15:
            self.entry_width["textvariable"] = tk.StringVar(value="15")
            width = 15
        elif width > 100:
            self.entry_width["textvariable"] = tk.StringVar(value="100")
            width = 100

        height = int(self.entry_height.get() + "0")//10
        if height < 15:
            self.entry_height["textvariable"] = tk.StringVar(value="15")
            height = 15
        elif height > 100:
            self.entry_height["textvariable"] = tk.StringVar(value="100")
            height = 100

        num_mines = int(self.entry_mine.get() + "0")//10
        s = width * height
        if num_mines < s/10:
            self.entry_mine["textvariable"] = tk.StringVar(value=str(round(s/10)))
            num_mines = round(s/10)
        elif num_mines > s:
            self.entry_mine["textvariable"] = tk.StringVar(value=str(s))
            num_mines = s

        self.lable_entry_mine["text"] = str(round(num_mines/s*100)) + "%"

    def save(self):
        self.check_value(None)
        conf = open("settings.txt", "w")
        conf.write(f"{self.mode_var.get()}\n" + self.entry_mine.get() + "\n" +
                   self.entry_width.get() + "\n" + self.entry_height.get())
        conf.close()
        self.btn_save["state"] = "disabled"




