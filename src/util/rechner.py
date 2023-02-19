from copy import copy, deepcopy

import numpy as np

from configuration.logging_configuration import log
from model.collections_wrapper import CollectionOfTestdaten, CollectionOfIdealfunktionen


def berechne_quadratische_abweichung(idealfunktion, trainingsfunktion):
    '''
    Berechnet die quadratische Abweichung zwischen den y-Werten von zwei Funktion
    :param idealfunktion: erste Funktion
    :param trainingsfunktion: zweite Funktion
    :return: Array mit den quadratischen Abweichungen aller y-Werte
    '''
    return np.square(idealfunktion.y - trainingsfunktion.y)


def berechne_absolute_abweichung(testdatensatz, idealfunktion):
    '''
    Berechnet die absolute Abweichung zwischen den y-Werten von zwei Funktion
    :param testdatensatz: erste Funktion
    :param idealfunktion: zweite Funktion
    :return: Absolute Abweichung
    '''
    return abs(testdatensatz.y - idealfunktion.get_y_from_x(testdatensatz.x))


def berechne_abweichungen_idealfunktionen_zu_trainingsfunktion(col_all_idealfunktionen, trainingsfunktion):
    '''
    Berechnet die Abweichung aller Eintraege einer Collection von Idealfunktionen zu einer bestimmten Trainingsfunktion.
    Dabei wird die Summe der quadratischen Abweichungen und die maximale Abweichung einer Idealfunktion ermittelt und gesetzt.
    :param col_all_idealfunktionen: Collection der Idealfunktionen
    :param trainingsfunktion: Bestimmte Trainingsfunktion
    :return: Collection der Idealfunktion mit gesetzten Abweichungen
    '''
    for idealfunktion in col_all_idealfunktionen.items:
        quadratische_abweichungen = berechne_quadratische_abweichung(idealfunktion, trainingsfunktion)
        idealfunktion.summe_abweichungen = quadratische_abweichungen.sum()
        idealfunktion.maximale_abweichung = quadratische_abweichungen.max()
    return col_all_idealfunktionen


def berechne_ideale_funktionen(col_trainingssaetze, col_all_idealfunktionen):
    '''
    Berechnet fuer eine Collection von Trainingssaetzen die Idealfunktionen mit der geringsten Abweichung.
    :param col_trainingssaetze: Collection von Trainingssaetzen
    :param col_all_idealfunktionen: Collection von Idealfunktionen
    :return: Collection mit den Idealfunktionen mit der geringsten Abweichung
    '''
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


def berechne_fitting_testdata(col_testdaten, col_ideale_funktionen):
    '''
    Berechnet welche Testdaten sich an welche Idealfunktion anfitten lassen.
    Das Kriterium ist hierbei, dass die Abweichung kleiner als die maximale Abweichung der Idealfunktion
    zur Trainingsfunktion plus die Wurzel aus zwei sein muss.
    Passt ein Testdatensatz zu mehreren Idealfunktionen, wird je passender Idealfunktion ein Testdatensatz angelegt.
    Auch wir nachgehalten, welche Testdaten sich an keiner Idealfunktion anfitten lassen.
    :param col_testdaten: Collection aller Testdatensaetze
    :param col_ideale_funktionen: Collection der Idealfunktionen
    :return: Eine Collection mit den Testdaten, die sich an eine Idealfunktion fitten lassen
    und eine Collection mit den Testdaten, die zu keiner Idealfunktion passten.
    '''
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
