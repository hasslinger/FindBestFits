from abc import abstractmethod, ABC

from matplotlib import pyplot as plt


class Plotter(ABC):
    '''
    Abstrakte Oberklasse fuer im Programm genutzte Plotter. Sie sammelt abstrakt Methoden, die von den genutzten
    Plottern implementiert werden muessen.
    Die angebotenden Methoden sind dabei statisch.
    '''
    @staticmethod
    @abstractmethod
    def plot_with_legend(self, funktion, groesse):
        pass

    @staticmethod
    @abstractmethod
    def plot_without_legend(self, funktion, groesse):
        pass

    @staticmethod
    @abstractmethod
    def plot_with_color(self, funktion, color):
        pass


class ScatterPlotter(Plotter):
    '''
    Kann genutzt werden um Funktionen als Scatterplots zu visualisieren.
    '''
    def plot_with_legend(self, funktion, groesse):
        plt.scatter(x=funktion.x, y=funktion.y, label=funktion.id, s=groesse)

    def plot_without_legend(self, funktion, groesse):
        plt.scatter(x=funktion.x, y=funktion.y, c='tab:blue', s=groesse)

    def plot_with_color(self, funktion, color):
        plt.scatter(x=funktion.x, y=funktion.y, color=color, s=20)


class LinePlotter(Plotter):
    '''
    Kann genutzt werden um Funktionen als Lineplots zu visualisieren.
    '''
    def plot_with_legend(self, funktion, groesse):
        plt.plot(funktion.x, funktion.y, label=funktion.id, lw=groesse)

    def plot_without_legend(self, funktion, groesse):
        plt.plot(funktion.x, funktion.y, lw=groesse)

    def plot_with_color(self, funktion, color):
        plt.plot(funktion.x, funktion.y, label=funktion.id, color=color, lw=1)
        plt.fill_between(funktion.x, funktion.y + funktion.get_faktor_maximale_abweichung(),
                         funktion.y - funktion.get_faktor_maximale_abweichung(), alpha=0.2, facecolor=color)
