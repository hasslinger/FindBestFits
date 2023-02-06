import unittest
import numpy as np
import pandas as pd

from versuche.rechner import berechne_quadratische_abweichung, get_testfunktion_from_trainingssatz, \
    berechne_abweichungen_idealfunktionen_zu_trainingsfunktion, berechne_delta_zu_idealen_funktion, \
    berechne_ideale_funktionen, berechne_testdaten


class TestFunctions(unittest.TestCase):
    def test_berechne_quadratische_abweichung(self):
        y1 = np.array([1, 2, 3])
        y1_train = np.array([2, 2, 2])
        result = berechne_quadratische_abweichung(y1, y1_train)
        expected = np.array([1, 0, 1])
        self.assertTrue((result == expected).all())

        y1 = np.array([2, 4, 6])
        y1_train = np.array([1, 3, 5])
        result = berechne_quadratische_abweichung(y1, y1_train)
        expected = np.array([1, 1, 1])
        self.assertTrue((result == expected).all())

    def test_get_testfunktion_from_trainingssatz(self):
        df_train = pd.DataFrame({'x': [1, 2, 3], 'y_train1': [2, 2, 2], 'y_train2': [3, 3, 3]})
        testfunktionId = 'y_train1'
        result = get_testfunktion_from_trainingssatz(df_train, testfunktionId)
        expected = pd.DataFrame({'x': [1, 2, 3], 'y_train': [2, 2, 2]})
        self.assertTrue(result.equals(expected))

        df_train = pd.DataFrame({'x': [1, 2, 3], 'y_train1': [3, 3, 3], 'y_train2': [2, 2, 2]})
        testfunktionId = 'y_train2'
        result = get_testfunktion_from_trainingssatz(df_train, testfunktionId)
        expected = pd.DataFrame({'x': [1, 2, 3], 'y_train': [2, 2, 2]})
        self.assertTrue(result.equals(expected))

    def test_berechne_abweichungen_idealfunktionen_zu_trainingsfunktion(self):
        # Prepare test data
        df_ideal = pd.DataFrame({'x': [1, 2, 3], 'f1': [1, 2, 3], 'f2': [3, 2, 1]})
        testfunktion = pd.DataFrame({'x': [1, 2, 3], 'y_train': [2, 3, 2]})
        expected_result = pd.DataFrame({'f1': [1, 1, 4], 'f2': [1, 1, 4]})

        # Call the function and compare its result to the expected result
        result = berechne_abweichungen_idealfunktionen_zu_trainingsfunktion(df_ideal, testfunktion)
        pd.testing.assert_frame_equal(result, expected_result)

    def test_berechne_ideale_funktionen(self):
        # Prepare test data
        df_train = pd.DataFrame({'x': [1, 2, 3], 'y': [2, 3, 2]})
        df_ideal = pd.DataFrame({'x': [1, 2, 3], 'f1': [1, 2, 3], 'f2': [3, 2, 1]})
        expected_ideal_functions = ['f1']
        expected_maximal_abweichung = 4

        # Call the function and compare its result to the expected result
        ideal_functions, maximal_abweichung = berechne_ideale_funktionen(df_train, df_ideal)
        self.assertEqual(ideal_functions, expected_ideal_functions)
        self.assertEqual(maximal_abweichung, expected_maximal_abweichung)

    def test_berechne_delta_zu_idealen_funktion(self):
        # Prepare test data
        df_ideal = pd.DataFrame({'x': [1, 2, 3], 'f1': [1, 2, 3], 'f2': [3, 2, 1]})
        df_test = pd.DataFrame({'x': [2], 'y': [3]})
        maximaleAbweichung = 1
        expected_result = (0, 'f1')

        # Call the function and compare its result to the expected result
        result = berechne_delta_zu_idealen_funktion(df_test.iloc[0], df_ideal, maximaleAbweichung)
        self.assertEqual(result, expected_result)

    def test_berechne_testdaten(self):
        df_test = pd.DataFrame({'y': [1, 2, 3, 4, 5], 'x': [1, 2, 3, 4, 5]})
        df_ideal = pd.DataFrame({'y': [1, 2, 3, 4, 5], 'x': [1, 2, 3, 4, 5]})
        maximaleAbweichung = 0

        result = berechne_testdaten(df_test, df_ideal, maximaleAbweichung)
        expected = pd.DataFrame({'y': [1, 2, 3, 4, 5], 'x': [1, 2, 3, 4, 5], 'deltaY': [0, 0, 0, 0, 0], 'idealfunk': [1, 2, 3, 4, 5]})

        self.assertTrue(result.equals(expected))

    def test_berechne_testdaten_with_null_values(self):
        df_test = pd.DataFrame({'y': [1, 2, np.nan, 4, 5], 'x': [1, 2, 3, 4, 5]})
        df_ideal = pd.DataFrame({'y': [1, 2, 3, 4, 5], 'x': [1, 2, 3, 4, 5]})
        maximaleAbweichung = 0

        result = berechne_testdaten(df_test, df_ideal, maximaleAbweichung)
        expected = pd.DataFrame({'y': [1, 2, 4, 5], 'x': [1, 2, 4, 5], 'deltaY': [0, 0, 0, 0], 'idealfunk': [1, 2, 4, 5]})

        self.assertTrue(result.equals(expected))

    def test_berechne_testdaten_with_different_ideal_and_test_data(self):
        df_test = pd.DataFrame({'y': [1, 2, 3, 4, 5], 'x': [1, 2, 3, 4, 5]})
        df_ideal = pd.DataFrame({'y': [2, 3, 4, 5, 6], 'x': [1, 2, 3, 4, 5]})
        maximaleAbweichung = 1

        result = berechne_testdaten(df_test, df_ideal, maximaleAbweichung)
        expected = pd.DataFrame({'y': [2, 3, 4, 5], 'x': [1, 2, 3, 4], 'deltaY': [1, 1, 1, 1], 'idealfunk': [2, 3, 4, 5]})

        self.assertTrue(result.equals(expected))

if __name__ == '__main__':
    unittest.main()