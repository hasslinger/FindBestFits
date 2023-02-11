from funktionen import Testdatensatz


def convert_to_array_of_function(df, function_class):
    array_of_functions = []

    for funktionId in df.columns.drop('x').values:
        array_of_functions.append(function_class(df['x'], df[funktionId], funktionId))

    return array_of_functions


def convert_to_array_of_testdaten(df_test):
    return [(Testdatensatz(row.x, row.y, index)) for index, row in df_test.iterrows()]
