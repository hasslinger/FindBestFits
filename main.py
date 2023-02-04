import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import visualisierung
import description
from rechner import berechne_ideale_funktionen, berechne_testdaten
from repository import Repository
from funktion_classes import Testfunktion, Testdaten



def main():
    """
    This part of the script will only be executed if the script is called directly (not by import on another script)
    """

    print("Starting Programm ...")

    # read Files
    df_train = pd.read_csv('data/Beispiel-Datensätze/train.csv')
    df_ideal = pd.read_csv('data/Beispiel-Datensätze/ideal.csv')
    df_test = pd.read_csv('data/Beispiel-Datensätze/test.csv')
    # infos
    description.describe(df_train, 'Trainingsdatensaetze')
    description.describe(df_ideal, 'Ideale Funktionen')
    description.describe(df_test, 'Testdatensatz')

    # plot
    visualisierung.plot_train(df_train)
    visualisierung.plot_ideal(df_ideal)
    visualisierung.plot_test(df_test)

    ############################################################

    # Laden der Daten in DB-Tabellen (1&2)
    repo = Repository()
    repo.addDataframe(df_train, "Testfunktion")
    repo.addDataframe(df_ideal, "Idealfunktion")
    #repo.addDataframe(df_test, "Testdaten")

    # Testdaten in andere CSV-Datei schreiben wenn sie Kriterium erfuellen

    ##########################################################

    # Berechne vier ideale Funktionen, die den kleinsten least_squared haben
    idealeFunktionenIds, maximaleAbweichung = berechne_ideale_funktionen(df_train, df_ideal)

    print('Die idealen Funktionen haben folgende ids: {}'.format(idealeFunktionenIds))

    idealeFunktionenIds.append('x')
    visualisierung.plot_ideal(df_ideal[idealeFunktionenIds])
    plt.show()


    ########################################################

    faktorMaximaleAbweichung = maximaleAbweichung + np.sqrt(2)
    df_cleaned_testdata = berechne_testdaten(df_test, df_ideal[idealeFunktionenIds], faktorMaximaleAbweichung)
    visualisierung.plot_cleaned_test(df_cleaned_testdata[['x', 'y', 'idealfunk']])
    plt.show()

    ###########################################################

    repo.addDataframe(df_cleaned_testdata, "Testdaten")


if __name__ == "__main__":
    main()
