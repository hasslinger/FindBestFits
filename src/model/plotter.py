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
    def plot_with_legend(datensatz, groesse):
        pass

    @staticmethod
    @abstractmethod
    def plot_without_legend(datensatz, groesse):
        pass

    @staticmethod
    @abstractmethod
    def plot_with_color(datensatz, color):
        pass


class ScatterPlotter(Plotter):
    '''
    Kann genutzt werden um Datensaetze als Scatterplots zu visualisieren.
    '''

    @staticmethod
    def plot_with_legend(datensatz, groesse):
        plt.scatter(x=datensatz.x, y=datensatz.y, label=datensatz.id, s=groesse)

    @staticmethod
    def plot_without_legend(datensatz, groesse):
        plt.scatter(x=datensatz.x, y=datensatz.y, c='tab:blue', s=groesse)

    @staticmethod
    def plot_with_color(datensatz, color):
        plt.scatter(x=datensatz.x, y=datensatz.y, color=color, s=20)


class LinePlotter(Plotter):
    '''
    Kann genutzt werden um Datensaetze als Lineplots zu visualisieren.
    '''

    @staticmethod
    def plot_with_legend(datensatz, groesse):
        plt.plot(datensatz.x, datensatz.y, label=datensatz.id, lw=groesse)

    @staticmethod
    def plot_without_legend(datensatz, groesse):
        plt.plot(datensatz.x, datensatz.y, lw=groesse)

    @staticmethod
    def plot_with_color(datensatz, color):
        plt.plot(datensatz.x, datensatz.y, label=datensatz.id, color=color, lw=1)
        plt.fill_between(datensatz.x, datensatz.y + datensatz.get_faktor_maximale_abweichung(),
                         datensatz.y - datensatz.get_faktor_maximale_abweichung(), alpha=0.2, facecolor=color)
