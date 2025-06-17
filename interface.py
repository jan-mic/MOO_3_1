import tkinter as tk
import methods
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

        # Główna rama z tabelą u góry
        self.top_frame = tk.Frame(self.main_frame)
        self.top_frame.pack(side="top", anchor="n", fill="x")

        self.control_frame = tk.Frame(self.top_frame)
        self.control_frame.pack(side="left", anchor="n", padx=10, pady=10)

        self.add_row_btn = tk.Button(self.control_frame, text="Dodaj wiersz", command=self.add_row)
        self.add_row_btn.pack(fill="x")

        self.remove_row_btn = tk.Button(self.control_frame, text="Usuń wiersz", command=self.remove_row)
        self.remove_row_btn.pack(fill="x")

        self.add_col_btn = tk.Button(self.control_frame, text="Dodaj kolumnę", command=self.add_col)
        self.add_col_btn.pack(fill="x")

        self.remove_col_btn = tk.Button(self.control_frame, text="Usuń kolumnę", command=self.remove_col)
        self.remove_col_btn.pack(fill="x")

        self.calc_btn = tk.Button(self.control_frame, text="Oblicz1", command=self.calculate)
        self.calc_btn.pack(fill="x", pady=10)

        # Pola m1 - m5 z wynikami
        self.result_labels = []
        self.result_entries = []
        for i in range(5):
            row = tk.Frame(self.control_frame)
            row.pack(fill="x", pady=1)
            label = tk.Label(row, text=f"m{i + 1}", width=4, anchor="w")
            label.pack(side="left")
            entry = tk.Entry(row, width=10)
            entry.pack(side="left", fill="x", expand=True)
            self.result_labels.append(label)
            self.result_entries.append(entry)

        self.table_frame = tk.Frame(self.top_frame)
        self.table_frame.pack(side="left", padx=10, pady=10)

        self.vcmd = (self.root.register(self.validate_entry), '%P')

        self.draw_table()

    def check_sums(self, popyt_odbiorcy, podaz_dostawcy):
        try:
            sum_popyt = sum(int(x) if x != '' else 0 for x in popyt_odbiorcy)
            sum_podaz = sum(int(x) if x != '' else 0 for x in podaz_dostawcy)

            if sum_podaz > sum_popyt:
                roznica = sum_podaz - sum_popyt
                self.add_col()  # dodaje nową kolumnę

                # Wpisujemy różnicę do ostatniego wiersza (popyt)
                self.entries[-1][self.cols - 1].delete(0, tk.END)
                self.entries[-1][self.cols - 1].insert(0, str(roznica))

            elif sum_popyt > sum_podaz:
                roznica = sum_popyt - sum_podaz
                self.add_row()  # dodaje nowy wiersz

                # Wpisujemy różnicę do ostatniej kolumny nowego wiersza (podaż)
                self.entries[-2][self.cols].delete(0, tk.END)
                self.entries[-2][self.cols].insert(0, str(roznica))

            self.update_sums()

        except ValueError:
            messagebox.showerror("Błąd", "Nieprawidłowe dane w tabeli")

    def calculate(self):
        # for i, entry in enumerate(self.result_entries):
        #     entry.delete(0, tk.END)
        #     entry.insert(0, str(i * 10))

        data = self.get_values()
        popyt_odbiorcy = [float(val) for val in data[-1]]
        podaz_dostawcy = [float(row[-1]) for row in data[:-1]]

        self.check_sums(popyt_odbiorcy, podaz_dostawcy)

        data = self.get_values()
        macierz_kosztow = [[float(cell) for cell in row[:-1]] for row in data[:-1]]
        popyt_odbiorcy = [float(val) for val in data[-1]]
        podaz_dostawcy = [float(row[-1]) for row in data[:-1]]
        # print(f'macierz kosztow: {macierz_kosztow}')

        methods.method_1(macierz_kosztow, popyt_odbiorcy, podaz_dostawcy)

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
        current_data = self.get_values()
        self.rows += 1
        self.draw_table()

        # Odtwórz tylko poprzednie dane (bez nowego wiersza)
        for i in range(len(current_data) - 1):  # bez ostatniego popytu
            for j in range(len(current_data[i])):
                if i < len(self.entries) and j < len(self.entries[i]):
                    self.entries[i][j].delete(0, tk.END)
                    self.entries[i][j].insert(0, current_data[i][j])

        # Odtwórz popyt (ostatni wiersz)
        for j in range(len(current_data[-1])):
            if j < len(self.entries[-1]):
                self.entries[-1][j].delete(0, tk.END)
                self.entries[-1][j].insert(0, current_data[-1][j])

    def remove_row(self):
        if self.rows > 1:
            current_data = self.get_values()
            self.rows -= 1
            self.draw_table()
            for i in range(min(len(current_data), self.rows + 1)):
                for j in range(len(current_data[i])):
                    if i < len(self.entries) and j < len(self.entries[i]):
                        self.entries[i][j].delete(0, tk.END)
                        self.entries[i][j].insert(0, current_data[i][j])

    def add_col(self):
        current_data = self.get_values()
        self.cols += 1
        self.draw_table()

        # Odtwórz dane bez nowej (ostatniej) kolumny
        for i in range(len(current_data) - 1):  # wiersze dostawców
            for j in range(len(current_data[i]) - 1):  # kolumny odbiorców (bez podaży)
                self.entries[i][j].delete(0, tk.END)
                self.entries[i][j].insert(0, current_data[i][j])

            # kolumna podaży (ostatnia kolumna)
            self.entries[i][self.cols].delete(0, tk.END)
            self.entries[i][self.cols].insert(0, current_data[i][-1])

        # ostatni wiersz – popyt
        for j in range(len(current_data[-1])):
            self.entries[-1][j].delete(0, tk.END)
            self.entries[-1][j].insert(0, current_data[-1][j])

    def remove_col(self):
        if self.cols > 1:
            current_data = self.get_values()
            self.cols -= 1
            self.draw_table()
            for i in range(len(current_data)):
                for j in range(min(len(current_data[i]), self.cols + 1)):
                    if i < len(self.entries) and j < len(self.entries[i]):
                        self.entries[i][j].delete(0, tk.END)
                        self.entries[i][j].insert(0, current_data[i][j])

    def get_values(self):
        return [[entry.get() for entry in row] for row in self.entries]


if __name__ == "__main__":
    root = tk.Tk()
    app = TableEditor(root)
    root.mainloop()
