import struct

import numpy

from help_methods import *
import numpy as np


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
        self.info_label = ttk.Label(text="Введите начальное состояние(27 символов): ", width=45)

        # buttons
        self.encode_btn = ttk.Button(self.window, text="Зашифровать", takefocus=False)
        self.decode_btn = ttk.Button(self.window, text="Дешифровать", takefocus=False)
        self.loadBtn = ttk.Button(self.panelFrame, text='Load', takefocus=False)
        self.saveBtn = ttk.Button(self.panelFrame, text='Save', takefocus=False)
        self.quitBtn = ttk.Button(self.panelFrame, text='Load Key', takefocus=False)

        # Entry and Text
        self.text_input = tk.Text(self.window, width=30, wrap="word",)
        self.text_output = tk.Text(self.window, width=30, wrap="word")
        self.key_output = tk.Text(self.window, width=25, wrap="word")
        self.check = (self.window.register(is_valid), "%P")
        self.word_input = ttk.Entry(self.window, width=30, validate="key", validatecommand=self.check)

        # some stuff
        self.polynomial = 'x^27 + x^8 + x^7 + x^1 + 1'
        self.poly = [27, 8, 7, 1]
        # self.poly = [4, 1]
        self.input_combo = []
        self.max = self.poly[0]
        self.start = self.input_combo.copy()

    # binding funcs

    def Quit(self, ev):
        fn = filedialog.Open(self.window, filetypes=[('*.txt files', '.txt')]).show()
        if fn == '':
            return
        else:
            self.word_input.delete("0", tk.END)
            self.word_input.insert("0", open(fn, "rt").read())

    def LoadFile(self, ev):
        fn = filedialog.Open(self.window, filetypes=[('*.txt files', '.txt'), ('*.jpg file', '.jpg'),
                                                     ('*.png file', '.png')]).show()
        if fn == '':
            return
        else:
            self.dtype = np.dtype('B')
            self.text_input.delete("1.0", tk.END)
            numpy_data = np.fromfile(fn, self.dtype)
            self.bye = bytes()
            string = ""
            for num in np.ndenumerate(numpy_data):
                self.bye += bytes(numpy.binary_repr(num[1], width=8), encoding='utf-8')
                string += numpy.binary_repr(num[1], width=8) + " "
                # input_data.append(numpy.binary_repr(num[1], width=8))
            # string = ""
            # for st in input_data:
            #     self.bye += bytes(st, encoding='utf-8')
            #     string += st + " "
            self.text_input.insert("1.0", string)

    def SaveFile(self, ev):
        fn = filedialog.SaveAs(self.window, filetypes=[('*.txt files', '.txt')]).show()
        if fn == '':
            return
        if not fn.endswith(".txt"):
            fn += ".txt"
        output_text = self.text_output.get("1.0", tk.END)
        open(fn, "wt").write(output_text)

    # generator

    def shift(self, arr):
        for i in range(len(arr) - 1):
            arr[i] = arr[i + 1]
        arr[len(arr) - 1] = 0
        return arr

    def loop(self, length):
        count = 0
        result = []
        inp_len = len(self.input_combo)
        while count < length - 1:
            result.append(self.input_combo[0])
            b = np.logical_xor(self.input_combo[inp_len - self.poly[0]], self.input_combo[inp_len-self.poly[1]])
            if len(self.poly) > 2:
                for i in range(2, len(self.poly)):
                    b = np.logical_xor(self.input_combo[inp_len-self.poly[i]], b)
            self.input_combo = self.shift(self.input_combo)
            self.input_combo[inp_len - 1] = 0 if not b else 1
            count += 1
        result.append(self.input_combo[0])
        return result

    # main encode and decode

    def take_text(self,):
        text = self.text_input.get("1.0", tk.END)
        result = ""
        for i in range(len(text)):
            if re.match("[01\b]+$", text[i]):
                result += text[i]
        return result

    def xor(self, data, key):
        import numpy, math

        dt = numpy.dtype('B')

        arr = numpy.bitwise_xor(numpy.fromstring(key, dtype=dt), numpy.fromstring(data, dtype=dt))

        return numpy.packbits(arr, bitorder="little")

    def encode(self, ev):
        start_seq = self.word_input.get()
        self.input_combo = []
        for k in start_seq:
            if k.isdigit():
                self.input_combo.append(int(k))
        start_len = len(start_seq)
        if start_len != self.poly[0]:
            self.word_input.delete("0", tk.END)
            return
        text_inp = self.take_text()
        if len(text_inp) == 0:
            return
        key = self.loop(len(text_inp))
        key_byte = bytes(key)
        print(self.xor(self.bye, key_byte))
        self.key_output.delete("1.0", tk.END)
        self.key_output.insert("1.0", "".join(str(x) for x in key))
        result = ""
        count = 0
        for j in range(len(text_inp)):
            if np.logical_xor(int(text_inp[j]), key[j]):
                result = ''.join([result, str(1)])
            else:
                result = ''.join([result, str(0)])
            count += 1
            if count % 8 == 0 and j != 0:
                result += " "
        self.text_output.delete("1.0", tk.END)
        self.text_output.insert("1.0", result)

    # tkinter methods to bind it all together

    def binding(self):
        self.encode_btn.bind("<Button-1>", self.encode)
        self.decode_btn.bind("<Button-1>", self.encode)
        self.loadBtn.bind("<Button-1>", self.LoadFile)
        self.saveBtn.bind("<Button-1>", self.SaveFile)
        self.quitBtn.bind("<Button-1>", self.Quit)

    def placing(self):
        self.text_input.place(x=15, y=50, height=180, width=185)
        self.text_output.place(x=400 + 75, y=50, height=180, width=190)
        self.key_output.place(x=220, y=185, height=90, width=235)
        self.encode_btn.place(x=250, y=105, width=180)
        self.decode_btn.place(x=250, y=145, width=180)
        self.panelFrame.pack(side='top', fill='x')
        self.loadBtn.place(x=10, y=3, width=40, height=22)
        self.saveBtn.place(x=60, y=3, width=40, height=22)
        self.quitBtn.place(x=110, y=3, width=70, height=22)
        self.word_input.place(x=240, y=70, height=22, width=200)
        self.info_label.place(x=225, y=50, height=22)

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
