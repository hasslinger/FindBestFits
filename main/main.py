import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

from converter import convert_to_array_of_idealfunktionen, convert_to_array_of_trainingsfunktionen, \
    convert_to_array_of_testdaten
from rechner import berechne_ideale_funktionen, berechne_fitting_testdata
from repository import Repository
from visualisierung import plot_array_of_functions, plot_combined_solution


def main():
    """
    This part of the script will only be executed if the script is called directly (not by import on another script)
    """

    #########################################################
    # read Files #
    #########################################################

    # Trainingssaetze
    df_train = pd.read_csv('../data/Beispiel-Datensätze/train.csv')
    array_of_trainingssaetze = convert_to_array_of_trainingsfunktionen(df_train)
    plot_array_of_functions(array_of_trainingssaetze, "Trainingsdatensätze", True, 0.8)

    # Idealfunktionen
    df_ideal = pd.read_csv('../data/Beispiel-Datensätze/ideal.csv')
    array_of_all_idealfunktionen = convert_to_array_of_idealfunktionen(df_ideal)
    plot_array_of_functions(array_of_all_idealfunktionen, "Bereitgestellte ideale Funktionen", False, 0.8)

    # Testdaten
    df_test = pd.read_csv('../data/Beispiel-Datensätze/test.csv')
    array_of_all_testdaten = convert_to_array_of_testdaten(df_test)
    plot_array_of_functions(array_of_all_testdaten, "Bereitgestellte Testdaten", False, 20)

    #########################################################
    # Persist tables #
    #########################################################

    repo = Repository()
    repo.addDataframe(df_train, "Trainingdata")
    repo.addDataframe(df_ideal, "Idealdata")

    #########################################################
    # Calculate 4 best Idealfunktionen #
    #########################################################

    array_of_ideale_funktionen, maximale_abweichung = berechne_ideale_funktionen(
        array_of_trainingssaetze, array_of_all_idealfunktionen)
    plot_array_of_functions(array_of_ideale_funktionen, "Ermittelte ideale Funktionen fuer Trainingsdaten",
                            True, 0.8)

    #########################################################
    # Calculate fitting Testdata #
    #########################################################

    # Calculate
    faktor_maximale_abweichung = maximale_abweichung + np.sqrt(2)
    array_of_fitting_testdaten = berechne_fitting_testdata(
        array_of_all_testdaten, array_of_ideale_funktionen, faktor_maximale_abweichung)
    print(array_of_fitting_testdaten)
    plot_array_of_functions(array_of_fitting_testdaten, "Fitting Testdaten", False, 20)

    # Map and persist
    fitting_testdaten_entities = list(map(lambda x: x.to_entity(), array_of_fitting_testdaten))
    repo.addAll(fitting_testdaten_entities)

    #########################################################
    # Visualize #
    #########################################################

    plot_combined_solution(array_of_fitting_testdaten, array_of_ideale_funktionen,
                           list(set(array_of_all_testdaten) - set(array_of_fitting_testdaten)),
                           faktor_maximale_abweichung)

    plt.show()


if __name__ == "__main__":
    main()
