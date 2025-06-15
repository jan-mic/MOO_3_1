import tkinter as tk
import method_1
from tkinter import simpledialog, messagebox


class TableEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Edytowalna Tabela")

        self.rows = 3
        self.cols = 4
        self.entries = []

        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill="both", expand=True)

        self.control_frame = tk.Frame(self.main_frame)
        self.control_frame.pack(side="left", anchor="n", padx=10, pady=10)

        self.add_row_btn = tk.Button(self.control_frame, text="Dodaj wiersz", command=self.add_row)
        self.add_row_btn.pack(fill="x")

        self.remove_row_btn = tk.Button(self.control_frame, text="Usuń wiersz", command=self.remove_row)
        self.remove_row_btn.pack(fill="x")

        self.add_col_btn = tk.Button(self.control_frame, text="Dodaj kolumnę", command=self.add_col)
        self.add_col_btn.pack(fill="x")

        self.remove_col_btn = tk.Button(self.control_frame, text="Usuń kolumnę", command=self.remove_col)
        self.remove_col_btn.pack(fill="x")

        # Dodanie 5 przycisków "Oblicz"
        for i in range(1, 6):
            btn = tk.Button(
                self.control_frame,
                text=f"Oblicz{i}",
                command=lambda num=i: self.calculate(num)
            )
            btn.pack(fill="x", pady=2)

        self.table_frame = tk.Frame(self.main_frame)
        self.table_frame.pack(side="left", padx=10, pady=10)

        self.vcmd = (self.root.register(self.validate_entry), '%P')

        self.draw_table()

    def calculate(self, button_num):
        if button_num == 1:
            method_1.calculate(self.get_values())
        elif button_num == 2:
            method_1.calculate()
        elif button_num == 3:
            method_1.calculate()
        elif button_num == 4:
            method_1.calculate()
        elif button_num == 5:
            method_1.calculate()

    def validate_entry(self, value):
        if value == "" or value == "-":
            return True
        try:
            int(value)
            return True
        except ValueError:
            return False

    def draw_table(self):
        for widget in self.table_frame.winfo_children():
            widget.destroy()
        self.entries = []

        # Nagłówki kolumn O1, O2, ...
        for j in range(self.cols):
            label = tk.Label(self.table_frame, text=f"O{j + 1}", width=10, relief="ridge", bd=2,
                             highlightbackground="black")
            label.grid(row=0, column=j + 1, padx=1, pady=1)

        # Nagłówek ostatniej kolumny
        label = tk.Label(self.table_frame, text="podaż", width=10, relief="ridge", bd=2, highlightbackground="blue",
                         highlightcolor="blue")
        label.grid(row=0, column=self.cols + 1, padx=1, pady=1)

        for i in range(self.rows):
            row_entries = []

            # Etykieta wiersza D1, D2, ...
            label = tk.Label(self.table_frame, text=f"D{i + 1}", width=10, relief="ridge", bd=2,
                             highlightbackground="red", highlightcolor="red")
            label.grid(row=i + 1, column=0, padx=1, pady=1)

            for j in range(self.cols):
                frame = tk.Frame(self.table_frame, bd=1, relief="solid")
                frame.grid(row=i + 1, column=j + 1, padx=1, pady=1)
                entry = tk.Entry(frame, width=10, validate='key', validatecommand=self.vcmd, bd=0)
                entry.pack(fill="both", expand=True)
                entry.insert(0, "0")
                row_entries.append(entry)

            # Ostatnia kolumna - bez czarnej obwódki
            frame = tk.Frame(self.table_frame)
            frame.grid(row=i + 1, column=self.cols + 1, padx=1, pady=1)
            entry = tk.Entry(frame, width=10, validate='key', validatecommand=self.vcmd)
            entry.pack(fill="both", expand=True)
            entry.insert(0, "0")
            row_entries.append(entry)

            self.entries.append(row_entries)

        # Dodatkowy wiersz (ostatni) - bez czarnej obwódki dla kolumny podaż
        bottom_row = []
        for j in range(self.cols):
            frame = tk.Frame(self.table_frame)
            frame.grid(row=self.rows + 1, column=j + 1, padx=1, pady=1)
            entry = tk.Entry(frame, width=10, validate='key', validatecommand=self.vcmd)
            entry.pack(fill="both", expand=True)
            entry.insert(0, "0")
            bottom_row.append(entry)

        # Komórka suma ostatniego wiersza
        frame = tk.Frame(self.table_frame, bd=2, relief="solid", highlightbackground="red", highlightcolor="red")
        frame.grid(row=self.rows + 1, column=self.cols + 1, padx=1, pady=1, sticky="nsew")
        self.sum_row_entry = tk.Entry(frame, width=10, state='readonly')
        self.sum_row_entry.pack(fill="both", expand=True)

        # Komórka suma ostatniej kolumny
        frame2 = tk.Frame(self.table_frame, bd=2, relief="solid", highlightbackground="blue", highlightcolor="blue")
        frame2.grid(row=self.rows + 1, column=self.cols + 2, padx=1, pady=1, sticky="nsew")
        self.sum_col_entry = tk.Entry(frame2, width=10, state='readonly')
        self.sum_col_entry.pack(fill="both", expand=True)

        # Label popyt
        label = tk.Label(self.table_frame, text="popyt", width=10, relief="ridge", bd=2, highlightbackground="red")
        label.grid(row=self.rows + 1, column=0, padx=1, pady=1)

        # Label suma kolumny
        label = tk.Label(self.table_frame, text="suma", width=10, relief="ridge", bd=2, highlightbackground="blue")
        label.grid(row=self.rows + 2, column=self.cols + 1, columnspan=2, padx=1, pady=1)

        self.entries.append(bottom_row)

        self.update_sums()

        # Automatically resize the window to fit the new table
        self.root.update_idletasks()
        self.root.geometry("")

    def update_sums(self):
        try:
            sum_row = sum(int(entry.get()) for entry in self.entries[-1])
            self.sum_row_entry.config(state='normal')
            self.sum_row_entry.delete(0, tk.END)
            self.sum_row_entry.insert(0, str(sum_row))
            self.sum_row_entry.config(state='readonly')

            sum_col = sum(int(row[-1].get()) for row in self.entries[:-1])
            self.sum_col_entry.config(state='normal')
            self.sum_col_entry.delete(0, tk.END)
            self.sum_col_entry.insert(0, str(sum_col))
            self.sum_col_entry.config(state='readonly')
        except:
            pass

    def add_row(self):
        self.rows += 1
        self.draw_table()

    def remove_row(self):
        if self.rows > 1:
            self.rows -= 1
            self.draw_table()

    def add_col(self):
        self.cols += 1
        self.draw_table()

    def remove_col(self):
        if self.cols > 1:
            self.cols -= 1
            self.draw_table()

    def get_values(self):
        return [[entry.get() for entry in row] for row in self.entries]


if __name__ == "__main__":
    root = tk.Tk()
    app = TableEditor(root)
    root.mainloop()
