from abc import abstractmethod, ABC

import numpy as np

from exception.FindBestFitsException import FindBestFitsException
from persistence.entities import Testdaten
from model.plotter import ScatterPlotter, LinePlotter


class Datensatz(ABC):
    '''
    Abstrakte Oberklasse fuer alle im Programm genutzten Datensaetze (Trainingsfunktion, IdealFunktion, Testdatensatz).
    Jeder Datensatz muss bestimmte Attribute haben, welche in der Oberklasse gesammelt werden.
    Außerdem werden Methoden gesammelt, die auf allen Funktionen gleichermaßen ausgefuehrt werden.
    '''
    @abstractmethod
    def __init__(self, x, y, id, plotter):
        self.x = x
        self.y = y
        self.id = id
        self.plotter = plotter

    def plot(self, legend, groesse):
        if legend:
            self.plotter.plot_with_legend(self, groesse)
        else:
            self.plotter.plot_without_legend(self, groesse)

    def plot_with_color(self, color):
        self.plotter.plot_with_color(self, color)

    @abstractmethod
    def get_zuordnung(self):
        pass


class Trainingsfunktion(Datensatz):
    '''
    Eine Klasse fuer alle Trainingsfunktionen.
    Zur Visualisierung der Trainingsfunktionen soll in diesem Fall der ScatterPlotter genutzt werden.
    X und Y werden bei dieser Funktion durch pandas Series dargestellt.
    '''
    def __init__(self, x, y, label):
        super().__init__(x, y, label, ScatterPlotter)

    def get_zuordnung(self):
        return self.id


class IdealFunktion(Datensatz):
    '''
    Eine Klasse fuer alle idealen Funktionen.
    Zur Visualisierung der idealen Funktionen soll in diesem Fall der LinePlotter genutzt werden.
    X und Y werden bei dieser Funktion durch pandas Series dargestellt.
    Zudem wird pro idealfunktion die Summe der Abweichungen zu den Trainingsdaten und die maximale Abweichung gehalten.
    '''
    def __init__(self, x, y, label):
        super().__init__(x, y, label, LinePlotter)
        self.summe_abweichungen = None
        self.maximale_abweichung = None

    def get_y_from_x(self, x):
        fitting_x = self.x[self.x == x]
        if fitting_x.empty:
            raise FindBestFitsException(
                'Es konnte kein y-Wert zum x-Wert={} in der Idealfunktion={} gefunden werden'.format(x, self.id))
        return self.y.iloc[fitting_x.index[0]]

    def get_faktor_maximale_abweichung(self):
        return self.maximale_abweichung + np.sqrt(2)

    def get_zuordnung(self):
        return self.id


class Testdatensatz(Datensatz):
    '''
    Eine Klasse fuer alle Testdatensaetze.
    Zur Visualisierung der idealen Funktionen soll in diesem Fall der ScatterPlotter genutzt werden.
    Ein Testdatensatz ist in diesem Fall ein einzelner Punkt. X und Y sind daher float64 Werte.
    Zudem kann ein Testdatensatz einer idealen Funktion mit entsprechender Abweichung zugeordnet werden.
    Das Resultat kann dann direkt in eine Entitaet umgewandelt werden.
    '''
    def __init__(self, x, y, id):
        super().__init__(x, y, id, ScatterPlotter)
        self.delta_y = None
        self.ideal_funk = None

    def to_entity(self):
        return Testdaten(X=self.x, Y1=self.y, delta_y=self.delta_y, ideal_funktion=self.ideal_funk)

    def get_zuordnung(self):
        return self.ideal_funk
