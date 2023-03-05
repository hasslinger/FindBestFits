import pandas as pd
from matplotlib import pyplot as plt

from configuration.logging_configuration import log
from exception.FindBestFitsException import FindBestFitsException
from model.collections_wrapper import CollectionOfTrainingsfunktionen, CollectionOfIdealfunktionen, \
    CollectionOfTestdaten
from persistence.repository import Repository
from util.rechner import berechne_ideale_funktionen, berechne_fitting_testdata
from util.visualisierung import plot_combined_solution, plot_each_idealfunktion_mit_testdaten


def main():
    '''
    Ermittelt fuer eine Sammlung an Trainingssaetzen die jeweils best passensten Idealfunktionen.
    Anhand derer werden dann Testdaten entsprechenden Idealfunktionen zugeordnet bzw. aussortiert, wenn sie sich
    nicht an eine der Funktionen anfitten lassen.
    Die gegebenen Ausgangsdaten, sowie die ermittelten Ergebnisse werden in einer SQLite Datenbank persistiert
    und mit matplotlib visualisiert.
    '''

    #########################################################
    # read Files #
    #########################################################

    # Trainingssaetze
    df_train = pd.read_csv('../resources/data/train.csv')
    collection_of_trainingssaetze = CollectionOfTrainingsfunktionen(df_train)
    collection_of_trainingssaetze.visualize_collection_as_figure()

    # Idealfunktionen
    df_ideal = pd.read_csv('../resources/data/ideal.csv')
    collection_of_idealfunktionen = CollectionOfIdealfunktionen(df_ideal)
    collection_of_idealfunktionen.visualize_collection_as_figure()

    # Testdaten
    df_test = pd.read_csv('../resources/data/test.csv')
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
    collection_of_ideale_funktionen.visualize_collection_as_figure(
        "Ermittelte ideale Funktionen fuer Trainingsdaten", True)

    #########################################################
    # Calculate fitting Testdata #
    #########################################################

    # Calculate
    collection_of_testdatensatz_fitting, collection_of_testdatensatz_leftovers = berechne_fitting_testdata(
        collection_of_testdaten, collection_of_ideale_funktionen)
    collection_of_testdatensatz_fitting.visualize_collection_as_figure(
        "Testdaten die sich an eine Idealfunktion anpassen lassen")

    # Map and persist
    fitting_testdaten_entities = collection_of_testdatensatz_fitting.to_entities()
    repo.addAll(fitting_testdaten_entities)

    #########################################################
    # Visualize #
    #########################################################

    # All combined
    plot_combined_solution(
        collection_of_testdatensatz_fitting, collection_of_ideale_funktionen, collection_of_testdatensatz_leftovers)

    # Each Idealfunktion
    plot_each_idealfunktion_mit_testdaten(
        collection_of_testdatensatz_fitting, collection_of_ideale_funktionen, collection_of_testdaten)

    plt.show()


if __name__ == "__main__":
    try:
        main()
    except FindBestFitsException:
        log.error("Bei der Ausfuehrung des Programms ist eine checked Exception aufgetreten. Bitte pruefen!")

