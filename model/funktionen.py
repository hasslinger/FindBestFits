import numpy as np

from persistence.entities import Testdaten
from model.plotter import ScatterPlotter, LinePlotter


class Funktion:
    def __init__(self, x, y, id, plotter):
        self.x = x
        self.y = y
        self.id = id
        self.plotter = plotter

    # + describe methode?
    def plot(self, legend, groesse):
        if legend:
            self.plotter.plot_with_legend(self, groesse)
        else:
            self.plotter.plot_without_legend(self, groesse)

    def plot_with_colors(self, color):
        self.plotter.plot_with_colors(self, color)


class Trainingsfunktion(Funktion):
    def __init__(self, x, y, label):
        super().__init__(x, y, label, ScatterPlotter())


class IdealFunktion(Funktion):
    def __init__(self, x, y, label):
        super().__init__(x, y, label, LinePlotter())
        self.summe_abweichungen = None
        self.maximale_abweichung = None

    def get_y_from_x(self, x):
        return self.y.iloc[self.x[self.x == x].index[0]]

    def plot_with_colors_and_abweichung(self, color, maximale_abweichung):
        self.plotter.plot_with_colors_and_abweichung(self, color, maximale_abweichung)

    def get_faktor_maximale_abweichung(self):
        return self.maximale_abweichung + np.sqrt(2)



class Testdatensatz(Funktion):
    def __init__(self, x, y, id):
        super().__init__(x, y, id, ScatterPlotter())
        self.delta_y = None
        self.ideal_funk = None

    def to_entity(self):
        return Testdaten(X=self.x, Y1=self.y, delta_y=self.delta_y, ideal_funktion=self.ideal_funk)
