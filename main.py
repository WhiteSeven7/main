import os
import tkinter as tk
from datetime import date


class Days:
    def __init__(self):
        self.today = date.today()
        self.that_day = date(*(int(num) for num in read_data().split('-')))
        self.period = (self.today - self.that_day).days
        self.cache = None

    def change(self):
        self.cache = self.that_day
        self.that_day = self.today
        self.period = 0

    def undo(self):
        if self.cache is None:
            return
        self.that_day = self.cache
        self.period = (self.today - self.that_day).days
        self.cache = None


def read_data():
    if not os.path.exists('data.txt'):
        with open('data.txt', 'w', encoding='utf-8') as f:
            f.write('2022-1-1')
    with open('data.txt', 'r', encoding='utf-8') as ff:
        return ff.read()


def write_data(data_: date):
    with open('data.txt', 'w', encoding='utf-8') as f:
        f.truncate()
        f.write(data_.strftime('%Y-%m-%d'))


def create_window(title: str, w, h, x=200, y=200):
    window_ = tk.Tk()
    window_.title(title)
    window_.resizable(False, False)
    window_.geometry(f'{w}x{h}+{x}+{y}')
    return window_


def create_value(days_: 'Days'):
    return tk.StringVar(value=f'您上次晒被子的日期为{days_.that_day},\n距离今天已经过{days_.period}天。')


def create_label(master, tv):
    return tk.Label(master, font=('Aril', 20), textvariable=tv)


def create_button(master, t, c):
    return tk.Button(master, text=t, font=('Aril', 16), command=c)


def write_func(days_: 'Days', value_: tk.StringVar, button_: tk.Button):
    def inner_write():
        write_data(days_.today)
        days_.change()
        value_.set(f'您上次晒被子的日期为{days_.that_day},\n距离今天已经过{days_.period}天。')
        button_.place(x=220, y=100)

    return inner_write


def quit_app(windows_):
    def inner_func():
        windows_.quit()

    return inner_func


def undo_fun(days_: 'Days', value_):
    def inner_write():
        days_.undo()
        write_data(days_.that_day)
        value_.set(f'您上次晒被子的日期为{days_.that_day},\n距离今天已经过{days_.period}天。')

    return inner_write


days = Days()

window = create_window('晒被子记录器', 500, 300)
value = create_value(days)
label = create_label(window, value)
label.place(x=30, y=0)
button_u = create_button(window, '撤销', undo_fun(days, value))
button_w = create_button(window, '记录', write_func(days, value, button_u))
button_w.place(x=120, y=100)
button_q = create_button(window, '关闭', quit_app(window))
button_q.place(x=320, y=100)
window.mainloop()
