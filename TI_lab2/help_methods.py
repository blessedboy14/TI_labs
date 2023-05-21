import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import re

choices = ["Столбцовый метод", "Метод Виженера"]
alphabet = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U",
            "V", "W", "X", "Y", "Z"]

ru_alphabet = ["А", "Б", "В", "Г", "Д", "Е", "Ё", "Ж", "З", "И", "Й", "К", "Л", "М", "Н", "О", "П", "Р", "С", "Т", "У",
               "Ф", "Х", "Ц", "Ч", "Ш", "Щ", "Ъ", "Ы", "Ь", "Э", "Ю", "Я"]


def center(win):
    win.update_idletasks()
    width = win.winfo_width()
    frm_width = win.winfo_rootx() - win.winfo_x()
    win_width = width + 2 * frm_width
    height = win.winfo_height()
    titlebar_height = win.winfo_rooty() - win.winfo_y()
    win_height = height + titlebar_height + frm_width
    x = win.winfo_screenwidth() // 2 - win_width // 2 - 200
    y = win.winfo_screenheight() // 2 - win_height // 2 - 25
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    win.deiconify()


def is_valid(new_val):
    if not new_val:
        return True
    result = re.match("[01\b]+$", new_val) is not None
    if not result or len(new_val) > 27:
        return False
    return True
