from abc import ABC, abstractmethod
from operator import attrgetter

import pandas as pd

from configuration.logging_configuration import log
from exception.FindBestFitsException import FindBestFitsException
from model.funktionen import IdealFunktion, Trainingsfunktion, Testdatensatz
from util.visualisierung import plot_array_of_datensaetze


class CollectionOfDatensaetze(ABC):
    '''
    Abstrakte Oberklasse fuer alle Collections von Datensaetzen.
    Diese Collections dienen als Wrapper um verschiedene Datensaetze
    (Trainingsfunktion, IdealFunktion, Testdatensatz) zu halten.
    Es werden wiederkehrend auftretendende Operationen auf den Sammlungen von Datensaetzen zentralisiert.
    Operationen, die unabhängig vom Datensaetztyp sind, werden in dieser Klasse gesammelt.
    '''

    @abstractmethod
    def __init__(self, data, dataset_class):
        self.items = []
        if isinstance(data, pd.DataFrame):
            for id in data.columns.drop('x').values:
                self.items.append(dataset_class(data['x'], data[id], id))
        elif isinstance(data, list):
            self.items = data

    @abstractmethod
    def visualize_collection_as_figure(self, label, legend, groesse):
        plot_array_of_datensaetze(self.items, label, legend, groesse)

    def add_item(self, item):
        log.debug('Funktion %s wird der Collection %s hinzugefuegt.', item, self)
        self.items.append(item)

    def remove_if_present(self, item):
        '''Entfernt alle Testdaten dessen x und y Wert dem von item entspricht'''
        self.items = [x for x in self.items if not (x.x == item.x and x.y == item.y)]

    def plot_all_items(self, color='grey'):
        for item in self.items:
            if isinstance(color, dict):
                item.plot_with_color(color[item.get_zuordnung()])
            else:
                item.plot_with_color(color)

    def get_new_collection_with_zugeordnete_items(self, ids):
        '''Filtert Funktionen heraus, welche einer der ids zugeordnet sind und returned eine neue Collection'''
        return self.__class__(list(filter(lambda x: x.get_zuordnung() in ids, self.items)))

    def length(self):
        return len(self.items)


class CollectionOfTrainingsfunktionen(CollectionOfDatensaetze):
    '''
    Eine Wrapper Klasse zur Sammlung von Trainingsfunktionen.
    '''

    def __init__(self, data=None):
        super().__init__(data, Trainingsfunktion)

    def visualize_collection_as_figure(self, label="Trainingsdatensätze", legend=True, groesse=0.8):
        super().visualize_collection_as_figure(label, legend, groesse)


class CollectionOfIdealfunktionen(CollectionOfDatensaetze):
    '''
    Eine Wrapper Klasse zur Sammlung von Idealfunktionen.
    '''

    def __init__(self, data=None):
        super().__init__(data, IdealFunktion)

    def visualize_collection_as_figure(self, label="Bereitgestellte ideale Funktionen", legend=False, groesse=0.8):
        super().visualize_collection_as_figure(label, legend, groesse)

    def find_funktion_min_abweichungen(self):
        return min(self.items, key=attrgetter('summe_abweichungen'))

    def get_color_dict(self):
        '''Ordnet jeder Idealfunktion eine Farbe zu und returned das Ergebnis als Dictionary'''
        colors = dict()
        possible_values = ['b', 'r', 'g', 'y']
        if len(possible_values) < len(self.items):
            raise FindBestFitsException('Es gibt mehr Idealfunktionen als moegliche Farben.')
        for item in self.items:
            colors[item.id] = possible_values.pop(0)
        return colors


class CollectionOfTestdaten(CollectionOfDatensaetze):
    '''
    Eine Wrapper Klasse zur Sammlung von Testdaten.
    '''

    def __init__(self, data=None):
        if isinstance(data, pd.DataFrame):
            data = [(Testdatensatz(row.x, row.y, index)) for index, row in data.iterrows()]
        super().__init__(data, Testdatensatz)

    def visualize_collection_as_figure(self, label="Bereitgestellte Testdaten", legend=False, groesse=20):
        super().visualize_collection_as_figure(label, legend, groesse)

    def to_entities(self):
        return list(map(lambda x: x.to_entity(), self.items))

    def subtract(self, collection_of_testdaten):
        for item in collection_of_testdaten.items:
            self.remove_if_present(item)
