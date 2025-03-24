from tkinter import ttk
import tkinter as tk
class styles:
    def __init__(self):
        self.theme_var = tk.StringVar(value="dark")
    # Configure styles
    def configure_styles(self):
        style = ttk.Style()
        style.theme_use('clam')  # Use the 'clam' theme as a base

        if self.theme_var.get() == "dark":
            self.apply_dark_theme(style)
        else:
            self.apply_light_theme(style)

    def apply_dark_theme(self, style):
        style.configure('TFrame', background='#2E3440')
        style.configure('TLabel', background='#2E3440', foreground='#D8DEE9', font=('Helvetica', 12))
        style.configure('TButton', background='#4C566A', foreground='#D8DEE9', font=('Helvetica', 12), borderwidth=1)
        style.map('TButton', background=[('active', '#5E81AC')])
        style.configure('TEntry', fieldbackground='#3B4252', foreground='#D8DEE9', font=('Helvetica', 12))
        style.configure('TCombobox', fieldbackground='#3B4252', foreground='#D8DEE9', font=('Helvetica', 12))
        style.map('TCombobox', fieldbackground=[('readonly', '#3B4252')])
        style.configure('TRadiobutton', background='#2E3440', foreground='#D8DEE9', font=('Helvetica', 12))
        style.configure('TCheckbutton', background='#2E3440', foreground='#D8DEE9', font=('Helvetica', 12))
        style.configure('Horizontal.TProgressbar', background='#5E81AC', troughcolor='#3B4252', thickness=20)

    def apply_light_theme(self, style):
        style.configure('TFrame', background='#FFFFFF')
        style.configure('TLabel', background='#FFFFFF', foreground='#000000', font=('Helvetica', 12))
        style.configure('TButton', background='#E0E0E0', foreground='#000000', font=('Helvetica', 12), borderwidth=1)
        style.map('TButton', background=[('active', '#0078D7')])
        style.configure('TEntry', fieldbackground='#F0F0F0', foreground='#000000', font=('Helvetica', 12))
        style.configure('TCombobox', fieldbackground='#F0F0F0', foreground='#000000', font=('Helvetica', 12))
        style.map('TCombobox', fieldbackground=[('readonly', '#F0F0F0')])
        style.configure('TRadiobutton', background='#FFFFFF', foreground='#000000', font=('Helvetica', 12))
        style.configure('TCheckbutton', background='#FFFFFF', foreground='#000000', font=('Helvetica', 12))
        style.configure('Horizontal.TProgressbar', background='#0078D7', troughcolor='#E0E0E0', thickness=20)
