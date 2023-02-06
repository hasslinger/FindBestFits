from matplotlib import pyplot as plt
import seaborn as sns
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


def plot_combined_solution(array_of_fitting_testdaten, array_of_ideale_funktionen, array_of_all_testdaten_not_fitting, maximale_abweichung):
    plt.figure()
    plt.style.use('default')
    colours = {array_of_ideale_funktionen[0].id: 'r', array_of_ideale_funktionen[1].id: 'g',
               array_of_ideale_funktionen[2].id: 'b', array_of_ideale_funktionen[3].id: 'y'}
    # print(colours)
    # print(colours[array_of_fitting_testdaten[0].ideal_funk])
    fig, ax = plt.subplots()
    # for given_function in array_of_ideale_funktionen:
    #     print(given_function)
    #     print(given_function.x)
    #     sns.lineplot(x=given_function.x, y=given_function.y,  label = given_function.id, data=given_function, ax=ax, palette="rocket", linewidth=2.5)
    # for given_function in array_of_fitting_testdaten:
    #     sns.scatterplot(data=given_function, x="x", y="y", hue="ideal_funk", ax=ax, palette="rocket", s=200)
    #
    handles, labels = ax.get_legend_handles_labels()
    ax.legend([tuple(handles[::2]), tuple(handles[1::2])], labels[:2], handlelength=3,
              handler_map={tuple: HandlerTuple(ndivide=None)})
    for given_function in array_of_fitting_testdaten:
        plt.scatter(x=given_function.x, y=given_function.y, color=colours[given_function.ideal_funk], s=20)
    for given_function in array_of_ideale_funktionen:
        plt.plot(given_function.x, given_function.y, label=given_function.id, color=colours[given_function.id], lw=1)

        plt.fill_between(given_function.x, given_function.y-maximale_abweichung, given_function.y+maximale_abweichung,alpha=0.2, facecolor=colours[given_function.id])
    for given_function in array_of_all_testdaten_not_fitting:
        plt.scatter(x=given_function.x, y=given_function.y, c='grey', s=20)



    plt.title("COMBINED")
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.legend(loc='best', markerscale=8)
    plt.ylim(top=110)
    plt.ylim(bottom=-25)
    plt.grid(alpha=0.4)
    plt.show(block=False)
