# metoda północno-zachodniego kąta

import numpy as np


def method_1(macierz_kosztow, popyt_odbiorcy, podaz_dostawcy):
    macierz_wag = [[0.0 for _ in row] for row in macierz_kosztow]
    popyt = popyt_odbiorcy[:]
    podaz = podaz_dostawcy[:]

    for i, row in enumerate(macierz_kosztow):
        for j, col in enumerate(row):
            if podaz[i] <= popyt[j]:
                macierz_wag[i][j] = podaz[i]

                popyt[j] -= podaz[i]
                podaz[i] = 0
                # print(result)
            else:
                macierz_wag[i][j] = popyt[j]
                podaz[i] -= popyt[j]
                popyt[j] = 0

    # for i, row in enumerate(macierz_wag):
    #     for j, col in enumerate(row):
    #         result += col * macierz_wag[i][j]

    koszty = np.array(macierz_kosztow)
    wagi = np.array(macierz_wag)

    result = np.sum(koszty * wagi)

    print(f'Metoda 1: {result}')

    return result


def method_2(macierz_kosztow, popyt_odbiorcy, podaz_dostawcy):
    # Inicjalizacja macierzy alokacji (taka sama wielkość jak macierz kosztów)
    macierz_wag = [[0.0 for _ in row] for row in macierz_kosztow]

    # Kopie, by nie zmieniać oryginalnych danych
    popyt = popyt_odbiorcy[:]
    podaz = podaz_dostawcy[:]

    # Wiersze i kolumny dostępne (indeksy)
    active_rows = set(range(len(macierz_kosztow)))
    active_cols = set(range(len(macierz_kosztow[0])))

    while active_rows and active_cols:
        # Szukaj minimum w każdym wierszu (spośród dostępnych kolumn)
        min_koszty = []
        for i in active_rows:
            min_cost = float('inf')
            min_j = -1
            for j in active_cols:
                if macierz_kosztow[i][j] < min_cost:
                    min_cost = macierz_kosztow[i][j]
                    min_j = j
            min_koszty.append((min_cost, i, min_j))

        # Wybierz wiersz z najmniejszym takim kosztem
        min_koszt, row_idx, col_idx = min(min_koszty, key=lambda x: x[0])

        # Ile możemy przydzielić
        przydzial = min(podaz[row_idx], popyt[col_idx])
        macierz_wag[row_idx][col_idx] = przydzial
        podaz[row_idx] -= przydzial
        popyt[col_idx] -= przydzial

        # Usuń z aktywnych jeśli wyczerpany popyt lub podaż
        if podaz[row_idx] == 0:
            active_rows.remove(row_idx)
        if popyt[col_idx] == 0:
            active_cols.remove(col_idx)

    # Oblicz końcowy koszt
    koszty = np.array(macierz_kosztow)
    wagi = np.array(macierz_wag)
    result = np.sum(koszty * wagi)

    print(f"Metoda 2: {result}")
    return result


# def method_22(macierz_kosztow, popyt_odbiorcy, podaz_dostawcy):
#     macierz_wag = [[0.0 for _ in row] for row in macierz_kosztow]
#     popyt = popyt_odbiorcy[:]
#     podaz = podaz_dostawcy[:]
#     koszty = np.array(macierz_kosztow)
#     koszty = np.sort(koszty)
#     print(koszty)
#
#     for i, row in enumerate(koszty):
#         row_sorted = np.sort(row)
#         for j, col in enumerate(row):
#             if col > 0:
#                 if podaz[i] <= popyt[j]:
#                     macierz_wag[i][j] = podaz[i]
#
#                     popyt[j] -= podaz[i]
#                     podaz[i] = 0

# def method_23(macierz_kosztow, popyt_odbiorcy, podaz_dostawcy):
#     # Kopie wejściowych list, by ich nie zmieniać
#     popyt = popyt_odbiorcy.copy()
#     podaz = podaz_dostawcy.copy()
#     koszty = np.array(macierz_kosztow)
#     wagi = np.zeros_like(koszty)
#
#     rows, cols = koszty.shape
#
#     while np.any(popyt) and np.any(podaz):
#         # Szukamy minimalnego kosztu w każdym wierszu i przypisujemy transport
#         for i in range(rows):
#             if podaz[i] == 0:
#                 continue
#
#             # Znajdź kolumnę z minimalnym kosztem w wierszu i, gdzie popyt > 0
#             min_val = float('inf')
#             min_col = -1
#             for j in range(cols):
#                 if popyt[j] > 0 and koszty[i][j] < min_val:
#                     min_val = koszty[i][j]
#                     min_col = j
#
#             if min_col == -1:
#                 continue  # brak dostępnego popytu w tym wierszu
#
#             # przypisz minimum(podaż, popyt)
#             amount = min(podaz[i], popyt[min_col])
#             wagi[i][min_col] = amount
#             podaz[i] -= amount
#             popyt[min_col] -= amount
#
#     result = np.sum(koszty * wagi)
#     print(f"2. Metoda minimalnego elementu w wierszu: {result}")
#     return result

def method_3(macierz_kosztow, popyt_odbiorcy, podaz_dostawcy):
    # Kopie wejściowych list, by ich nie zmieniać
    popyt = popyt_odbiorcy.copy()
    podaz = podaz_dostawcy.copy()
    koszty = np.array(macierz_kosztow)
    wagi = np.zeros_like(koszty)

    rows, cols = koszty.shape

    while np.any(popyt) and np.any(podaz):
        # Szukamy minimalnego kosztu w każdej kolumnie i zapisujemy pozycje
        for j in range(cols):
            if popyt[j] == 0:
                continue

            # znajdź rząd z minimalnym kosztem w kolumnie j, gdzie podaż > 0
            min_val = float('inf')
            min_row = -1
            for i in range(rows):
                if podaz[i] > 0 and koszty[i][j] < min_val:
                    min_val = koszty[i][j]
                    min_row = i

            if min_row == -1:
                continue  # nie ma dostępnej podaży w tej kolumnie

            # przypisz minimum(podaż, popyt)
            amount = min(podaz[min_row], popyt[j])
            wagi[min_row][j] = amount
            podaz[min_row] -= amount
            popyt[j] -= amount

    result = np.sum(koszty * wagi)
    print(f"Metoda 3: {result}")
    return result
