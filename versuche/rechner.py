import numpy as np
import pandas as pd


def berechne_quadratische_abweichung(y1, y1_train):
    return np.square(y1_train - y1)


def get_testfunktion_from_trainingssatz(df_train, testfunktionId):
    return pd.DataFrame(df_train[['x', testfunktionId]]).set_axis(['x', 'y_train'], axis=1)


def berechne_abweichungen_idealfunktionen_zu_trainingsfunktion(df_ideal, testfunktion):
    mergedTestUndIdealFunktion = pd.merge(df_ideal, testfunktion, on='x', how='outer')
    idealFunktionenIds = df_ideal.columns.drop(['x']).values
    df_abweichungen = pd.DataFrame()
    for idealeFunktionId in idealFunktionenIds:
        df_abweichungen[idealeFunktionId] = berechne_quadratische_abweichung(
            mergedTestUndIdealFunktion[idealeFunktionId], mergedTestUndIdealFunktion['y_train'])
    return df_abweichungen


def berechne_ideale_funktionen(df_train, df_ideal):
    idealFunctions = []
    maximaleAbweichung = 0
    trainingsfunktionenIds = df_train.columns.drop(['x']).values

    for trainingsfunktionId in trainingsfunktionenIds:
        testfunktion = get_testfunktion_from_trainingssatz(df_train, trainingsfunktionId)

        df_abweichungen = berechne_abweichungen_idealfunktionen_zu_trainingsfunktion(df_ideal, testfunktion)

        print('Abweichungen der idealen Funktionen von der Trainingsfunktion: {}'.format(trainingsfunktionId))
        print(df_abweichungen)

        print('Die geringste quadratische Abweichung zur Trainingsfunktion {} hat die ideale Funktion {}'.format(
            trainingsfunktionId, df_abweichungen.sum().idxmin()))

        idealFunctions.append(df_abweichungen.sum().idxmin())

        print('Maximale Abweichung in idealer Funktion: {}'.format(df_abweichungen[df_abweichungen.sum().idxmin()].max()))
        maximaleAbweichungIdealerFunktion = df_abweichungen[df_abweichungen.sum().idxmin()].max()
        if maximaleAbweichungIdealerFunktion > maximaleAbweichung:
            maximaleAbweichung = maximaleAbweichungIdealerFunktion

        print('___________________')

    return idealFunctions, maximaleAbweichung


def berechne_delta_zu_idealen_funktion(row, df_ideal, maximaleAbweichung):
    idealFunktionenIds = df_ideal.columns.drop(['x']).values

    print(df_ideal)

    for idealfunktionId in idealFunktionenIds:
        yIdeal = df_ideal[df_ideal['x'] == row['x']][idealfunktionId].iloc[0]
        # print('_______________________________')
        # print(df_ideal[df_ideal['x'] == row['x']])
        # print(yIdeal)
        # print(yIdeal.info())
        # print('_______________________________')

        print('row[y] = {} | yIdeal = {} | abweichung = {}'.format(row['y'], yIdeal, row['y'] - yIdeal))
        print(abs(row['y'] - yIdeal) <= maximaleAbweichung)
        if abs(row['y'] - yIdeal) <= maximaleAbweichung:
            return abs(row['y'] - yIdeal), idealfunktionId
    return None, None


def berechne_testdaten(df_test, df_ideal, maximaleAbweichung):
    df_test_new = df_test
    df_test_new[['deltaY', 'idealfunk']] = df_test.apply(berechne_delta_zu_idealen_funktion, axis=1, result_type="expand", df_ideal=df_ideal, maximaleAbweichung=maximaleAbweichung)
    print(df_test_new.dropna())
    return df_test_new.dropna()
