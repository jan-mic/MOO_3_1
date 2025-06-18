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
            else:
                macierz_wag[i][j] = popyt[j]
                podaz[i] -= popyt[j]
                popyt[j] = 0

    koszty = np.array(macierz_kosztow)
    wagi = np.array(macierz_wag)

    result = np.sum(koszty * wagi)
    print(f'Metoda 1 (pln-zach): {result}')
    print(wagi)
    print('==================================')
    return result


def method_2(macierz_kosztow, popyt_odbiorcy, podaz_dostawcy):
    macierz_wag = [[0.0 for _ in row] for row in macierz_kosztow]
    popyt = popyt_odbiorcy[:]
    podaz = podaz_dostawcy[:]

    active_rows = set(range(len(macierz_kosztow)))
    active_cols = set(range(len(macierz_kosztow[0])))

    while active_rows and active_cols:
        min_koszty = []
        for i in active_rows:
            min_cost = float('inf')
            min_j = -1
            for j in active_cols:
                if macierz_kosztow[i][j] < min_cost:
                    min_cost = macierz_kosztow[i][j]
                    min_j = j
            min_koszty.append((min_cost, i, min_j))

        min_koszt, row_idx, col_idx = min(min_koszty, key=lambda x: x[0])

        przydzial = min(podaz[row_idx], popyt[col_idx])
        macierz_wag[row_idx][col_idx] = przydzial
        podaz[row_idx] -= przydzial
        popyt[col_idx] -= przydzial

        if podaz[row_idx] == 0:
            active_rows.remove(row_idx)
        if popyt[col_idx] == 0:
            active_cols.remove(col_idx)

    koszty = np.array(macierz_kosztow)
    wagi = np.array(macierz_wag)
    result = np.sum(koszty * wagi)

    print(f"Metoda 2 (min wiersza): {result}")
    print(wagi)
    print('==================================')
    return result


def method_3(macierz_kosztow, popyt_odbiorcy, podaz_dostawcy):
    koszt = np.array(macierz_kosztow, dtype=float)
    popyt = popyt_odbiorcy[:]
    podaz = podaz_dostawcy[:]

    m, n = koszt.shape
    wagi = np.zeros((m, n))
    popyt = popyt.copy()
    podaz = podaz.copy()
    odwiedzone = np.zeros((m, n), dtype=bool)

    while any(popyt) and any(podaz):
        min_wartosc = float('inf')
        min_i = min_j = -1
        for i in range(m):
            for j in range(n):
                if not odwiedzone[i][j] and koszt[i][j] < min_wartosc:
                    min_wartosc = koszt[i][j]
                    min_i, min_j = i, j

        i, j = min_i, min_j

        ilosc = min(podaz[i], popyt[j])
        wagi[i][j] = ilosc
        podaz[i] -= ilosc
        popyt[j] -= ilosc

        if podaz[i] == 0:
            odwiedzone[i, :] = True
        if popyt[j] == 0:
            odwiedzone[:, j] = True

    koszt_calkowity = np.sum(wagi * koszt)
    print(f'Metoda 3 (min macierzy): {koszt_calkowity}')
    print(wagi)
    print('==================================')
    return koszt_calkowity
