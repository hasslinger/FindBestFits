import unittest

import pandas as pd

from model.collections_wrapper import CollectionOfTrainingsfunktionen, CollectionOfIdealfunktionen, \
    CollectionOfTestdaten
from model.funktionen import IdealFunktion, Trainingsfunktion, Testdatensatz
from util.rechner import berechne_quadratische_abweichung, berechne_absolute_abweichung, berechne_ideale_funktionen, \
    berechne_fitting_testdata


class TestRechner(unittest.TestCase):
    '''
    Testet alle Funktionen der rechner.py
    '''
    def test_berechne_quadratische_abweichung(self):
        idealfunktion = IdealFunktion(pd.Series([5, 4, 6]), pd.Series([5, 10, 0]), 'y2')
        trainingsfunktion = Trainingsfunktion(pd.Series([5, 4, 6]), pd.Series([10, 5, 0]), 'y5')
        result = berechne_quadratische_abweichung(idealfunktion, trainingsfunktion)
        expected = [25, 25, 0]
        self.assertTrue((result == expected).all())

    def test_berechne_absolute_abweichung(self):
        testdatensatz = Testdatensatz(4, 90, 1)
        idealfunktion = IdealFunktion(pd.Series([5, 4, 6]), pd.Series([5, 10, 0]), 'y2')
        result = berechne_absolute_abweichung(testdatensatz, idealfunktion)
        expected = 80
        self.assertEqual(result, expected)

    def test_berechne_ideale_funktionen(self):
        col_trainingssaetze = CollectionOfTrainingsfunktionen(
            pd.DataFrame({'x': [1, 2, 3], '1': [2, 3, 2], '2': [20, 30, 20]}))
        col_all_idealfunktionen = CollectionOfIdealfunktionen(
            pd.DataFrame({'x': [1, 2, 3], 'y1': [10, 20, 30], 'y2': [5, 6, 8], 'y3': [3, 2, 1]}))
        result = berechne_ideale_funktionen(col_trainingssaetze, col_all_idealfunktionen)
        self.assertEqual(result.items[0].id, 'y3')
        self.assertEqual(result.items[0].maximale_abweichung, 1)
        self.assertEqual(result.items[1].id, 'y1')
        self.assertEqual(result.items[1].maximale_abweichung, 100)

    def test_berechne_fitting_testdata(self):
        col_testdaten = CollectionOfTestdaten(pd.DataFrame({'x': [1, 2, 3, 4, 5], 'y': [1, 20, 3, 46, 50]}))
        col_ideale_funktionen = CollectionOfIdealfunktionen(
            pd.DataFrame(
                {'x': [1, 2, 3, 4, 5], 'y1': [10, 20, 30, 40, 0], 'y2': [5, 6, 8, 46, 0], 'y3': [3, 2, 1, 0, 0]}))
        for item in col_ideale_funktionen.items:
            item.maximale_abweichung = 3
        result_fitting, result_leftovers = berechne_fitting_testdata(col_testdaten, col_ideale_funktionen)

        self.assertEqual(len(result_fitting.items), 5)
        self.assertEqual(len(result_leftovers.items), 1)
        self.assertEqual(result_fitting.items[0].ideal_funk, 'y1')
        self.assertEqual(result_fitting.items[0].y, 20)
        self.assertEqual(result_fitting.items[1].ideal_funk, 'y2')
        self.assertEqual(result_fitting.items[1].y, 1)
        self.assertEqual(result_fitting.items[2].ideal_funk, 'y2')
        self.assertEqual(result_fitting.items[2].y, 46)
        self.assertEqual(result_fitting.items[3].ideal_funk, 'y3')
        self.assertEqual(result_fitting.items[3].y, 1)
        self.assertEqual(result_fitting.items[4].ideal_funk, 'y3')
        self.assertEqual(result_fitting.items[4].y, 3)
        self.assertEqual(result_leftovers.items[0].ideal_funk, None)
        self.assertEqual(result_leftovers.items[0].y, 50)


if __name__ == '__main__':
    unittest.main()
