from abc import abstractmethod, ABC

from matplotlib import pyplot as plt


class Plotter(ABC):
    @abstractmethod
    def plot_with_legend(self, funktion, groesse):
        pass

    @abstractmethod
    def plot_without_legend(self, funktion, groesse):
        pass

    def plot_with_color(self, funktion, color):
        pass


class ScatterPlotter(Plotter):

    # overriding abstract method
    def plot_with_legend(self, funktion, groesse):
        plt.scatter(x=funktion.x, y=funktion.y, label=funktion.id, s=groesse)

    # overriding abstract method
    def plot_without_legend(self, funktion, groesse):
        plt.scatter(x=funktion.x, y=funktion.y, c='tab:blue', s=groesse)

    # overriding abstract method
    def plot_with_color(self, funktion, color):
        plt.scatter(x=funktion.x, y=funktion.y, color=color, s=20)


class LinePlotter(Plotter):

    # overriding abstract method
    def plot_with_legend(self, funktion, groesse):
        plt.plot(funktion.x, funktion.y, label=funktion.id, lw=groesse)

    # overriding abstract method
    def plot_without_legend(self, funktion, groesse):
        plt.plot(funktion.x, funktion.y, lw=groesse)

    def plot_with_color_and_abweichung(self, funktion, color, maximale_abweichung):
        plt.plot(funktion.x, funktion.y, label=funktion.id, color=color, lw=1)

        plt.fill_between(funktion.x, funktion.y + funktion.get_faktor_maximale_abweichung(),
                         funktion.y - funktion.get_faktor_maximale_abweichung(), alpha=0.2, facecolor=color)
