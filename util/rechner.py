from copy import copy

import numpy as np

#from collections_wrapper import CollectionOfTestdaten, CollectionOfIdealfunktionen
from model.collections_wrapper import CollectionOfTestdaten, CollectionOfIdealfunktionen


def berechne_quadratische_abweichung(idealfunktion, trainingsfunktion):
    return np.square(idealfunktion.y - trainingsfunktion.y)


def berechne_abweichungen_idealfunktionen_zu_trainingsfunktion(collection_of_all_idealfunktionen, trainingsfunktion):
    for idealfunktion in collection_of_all_idealfunktionen.items:
        quadratische_abweichungen = berechne_quadratische_abweichung(idealfunktion, trainingsfunktion)
        idealfunktion.summe_abweichungen = quadratische_abweichungen.sum()
        idealfunktion.maximale_abweichung = quadratische_abweichungen.max()
    return collection_of_all_idealfunktionen


def berechne_ideale_funktionen(collection_of_trainingssaetze, collection_of_all_idealfunktionen):
    collection_of_ideale_funktionen = CollectionOfIdealfunktionen()
    for trainingsfunktion in collection_of_trainingssaetze.items:
        collection_of_all_idealfunktionen = berechne_abweichungen_idealfunktionen_zu_trainingsfunktion(
            collection_of_all_idealfunktionen, trainingsfunktion)
        ideale_funktion = copy(collection_of_all_idealfunktionen.find_funktion_min_abweichungen())

        print('Die geringste quadratische Abweichung zur Trainingsfunktion {} hat die ideale Funktion {}'.format(
            trainingsfunktion.id, ideale_funktion.id))
        collection_of_ideale_funktionen.add_item(ideale_funktion)

        print('Maximale Abweichung in idealer Funktion: {}'.format(ideale_funktion.maximale_abweichung))
        if ideale_funktion.maximale_abweichung > collection_of_ideale_funktionen.maximale_abweichung:
            collection_of_ideale_funktionen.maximale_abweichung = ideale_funktion.maximale_abweichung

    return collection_of_ideale_funktionen


def berechne_delta_zu_idealen_funktionen(testdatensatz, collection_of_ideale_funktionen):
    for idealfunktion in collection_of_ideale_funktionen.items:
        y_ideal = idealfunktion.get_y_from_x(testdatensatz.x)
        if abs(testdatensatz.y - y_ideal) <= idealfunktion.get_faktor_maximale_abweichung():
            testdatensatz.delta_y = abs(testdatensatz.y - y_ideal)
            testdatensatz.ideal_funk = idealfunktion.id
            return testdatensatz


def berechne_fitting_testdata(collection_of_testdaten, collection_of_ideale_funktionen):
    collection_of_testdatensatz_fitting = CollectionOfTestdaten()
    collection_of_testdatensatz_leftovers = CollectionOfTestdaten()
    collection_of_testdatensatz_leftovers.items = collection_of_testdaten.items.copy()
    for idealfunktion in collection_of_ideale_funktionen.items:
        for testdatensatz in collection_of_testdaten.items:
            abweichung = abs(testdatensatz.y - idealfunktion.get_y_from_x(testdatensatz.x))
            if abweichung <= idealfunktion.get_faktor_maximale_abweichung():
                testdatensatz.delta_y = abweichung
                testdatensatz.ideal_funk = idealfunktion.id
                collection_of_testdatensatz_fitting.add_item(copy(testdatensatz))
                collection_of_testdatensatz_leftovers.remove_if_present(testdatensatz)


    return collection_of_testdatensatz_fitting, collection_of_testdatensatz_leftovers


