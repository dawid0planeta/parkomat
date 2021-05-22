from tkinter import Entry, Tk, Label, Button
from tkinter.messagebox import showinfo
from tkinter import ttk
import tkinter as tk
from tkinter import N, W, E, S
from datetime import datetime
from parkomat.core import MoneyUnit, Parkomat

class ParkomatGUI:
    def __init__(self, master):
        self.master = master
        self._parkomat = Parkomat()
        self._curr_time_label = tk.StringVar()
        self._leave_time_label = tk.StringVar()
        self._current_registration_num = tk.StringVar()
        self._current_registration_num.set('')
        self._current_time_var = tk.StringVar()
        self._current_time_var.set(self._parkomat.curr_time.strftime("%H:%M:%S"))
        self.update_curr_time()
        self.update_leave_time()
        master.title("Parkomat")

        units = [MoneyUnit(s) for s in ['0.01', '0.02', '0.05', '0.10', '0.20', '0.50', '1.00', '2.00', '5.00', '10.00', '20.00', '50.00']]

        for i, unit in enumerate(units):
            Button(master, text="Wrzuć " + str(unit) + "zł",
            command=lambda unit=unit: self._parkomat.put_money(unit)).grid(column=0, row=i)

        Label(master, text="Podaj aktualną godzinę:").grid(column=1, row=0)
        Entry(master, textvariable=self._current_time_var).grid(column=2, row=0)
        Button(master, text="Zatwierdź", command=self.change_time).grid(column=3, row=0)

        Label(master, text="Aktualny czas:").grid(column=1, row=1)
        Label(master, textvariable=self._curr_time_label).grid(column=2, row=1)
        Label(master, text="Czas odjazdu:").grid(column=1, row=2)
        Label(master, textvariable=self._leave_time_label).grid(column=2, row=2)
        Label(master, text="Podaj numer rejestracyjny:").grid(column=1, row=3)
        Entry(master, textvariable=self._current_registration_num).grid(column=2, row=3)
        Button(master, text="Kup", command=self.confirm).grid(column=3, row=3)
        Button(master, text="Anuluj", command=self.cancel).grid(column=2, row=11)


    def update_curr_time(self):
        self._parkomat.update_time()
        self._curr_time_label.set(self._parkomat.curr_time.strftime("%a %d %b %Y %H:%M:%S"))
        self.master.after(1000, self.update_curr_time)

    def update_leave_time(self):
        self._leave_time_label.set(self._parkomat.leave_time.strftime("%a %d %b %Y %H:%M:%S"))
        self.master.after(1000, self.update_leave_time)

    def confirm(self):

        self._parkomat.registration_number = self._current_registration_num.get()
        receipt = self._parkomat.buy()
        showinfo("Paragon", "Numer rejestracyjny: {nr}\nGodzina zakupu: {order_time}\nGodzina odjazdu: {leave_time}".format(
                             nr=receipt[0],
                             order_time=receipt[1].strftime("%a %d %b %Y %H:%M:%S"),
                             leave_time=receipt[2].strftime("%a %d %b %Y %H:%M:%S")))

        self._current_registration_num.set('')

    def cancel(self):
        self._parkomat.reset()
        self._current_registration_num.set('')

    def change_time(self):
        self._parkomat.curr_time = self._current_time_var.get()