import pandas as pd
from matplotlib import pyplot as plt

from model.collections_wrapper import CollectionOfTrainingsfunktionen, CollectionOfIdealfunktionen, CollectionOfTestdaten
from util.rechner import berechne_ideale_funktionen, berechne_fitting_testdata
from persistence.repository import Repository
from util.visualisierung import plot_combined_solution


def main():
    """
    This part of the script will only be executed if the script is called directly (not by import on another script)
    """

    #########################################################
    # read Files #
    #########################################################

    # Trainingssaetze
    df_train = pd.read_csv('resources/data/train.csv')
    collection_of_trainingssaetze = CollectionOfTrainingsfunktionen(df_train)
    collection_of_trainingssaetze.visualize_collection_as_figure()

    # Idealfunktionen
    df_ideal = pd.read_csv('resources/data/ideal.csv')
    collection_of_idealfunktionen = CollectionOfIdealfunktionen(df_ideal)
    collection_of_idealfunktionen.visualize_collection_as_figure()

    # Testdaten
    df_test = pd.read_csv('resources/data/test.csv')
    collection_of_testdaten = CollectionOfTestdaten(df_test)
    collection_of_testdaten.visualize_collection_as_figure()

    #########################################################
    # Persist tables #
    #########################################################

    repo = Repository()
    repo.addDataframe(df_train, "Trainingdata")
    repo.addDataframe(df_ideal, "Idealdata")

    #########################################################
    # Calculate 4 best Idealfunktionen #
    #########################################################

    collection_of_ideale_funktionen = berechne_ideale_funktionen(
        collection_of_trainingssaetze, collection_of_idealfunktionen)
    collection_of_ideale_funktionen.visualize_collection_as_figure("Ermittelte ideale Funktionen fuer Trainingsdaten",
                                                                   True)

    for funktion in collection_of_ideale_funktionen.items:
        print("Vier maximale Abweichungen: {}".format(funktion.maximale_abweichung))

    #########################################################
    # Calculate fitting Testdata #
    #########################################################

    # Calculate
    collection_of_testdatensatz_fitting, collection_of_testdatensatz_leftovers = berechne_fitting_testdata(
        collection_of_testdaten, collection_of_ideale_funktionen)
    collection_of_testdatensatz_fitting.visualize_collection_as_figure("Fitting Testdaten")
    print("Anzahl fitting Testdaten: {}".format(len(collection_of_testdatensatz_fitting.items)))

    # Map and persist
    fitting_testdaten_entities = collection_of_testdatensatz_fitting.to_entities()
    repo.addAll(fitting_testdaten_entities)

    #########################################################
    # Visualize #
    #########################################################

    plot_combined_solution(collection_of_testdatensatz_fitting, collection_of_ideale_funktionen,
                           collection_of_testdatensatz_leftovers)

    print("Laenge: {}".format(len(collection_of_testdatensatz_fitting.items)))
    for idealfunktion in collection_of_ideale_funktionen.items:
        collection_of_single_idealfunktion = CollectionOfIdealfunktionen()
        collection_of_single_idealfunktion.items.append(idealfunktion)
        collection_of_testdaten_fitting_ideal = CollectionOfTestdaten()
        collection_of_all_testdaten = CollectionOfTestdaten()
        collection_of_all_testdaten.items = collection_of_testdaten.items.copy()
        for item in collection_of_testdatensatz_fitting.items:
            if item.ideal_funk == idealfunktion.id:
                collection_of_testdaten_fitting_ideal.add_item(item)
        collection_of_all_testdaten.subtract(collection_of_testdaten_fitting_ideal)
        print("Länge Gesamt {} | Fitting {} | Not fitting {}".format(len(collection_of_testdaten_fitting_ideal.items) + len(collection_of_all_testdaten.items), len(collection_of_testdaten_fitting_ideal.items), len(collection_of_all_testdaten.items)))

        plot_combined_solution(collection_of_testdaten_fitting_ideal, collection_of_single_idealfunktion,
                               collection_of_all_testdaten)
    # plot_each_idealfunktion_with_testdaten(collection_of_ideale_funktionen, collection_of_testdaten,
    #                                        collection_of_testdatensatz_fitting)

    plt.show()


if __name__ == "__main__":
    main()
