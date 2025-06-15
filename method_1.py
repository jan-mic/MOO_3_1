# metoda północno-zachodniego kąta

import numpy as np

result = None

def calculate(data):
    costs_matrix = [row[:-1] for row in data[:-1]]
    popyt_odbiorcy = data[-1]
    podaz_dostawcy = [row[-1] for row in data[:-1]]
    


    check_sums(costs_matrix, podaz_dostawcy, popyt_odbiorcy)



def check_sums(costs_matrix, podaz_dostawcy, popyt_odbiorcy):
    try:
        sum_popyt = sum(int(x) if x != '' else 0 for x in popyt_odbiorcy)
        sum_podaz = sum(int(x) if x != '' else 0 for x in podaz_dostawcy)

        if sum_podaz > sum_popyt:
            #dodaj kolumne

        else:
            #dodaj wiersz
    except ValueError:
        return "Błąd: Nieprawidłowe dane w tabeli"