from help_methods import *


class MyWindow:
    def __init__(self):
        # window
        def _onKeyRelease(event):
            ctrl = (event.state & 0x4) != 0
            if event.keycode == 88 and ctrl and event.keysym.lower() != "x":
                event.widget.event_generate("<<Cut>>")

            if event.keycode == 86 and ctrl and event.keysym.lower() != "v":
                event.widget.event_generate("<<Paste>>")

            if event.keycode == 67 and ctrl and event.keysym.lower() != "c":
                event.widget.event_generate("<<Copy>>")
        self.window = tk.Tk()
        self.window.resizable(width=False, height=False)
        self.window.bind_all("<Key>", _onKeyRelease, "+")
        self.window.title("TI_lab1")
        self.window.geometry("680x285")
        center(self.window)

        # styles
        self.frame_style = ttk.Style()
        self.frame_style.configure("My.TFrame", background="gray")

        # up frame
        self.panelFrame = ttk.Frame(self.window, height=30, style="My.TFrame")
        self.panelFrame.configure()

        # label
        self.info_label = ttk.Label(text="Введите ключ: ", width=30)

        # buttons
        self.encode_btn = ttk.Button(self.window, text="Зашифровать", takefocus=False)
        self.decode_btn = ttk.Button(self.window, text="Дешифровать", takefocus=False)
        self.loadBtn = ttk.Button(self.panelFrame, text='Load', takefocus=False)
        self.saveBtn = ttk.Button(self.panelFrame, text='Save', takefocus=False)
        self.quitBtn = ttk.Button(self.panelFrame, text='Quit', takefocus=False)

        # Entry and Text
        self.text_input = tk.Text(self.window, width=30, wrap="word")
        self.text_output = tk.Text(self.window, width=30, wrap="word")
        self.check = (self.window.register(is_valid), "%P")
        self.word_input = ttk.Entry(self.window, width=30)

        # combobox
        self.choice_var = tk.StringVar(value=choices[0])
        self.choose_method = ttk.Combobox(values=choices, textvariable=self.choice_var, state="readonly")

    # binding funcs

    def Quit(self, ev):
        self.window.destroy()

    def LoadFile(self, ev):
        fn = filedialog.Open(self.window, filetypes=[('*.txt files', '.txt')]).show()
        if fn == '':
            return
        else:
            self.text_input.insert("1.0", open(fn, "rt").read())


    def SaveFile(self, ev):
        fn = filedialog.SaveAs(self.window, filetypes=[('*.txt files', '.txt')]).show()
        if fn == '':
            return
        if not fn.endswith(".txt"):
            fn += ".txt"
        open(fn, "wt").write(self.text_output.get("1.0", tk.END))

    # filtration of input

    def take_text(self, lang):
        result = ""
        if lang == "en":
            text = self.text_input.get("1.0", tk.END)
            for i in range(len(text)):
                if re.match("[a-zA-Z]", text[i]):
                    result += text[i]
        elif lang == "ru":
            text = self.text_input.get("1.0", tk.END)
            for i in range(len(text)):
                if re.match("[а-яА-ЯЁё]", text[i]):
                    result += text[i]
        return result

    def take_key(self, lang):
        result = ""
        if lang == "en":
            key = self.word_input.get()
            for i in range(len(key)):
                if re.match("[a-zA-Z]", key[i]):
                    result += key[i]
        elif lang == "ru":
            key = self.word_input.get()
            for i in range(len(key)):
                if re.match("[а-яА-ЯЁё]", key[i]):
                    result += key[i]
        return result

    # general encode/decode

    def decode(self, ev):
        text = ""
        if self.choose_method.get() == choices[0]:
            text = self.take_text("en")
            text = self.decode_column(text.upper())
        elif self.choose_method.get() == choices[1]:
            text = self.take_text("ru")
            text = self.decode_vijener(text.upper())
        self.text_output.delete("1.0", tk.END)
        self.text_output.insert("1.0", text.upper())

    def encode(self, ev):
        text = ""
        if self.choose_method.get() == choices[0]:
            text = self.take_text("en")
            text = self.encode_column(text.upper())
        elif self.choose_method.get() == choices[1]:
            text = self.take_text("ru")
            text = self.encode_vijener(text.upper())
        self.text_output.delete("1.0", tk.END)
        self.text_output.insert("1.0", text.upper())

    # column method

    def encode_column(self, text):
        key = self.take_key("en").upper()
        key_len = len(key)
        if len(key) == 0 or len(text) == 0:
            return ""
        if len(key) > len(text):
            return ""
        if key_len == 1:
            return text
        result = ""
        count = 0
        border = 0
        char = 0
        last_key = -1
        j = 0
        while count < key_len:
            min_i = len(alphabet) - 1
            for i in range(0, key_len):
                if min_i > alphabet.index(key[i]) > border:
                    min_i = alphabet.index(key[i])
                    j = i
                elif key[i] == key[last_key] and i > last_key != i \
                        and min_i > alphabet.index(key[i]) >= border:
                    min_i = alphabet.index(key[i])
                    j = i
            last_key = j
            while j < len(text):
                char += 1
                result += text[j]
                if char % 5 == 0:
                    result += " "
                j += key_len
            border = min_i
            count += 1
        return result

    def decode_column(self, text):
        key = self.take_key("en").upper()
        key_len = len(key)
        if len(key) == 0 or len(text) == 0:
            return ""
        if len(key) > len(text):
            return ""
        if key_len == 1:
            return text
        rows = len(text) // key_len
        rows = rows + 1 if len(text) % key_len != 0 else rows
        additional_cells = len(text) % key_len
        result = ""
        matrix = []
        for i in range(rows):
            row = []
            for j in range(key_len):
                row.append("")
            matrix.append(row)
        for i in range(additional_cells):
            matrix[rows-1][i] = "1"
        border = 0
        count = 0
        curr_i = 0
        last_key = -1
        j = 0
        while count < key_len:
            min_i = len(alphabet) - 1
            for i in range(0, key_len):
                if min_i > alphabet.index(key[i]) > border:
                    min_i = alphabet.index(key[i])
                    j = i
                elif key[i] == key[last_key] and i > last_key != i \
                        and min_i > alphabet.index(key[i]) >= border:
                    min_i = alphabet.index(key[i])
                    j = i
            last_key = j
            if matrix[rows-1][j] == "1":
                for i in range(rows):
                    matrix[i][j] = text[curr_i]
                    curr_i += 1
            elif len(text) == key_len:
                matrix[0][j] = text[curr_i]
                curr_i += 1
            else:
                for i in range(rows - 1):
                    matrix[i][j] = text[curr_i]
                    curr_i += 1
            count += 1
            border = min_i
        for i in range(rows):
            for j in range(key_len):
                if matrix[i][j]:
                    result += matrix[i][j]
        return result

    # vijener's methods

    def move_key(self, key):
        result = ""
        for i in range(len(key)):
            result += ru_alphabet[(ru_alphabet.index(key[i]) + 1) % len(ru_alphabet)]
        return result

    def encode_vijener(self, text):
        key = self.take_key("ru").upper()
        key_len = len(key)
        if len(key) == 0 or len(text) == 0:
            return ""

        repeat_times = len(text)//key_len
        updated_key = key
        for i in range(repeat_times):
            updated_key += self.move_key(updated_key[-key_len::])
        updated_key = updated_key[:-(len(updated_key) - len(text))]
        result = ""
        char = 0
        for i in range(len(text)):
            char += 1
            result += ru_alphabet[(ru_alphabet.index(text[i]) + ru_alphabet.index(updated_key[i])) % len(ru_alphabet)]
            if char % 5 == 0:
                result += " "
        return result

    def decode_vijener(self, text):
        key = self.take_key("ru").upper()
        key_len = len(key)
        if len(key) == 0 or len(text) == 0:
            return ""
        repeat_times = len(text) // key_len
        updated_key = key
        for i in range(repeat_times):
            updated_key += self.move_key(updated_key[-key_len::])
        updated_key = updated_key[:-(len(updated_key) - len(text))]
        result = ""
        for i in range(len(text)):
            result += ru_alphabet[(ru_alphabet.index(text[i]) - ru_alphabet.index(updated_key[i]) + len(ru_alphabet))
                                  % len(ru_alphabet)]
        return result

    # tkinter methods to bind it all together

    def binding(self):
        self.encode_btn.bind("<Button-1>", self.encode)
        self.decode_btn.bind("<Button-1>", self.decode)
        self.loadBtn.bind("<Button-1>", self.LoadFile)
        self.saveBtn.bind("<Button-1>", self.SaveFile)
        self.quitBtn.bind("<Button-1>", self.Quit)

    def placing(self):
        self.text_input.place(x=15, y=50, height=180, width=185)
        self.text_output.place(x=400 + 75, y=50, height=180, width=185)
        self.encode_btn.place(x=250, y=135, width=180)
        self.decode_btn.place(x=250, y=175, width=180)
        self.panelFrame.pack(side='top', fill='x')
        self.loadBtn.place(x=10, y=3, width=40, height=22)
        self.saveBtn.place(x=60, y=3, width=40, height=22)
        self.quitBtn.place(x=110, y=3, width=40, height=22)
        self.word_input.place(x=240, y=95, height=22, width=200)
        self.info_label.place(x=240, y=75, height=22)
        self.choose_method.place(x=240, y=50, width=200)

    def run(self):
        self.window.mainloop()


class Main:
    def __init__(self):
        self.window = MyWindow()
        self.window.binding()
        self.window.placing()

    def main(self):
        self.window.run()


if __name__ == '__main__':
    myMain = Main()
    myMain.main()
