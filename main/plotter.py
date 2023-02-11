from abc import abstractmethod, ABC

from matplotlib import pyplot as plt


class Plotter(ABC):
    @abstractmethod
    def plot_with_legend(self, funktion, groesse):
        pass

    @abstractmethod
    def plot_without_legend(self, funktion, groesse):
        pass


class ScatterPlotter(Plotter):

    # overriding abstract method
    def plot_with_legend(self, funktion, groesse):
        plt.scatter(x=funktion.x, y=funktion.y, cmap=funktion.id, label=funktion.id, s=groesse)

    # overriding abstract method
    def plot_without_legend(self, funktion, groesse):
        plt.scatter(x=funktion.x, y=funktion.y, c='tab:blue', s=groesse)


class LinePlotter(Plotter):

    # overriding abstract method
    def plot_with_legend(self, funktion, groesse):
        plt.plot(funktion.x, funktion.y, label=funktion.id, lw=groesse)

    # overriding abstract method
    def plot_without_legend(self, funktion, groesse):
        plt.plot(funktion.x, funktion.y, lw=groesse)
