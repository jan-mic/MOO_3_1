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
    return result


def method_3(macierz_kosztow, popyt_odbiorcy, podaz_dostawcy):
    popyt = popyt_odbiorcy.copy()
    podaz = podaz_dostawcy.copy()
    koszty = np.array(macierz_kosztow)
    wagi = np.zeros_like(koszty)

    rows, cols = koszty.shape

    while np.any(popyt) and np.any(podaz):
        for j in range(cols):
            if popyt[j] == 0:
                continue

            min_val = float('inf')
            min_row = -1
            for i in range(rows):
                if podaz[i] > 0 and koszty[i][j] < min_val:
                    min_val = koszty[i][j]
                    min_row = i

            if min_row == -1:
                continue

            amount = min(podaz[min_row], popyt[j])
            wagi[min_row][j] = amount
            podaz[min_row] -= amount
            popyt[j] -= amount

    result = np.sum(koszty * wagi)
    print(f"Metoda 3 (min kolumny): {result}")
    return result


def method_4(macierz_kosztow, popyt_odbiorcy, podaz_dostawcy):
    popyt = popyt_odbiorcy.copy()
    podaz = podaz_dostawcy.copy()
    koszty = np.array(macierz_kosztow)
    wagi = np.zeros_like(koszty)

    rows, cols = koszty.shape
    row_done = [False] * rows
    col_done = [False] * cols

    def penalty_line(line):
        sorted_vals = sorted([v for v in line if v != float('inf')])
        if len(sorted_vals) >= 2:
            return sorted_vals[1] - sorted_vals[0]
        elif len(sorted_vals) == 1:
            return sorted_vals[0]
        else:
            return -1

    while np.any(popyt) and np.any(podaz):
        difference = []

        for i in range(rows):
            if not row_done[i]:
                line = [koszty[i][j] if not col_done[j] else float('inf') for j in range(cols)]
                difference.append(('row', i, penalty_line(line)))

        for j in range(cols):
            if not col_done[j]:
                line = [koszty[i][j] if not row_done[i] else float('inf') for i in range(rows)]
                difference.append(('col', j, penalty_line(line)))

        difference.sort(key=lambda x: x[2], reverse=True)
        choice_type, index, _ = difference[0]

        if choice_type == 'row':
            i = index
            min_cost = float('inf')
            min_j = -1
            for j in range(cols):
                if not col_done[j] and koszty[i][j] < min_cost:
                    min_cost = koszty[i][j]
                    min_j = j
            amount = min(podaz[i], popyt[min_j])
            wagi[i][min_j] = amount
            podaz[i] -= amount
            popyt[min_j] -= amount
            if podaz[i] == 0:
                row_done[i] = True
            if popyt[min_j] == 0:
                col_done[min_j] = True
        else:
            j = index
            min_cost = float('inf')
            min_i = -1
            for i in range(rows):
                if not row_done[i] and koszty[i][j] < min_cost:
                    min_cost = koszty[i][j]
                    min_i = i
            amount = min(podaz[min_i], popyt[j])
            wagi[min_i][j] = amount
            podaz[min_i] -= amount
            popyt[j] -= amount
            if podaz[min_i] == 0:
                row_done[min_i] = True
            if popyt[j] == 0:
                col_done[j] = True

    result = np.sum(koszty * wagi)
    print(f"Metoda 4 (VAM): {result}")
    return result
