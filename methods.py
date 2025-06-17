# metoda północno-zachodniego kąta

import numpy as np


def method_1(macierz_kosztow, popyt_odbiorcy, podaz_dostawcy):
    macierz_wag = [[0.0 for _ in row] for row in macierz_kosztow]
    result = 0

    for i, row in enumerate(macierz_kosztow):
        for j, col in enumerate(row):
            if podaz_dostawcy[i] <= popyt_odbiorcy[j]:
                macierz_wag[i][j] = podaz_dostawcy[i]

                popyt_odbiorcy[j] -= podaz_dostawcy[i]
                podaz_dostawcy[i] = 0
                # print(result)
            else:
                macierz_wag[i][j] = popyt_odbiorcy[j]
                podaz_dostawcy[i] -= popyt_odbiorcy[j]
                popyt_odbiorcy[j] = 0

    # for i, row in enumerate(macierz_wag):
    #     for j, col in enumerate(row):
    #         result += col * macierz_wag[i][j]

    koszty = np.array(macierz_kosztow)
    alokacja = np.array(macierz_wag)

    result = np.sum(koszty * alokacja)

    print(f'Metoda 1: {result}')

    return result
