from matplotlib import pyplot as plt
from matplotlib.legend_handler import HandlerTuple


def plot_array_of_functions(array_of_functions, title, legend, groesse):
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
                           collection_of_all_testdaten_not_fitting):
    plt.figure()
    plt.style.use('default')
    colors = collection_of_ideale_funktionen.get_color_dict()
    #colors = {collection_of_ideale_funktionen.items[0].id: 'r', collection_of_ideale_funktionen.items[1].id: 'g', collection_of_ideale_funktionen.items[2].id: 'b', collection_of_ideale_funktionen.items[3].id: 'y'}
    fig, ax = plt.subplots()
    handles, labels = ax.get_legend_handles_labels()
    ax.legend([tuple(handles[::2]), tuple(handles[1::2])], labels[:2], handlelength=3,
              handler_map={tuple: HandlerTuple(ndivide=None)})
    collection_of_fitting_testdaten.plot_all_items(colors)
    collection_of_ideale_funktionen.plot_all_items(colors)
    collection_of_all_testdaten_not_fitting.plot_all_items()

    plt.title("Darstellung der idealen Testfunktionen und die zugehoerigen Testdaten")
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.legend(loc='best', markerscale=8)
    plt.ylim(top=110)
    plt.ylim(bottom=-25)
    plt.grid(alpha=0.4)
    plt.show(block=False)
