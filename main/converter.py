from funktionen import Trainingsfunktion, IdealFunktion, Testdatensatz


def convert_to_array_of_trainingsfunktionen(df_train):
    array_of_functions = []

    for funktionId in df_train.columns.drop('x').values:
        array_of_functions.append(Trainingsfunktion(df_train['x'], df_train[funktionId], funktionId))

    return array_of_functions


def convert_to_array_of_idealfunktionen(df_train):
    array_of_functions = []

    for funktionId in df_train.columns.drop('x').values:
        array_of_functions.append(IdealFunktion(df_train['x'], df_train[funktionId], funktionId))

    return array_of_functions


def convert_to_array_of_testdaten(df_test):
    return [(Testdatensatz(row.x, row.y, index)) for index, row in df_test.iterrows()]
