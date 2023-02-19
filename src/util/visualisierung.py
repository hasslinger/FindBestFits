from copy import deepcopy

from matplotlib import pyplot as plt
from matplotlib.legend_handler import HandlerTuple

from configuration.logging_configuration import log
from exception.FindBestFitsException import FindBestFitsException


def plot_array_of_functions(array_of_functions, title, legend, groesse):
    '''
    Plottet alle Funktionen eines Typs mit deren jeweiliger plot Funktion zusammen in einer Grafik.
    :param array_of_functions: Das Array mit den Funktionen
    :param title: Der Titel des Diagramms
    :param legend: Boolean ob eine Legende angezeigt werden soll
    :param groesse: Die Groesse des jeweiligen Plotelements (z.B. linewidth oder size)
    '''
    plt.figure()
    plt.style.use('default')
    for given_function in array_of_functions:
        given_function.plot(legend, groesse)
    plt.title(title)
    plt.xlabel('X')
    plt.ylabel('Y')
    if legend:
        plt.legend(loc='best', markerscale=6)
    plt.ylim(top=110)
    plt.ylim(bottom=-25)
    plt.grid(alpha=0.4)
    plt.show(block=False)


def plot_combined_solution(collection_of_fitting_testdaten, collection_of_ideale_funktionen,
                           collection_of_all_testdaten_not_fitting, colors=None):
    '''
    Plottet mehrere Funktionsarten zusammen in einem Plot.
    Es werden passende und nicht passende Testdaten als Scatterplot visualisiert und gleichzeitig verschiedene
    Idealfunktionen als Liniendiagramme dargestellt.
    Dabei wird über die verschiedenen Funktionstypen bzw. Typen von Plotelementen ein einheitliches Farbschema
    verwendet, sodass Testdaten den zugehörigen Idealfunktionen zugeordnet werden koennen.
    Nicht passende Testdaten werden grau eingefaerbt.
    :param collection_of_fitting_testdaten: Collection der zugeordneten Testdaten
    :param collection_of_ideale_funktionen: Collection der idealen Funktionen
    :param collection_of_all_testdaten_not_fitting: Collection der nicht passenden Testdaten
    :param colors: Optionaler Parameter zum Festlegen der Farben je IdealfunktionId
    '''
    plt.style.use('default')
    if colors is None:
        colors = collection_of_ideale_funktionen.get_color_dict()
    fig, ax = plt.subplots()
    handles, labels = ax.get_legend_handles_labels()
    ax.legend([tuple(handles[::2]), tuple(handles[1::2])], labels[:2], handlelength=3,
              handler_map={tuple: HandlerTuple(ndivide=None)})
    collection_of_fitting_testdaten.plot_all_items(colors)
    collection_of_all_testdaten_not_fitting.plot_all_items('grey')
    collection_of_ideale_funktionen.plot_all_items(colors)

    plt.title("Darstellung der idealen Testfunktionen und die zugehoerigen Testdaten")
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.legend(loc='best', markerscale=8)
    plt.ylim(top=110)
    plt.ylim(bottom=-25)
    plt.grid(alpha=0.4)
    plt.show(block=False)


def plot_each_idealfunktion_mit_testdaten(collection_of_testdatensatz_fitting, collection_of_ideale_funktionen,
                                          collection_of_testdaten):
    '''
    Plottet mehrere Idealfunktionen mit einem Diagramm pro Funktion.
    Dabei werden jeweils die der Idealfunktion zugeordneten und nicht zugeordnet Testdaten entsprechend farblich ergaenzt.
    Ueber die verschiedenen Plots hinweg werden unterschiedliche Farben genutzt, die zur bisherigen Visualisierung der
    verschiedenen Idealfunktionen passt.
    :param collection_of_testdatensatz_fitting: Collection der zugeordneten Testdaten
    :param collection_of_ideale_funktionen: Collection der idealen Funktionen
    :param collection_of_testdaten: Collection aller vorhandenen Testdaten
    '''
    colors = collection_of_ideale_funktionen.get_color_dict()
    for idealfunktion in collection_of_ideale_funktionen.items:
        collection_of_testdaten_fitting_ideal = \
            collection_of_testdatensatz_fitting.get_new_collection_with_zugeordnete_items([idealfunktion.id])
        collection_of_single_idealfunktion = \
            collection_of_ideale_funktionen.get_new_collection_with_zugeordnete_items([idealfunktion.id])
        collection_of_all_testdaten = deepcopy(collection_of_testdaten)
        collection_of_all_testdaten.subtract(collection_of_testdaten_fitting_ideal)

        log.info("Plotting Idealfunktion \'%s\'. Die Testdaten verteilen sich hier wie folgt: "
                 "Gesamt %s | Fitting %s | Not fitting %s", idealfunktion.id,
                 collection_of_testdaten_fitting_ideal.length() + collection_of_all_testdaten.length(),
                 collection_of_testdaten_fitting_ideal.length(), collection_of_all_testdaten.length())
        if collection_of_testdaten.length() != \
                collection_of_testdaten_fitting_ideal.length() + collection_of_all_testdaten.length():
            raise FindBestFitsException(
                'Die Summe der fitting und not fitting Testdaten unterscheidet sich von der Gesamtzahl an Testdaten')

        plot_combined_solution(collection_of_testdaten_fitting_ideal, collection_of_single_idealfunktion,
                               collection_of_all_testdaten, colors)
