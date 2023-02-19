from copy import copy, deepcopy

import numpy as np

from configuration.logging_configuration import log
from model.collections_wrapper import CollectionOfTestdaten, CollectionOfIdealfunktionen


def berechne_quadratische_abweichung(idealfunktion, trainingsfunktion):
    return np.square(idealfunktion.y - trainingsfunktion.y)


def berechne_absolute_abweichung(testdatensatz, idealfunktion):
    return abs(testdatensatz.y - idealfunktion.get_y_from_x(testdatensatz.x))


def berechne_abweichungen_idealfunktionen_zu_trainingsfunktion(col_all_idealfunktionen, trainingsfunktion):
    for idealfunktion in col_all_idealfunktionen.items:
        quadratische_abweichungen = berechne_quadratische_abweichung(idealfunktion, trainingsfunktion)
        idealfunktion.summe_abweichungen = quadratische_abweichungen.sum()
        idealfunktion.maximale_abweichung = quadratische_abweichungen.max()
    return col_all_idealfunktionen


def berechne_ideale_funktionen(col_trainingssaetze, col_all_idealfunktionen):
    col_ideale_funktionen = CollectionOfIdealfunktionen()

    for trainingsfunktion in col_trainingssaetze.items:
        col_all_idealfunktionen = berechne_abweichungen_idealfunktionen_zu_trainingsfunktion(
            col_all_idealfunktionen, trainingsfunktion)
        ideale_funktion = copy(col_all_idealfunktionen.find_funktion_min_abweichungen())
        col_ideale_funktionen.add_item(ideale_funktion)

        log.info('Die geringste quadratische Abweichung zur Trainingsfunktion \'%s\' hat die ideale Funktion \'%s\'. '
                 'Die maximale quadratische Abweichung zwischen ihnen ist: %s',
                 trainingsfunktion.id, ideale_funktion.id, ideale_funktion.maximale_abweichung)

    return col_ideale_funktionen


def berechne_delta_zu_idealen_funktionen(testdatensatz, col_ideale_funktionen):
    for idealfunktion in col_ideale_funktionen.items:
        y_ideal = idealfunktion.get_y_from_x(testdatensatz.x)
        if abs(testdatensatz.y - y_ideal) <= idealfunktion.get_faktor_maximale_abweichung():
            testdatensatz.delta_y = abs(testdatensatz.y - y_ideal)
            testdatensatz.ideal_funk = idealfunktion.id
            return testdatensatz


def berechne_fitting_testdata(col_testdaten, col_ideale_funktionen):
    log.info('Anzahl Testdaten gesamt: %s', col_testdaten.length())
    col_testdatensatz_fitting = CollectionOfTestdaten()
    col_testdatensatz_leftovers = deepcopy(col_testdaten)
    for idealfunktion in col_ideale_funktionen.items:
        for testdatensatz in col_testdaten.items:
            abweichung = berechne_absolute_abweichung(testdatensatz, idealfunktion)
            if abweichung <= idealfunktion.get_faktor_maximale_abweichung():
                testdatensatz.delta_y = abweichung
                testdatensatz.ideal_funk = idealfunktion.id
                col_testdatensatz_fitting.add_item(copy(testdatensatz))
                col_testdatensatz_leftovers.remove_if_present(testdatensatz)

    log.info('Anzahl zugeordneter Testdaten: %s', col_testdatensatz_fitting.length())
    log.info('Anzahl nicht passender Testdaten: %s', col_testdatensatz_leftovers.length())
    return col_testdatensatz_fitting, col_testdatensatz_leftovers
