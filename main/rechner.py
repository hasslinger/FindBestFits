from functools import partial
from operator import attrgetter, is_not

import numpy as np


def berechne_quadratische_abweichung(idealfunktion, trainingsfunktion):
    return np.square(idealfunktion.y - trainingsfunktion.y)


def berechne_abweichungen_idealfunktionen_zu_trainingsfunktion(array_of_all_idealfunktionen, trainingsfunktion):
    for idealfunktion in array_of_all_idealfunktionen:
        quadratische_abweichungen = berechne_quadratische_abweichung(idealfunktion, trainingsfunktion)
        idealfunktion.summe_abweichungen = quadratische_abweichungen.sum()
        idealfunktion.maximale_abweichung = quadratische_abweichungen.max()
    return array_of_all_idealfunktionen


def find_funktion_min_abweichungen(array_of_all_idealfunktionen):
    return min(array_of_all_idealfunktionen, key=attrgetter('summe_abweichungen'))


def berechne_ideale_funktionen(array_of_trainingssaetze, array_of_all_idealfunktionen):
    ideale_funktionen = []
    maximale_abweichung = 0
    for trainingsfunktion in array_of_trainingssaetze:
        array_of_all_idealfunktionen = berechne_abweichungen_idealfunktionen_zu_trainingsfunktion(
            array_of_all_idealfunktionen, trainingsfunktion)
        ideale_funktion = find_funktion_min_abweichungen(array_of_all_idealfunktionen)

        print('Die geringste quadratische Abweichung zur Trainingsfunktion {} hat die ideale Funktion {}'.format(
            trainingsfunktion.id, ideale_funktion.id))
        ideale_funktionen.append(ideale_funktion)

        print('Maximale Abweichung in idealer Funktion: {}'.format(ideale_funktion.maximale_abweichung))
        if ideale_funktion.maximale_abweichung > maximale_abweichung:
            maximale_abweichung = ideale_funktion.maximale_abweichung

    return ideale_funktionen, maximale_abweichung


def berechne_delta_zu_idealen_funktionen(testdatensatz, array_of_ideale_funktionen, faktor_maximale_abweichung):
    for idealfunktion in array_of_ideale_funktionen:
        y_ideal = idealfunktion.get_y_from_x(testdatensatz.x)
        print('row[y] = {} | yIdeal = {} | abweichung = {}'.format(testdatensatz.y, y_ideal, testdatensatz.y - y_ideal))
        print(abs(testdatensatz.y - y_ideal) <= faktor_maximale_abweichung)
        if abs(testdatensatz.y - y_ideal) <= faktor_maximale_abweichung:
            testdatensatz.delta_y = abs(testdatensatz.y - y_ideal)
            testdatensatz.ideal_funk = idealfunktion.id
            return testdatensatz


def berechne_fitting_testdata(array_of_all_testdaten, array_of_ideale_funktionen, faktor_maximale_abweichung):
    testdatensatz_calculated = []
    for testdatensatz in array_of_all_testdaten:
        testdatensatz_calculated.append(berechne_delta_zu_idealen_funktionen(
            testdatensatz, array_of_ideale_funktionen, faktor_maximale_abweichung))

    return list(filter(partial(is_not, None), testdatensatz_calculated))
