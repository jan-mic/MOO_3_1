import tkinter as tk
import methods
from tkinter import messagebox


class TableEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Edytowalna Tabela")

        self.rows = 3
        self.cols = 4
        self.entries = []

        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill="both", expand=True)

        self.top_frame = tk.Frame(self.main_frame)
        self.top_frame.pack(side="top", fill="x")

        self.control_frame = tk.Frame(self.top_frame)
        self.control_frame.pack(side="left", padx=10, pady=10, anchor="n")

        self.add_row_btn = tk.Button(self.control_frame, text="Dodaj wiersz", command=self.add_row)
        self.add_row_btn.pack(fill="x")

        self.remove_row_btn = tk.Button(self.control_frame, text="Usuń wiersz", command=self.remove_row)
        self.remove_row_btn.pack(fill="x")

        self.add_col_btn = tk.Button(self.control_frame, text="Dodaj kolumnę", command=self.add_col)
        self.add_col_btn.pack(fill="x")

        self.remove_col_btn = tk.Button(self.control_frame, text="Usuń kolumnę", command=self.remove_col)
        self.remove_col_btn.pack(fill="x")

        self.calc_btn = tk.Button(self.control_frame, text="Oblicz", command=self.calculate)
        self.calc_btn.pack(fill="x", pady=10)

        self.results_frame = tk.LabelFrame(self.top_frame, padx=10, pady=10)
        self.results_frame.pack(side="left", padx=10, pady=10, anchor="n")

        self.result_labels = []
        self.result_entries = []
        labels = ['Płn-zach kąt', 'Min w wierszu', 'Min w macierzy', 'VAM']
        for i in range(len(labels)):
            row = tk.Frame(self.results_frame)
            row.pack(fill="x", pady=2)
            label = tk.Label(row, text=labels[i], width=12, anchor="w", relief="groove", bd=2, padx=5, pady=2)
            label.pack(side="left")
            entry = tk.Entry(row, width=15)
            entry.pack(side="left", fill="x", expand=True)
            self.result_labels.append(label)
            self.result_entries.append(entry)

        self.table_frame = tk.Frame(self.main_frame)
        self.table_frame.pack(side="top", fill="both", expand=True, padx=10, pady=10)

        self.vcmd = (self.root.register(self.validate_entry), '%P')

        self.draw_table()

    def check_sums(self, popyt_odbiorcy, podaz_dostawcy):
        try:
            sum_popyt = sum(int(x) if x != '' else 0 for x in popyt_odbiorcy)
            sum_podaz = sum(int(x) if x != '' else 0 for x in podaz_dostawcy)

            if sum_podaz > sum_popyt:
                roznica = sum_podaz - sum_popyt
                self.add_col()

                self.entries[-1][self.cols - 1].delete(0, tk.END)
                self.entries[-1][self.cols - 1].insert(0, str(roznica))

            elif sum_popyt > sum_podaz:
                roznica = sum_popyt - sum_podaz
                self.add_row()

                self.entries[-2][self.cols].delete(0, tk.END)
                self.entries[-2][self.cols].insert(0, str(roznica))

        except ValueError:
            messagebox.showerror("Błąd", "Nieprawidłowe dane w tabeli")

    def calculate(self):
        data = self.get_values()
        popyt_odbiorcy = [float(val) for val in data[-1]]
        podaz_dostawcy = [float(row[-1]) for row in data[:-1]]

        self.check_sums(popyt_odbiorcy, podaz_dostawcy)

        data = self.get_values()
        macierz_kosztow = [[float(cell) for cell in row[:-1]] for row in data[:-1]]
        popyt_odbiorcy = [float(val) for val in data[-1]]
        podaz_dostawcy = [float(row[-1]) for row in data[:-1]]

        result_1 = methods.method_1(macierz_kosztow.copy(), popyt_odbiorcy.copy(), podaz_dostawcy.copy())
        result_2 = methods.method_2(macierz_kosztow.copy(), popyt_odbiorcy.copy(), podaz_dostawcy.copy())
        result_3 = methods.method_3(macierz_kosztow.copy(), popyt_odbiorcy.copy(), podaz_dostawcy.copy())
        result_4 = methods.method_4(macierz_kosztow.copy(), popyt_odbiorcy.copy(), podaz_dostawcy.copy())
        # methods.method_22(macierz_kosztow.copy(), popyt_odbiorcy.copy(), podaz_dostawcy.copy())
        # methods.method_33(macierz_kosztow.copy(), popyt_odbiorcy.copy(), podaz_dostawcy.copy())
        # methods.metoda_min_w_kolumnie(macierz_kosztow.copy(), popyt_odbiorcy.copy(), podaz_dostawcy.copy())
        # methods.method_222(macierz_kosztow.copy(), popyt_odbiorcy.copy(), podaz_dostawcy.copy())

        self.result_entries[0].delete(0, tk.END)
        self.result_entries[0].insert(0, str(int(round(result_1))))
        self.result_entries[1].delete(0, tk.END)
        self.result_entries[1].insert(0, str(int(round(result_2))))
        self.result_entries[2].delete(0, tk.END)
        self.result_entries[2].insert(0, str(int(round(result_3))))
        self.result_entries[3].delete(0, tk.END)
        self.result_entries[3].insert(0, str(int(round(result_4))))

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

        domyslne_koszty = [
            [10, 40, 50, 20, 0],
            [20, 60, 40, 60, 0],
            [30, 30, 30, 40, 0]
        ]
        domyslne_podaze = [300, 450, 800]
        domyslne_popyt = [630, 160, 170, 340, 250]

        for j in range(self.cols):
            label = tk.Label(self.table_frame, text=f"O{j + 1}", width=10, relief="ridge", bd=2,
                             highlightbackground="black")
            label.grid(row=0, column=j + 1, padx=1, pady=1)

        label = tk.Label(self.table_frame, text="podaż", width=10, relief="ridge", bd=2, highlightbackground="blue",
                         highlightcolor="blue")
        label.grid(row=0, column=self.cols + 1, padx=1, pady=1)

        for i in range(self.rows):
            row_entries = []

            label = tk.Label(self.table_frame, text=f"D{i + 1}", width=10, relief="ridge", bd=2,
                             highlightbackground="red", highlightcolor="red")
            label.grid(row=i + 1, column=0, padx=1, pady=1)

            for j in range(self.cols):
                frame = tk.Frame(self.table_frame, bd=1, relief="solid")
                frame.grid(row=i + 1, column=j + 1, padx=1, pady=1)
                entry = tk.Entry(frame, width=10, validate='key', validatecommand=self.vcmd, bd=0)
                entry.pack(fill="both", expand=True)
                # entry.insert(0, "0")
                entry.insert(0, str(domyslne_koszty[i][j]))
                row_entries.append(entry)

            frame = tk.Frame(self.table_frame)
            frame.grid(row=i + 1, column=self.cols + 1, padx=1, pady=1)
            entry = tk.Entry(frame, width=10, validate='key', validatecommand=self.vcmd)
            entry.pack(fill="both", expand=True)
            # entry.insert(0, "0")
            entry.insert(0, str(domyslne_podaze[i]))
            row_entries.append(entry)

            self.entries.append(row_entries)

        bottom_row = []
        for j in range(self.cols):
            frame = tk.Frame(self.table_frame)
            frame.grid(row=self.rows + 1, column=j + 1, padx=1, pady=1)
            entry = tk.Entry(frame, width=10, validate='key', validatecommand=self.vcmd)
            entry.pack(fill="both", expand=True)
            # entry.insert(0, "0")
            entry.insert(0, str(domyslne_popyt[j]))
            bottom_row.append(entry)

        label = tk.Label(self.table_frame, text="popyt", width=10, relief="ridge", bd=2, highlightbackground="red")
        label.grid(row=self.rows + 1, column=0, padx=1, pady=1)

        self.entries.append(bottom_row)
        self.root.update_idletasks()
        self.root.geometry("")

    def add_row(self):
        current_data = self.get_values()
        self.rows += 1
        self.draw_table()

        for i in range(len(current_data) - 1):  # bez ostatniego popytu
            for j in range(len(current_data[i])):
                if i < len(self.entries) and j < len(self.entries[i]):
                    self.entries[i][j].delete(0, tk.END)
                    self.entries[i][j].insert(0, current_data[i][j])

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

        for i in range(len(current_data) - 1):
            for j in range(len(current_data[i]) - 1):
                self.entries[i][j].delete(0, tk.END)
                self.entries[i][j].insert(0, current_data[i][j])

            self.entries[i][self.cols].delete(0, tk.END)
            self.entries[i][self.cols].insert(0, current_data[i][-1])

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
