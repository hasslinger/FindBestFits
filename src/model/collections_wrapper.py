from operator import attrgetter

import pandas as pd

from configuration.logging_configuration import log
from model.funktionen import IdealFunktion, Trainingsfunktion, Testdatensatz
from util.visualisierung import plot_array_of_functions


class CollectionOfFunctions:
    def __init__(self, data, function_class):
        self.items = []
        if isinstance(data, pd.DataFrame):
            for funktionId in data.columns.drop('x').values:
                self.items.append(function_class(data['x'], data[funktionId], funktionId))
        elif isinstance(data, list):
            self.items = data

    def visualize_collection_as_figure(self, label, legend, groesse):
        plot_array_of_functions(self.items, label, legend, groesse)

    def add_item(self, item):
        log.debug('Funktion %s wird der Collection %s hinzugefuegt.', item, self)
        self.items.append(item)

    def remove_if_present(self, item):
        self.items = [x for x in self.items if not (x.x == item.x and x.y == item.y)]

    def plot_all_items(self, color='grey'):
        for item in self.items:
            if isinstance(color, dict):
                item.plot_with_color(color[item.get_zuordnung()])
            else:
                item.plot_with_color(color)

    def get_new_collection_with_zugeordnete_items(self, ideal_funk_ids):
        return self.__class__(list(filter(lambda x: x.get_zuordnung() in ideal_funk_ids, self.items)))

    def length(self):
        return len(self.items)


class CollectionOfTrainingsfunktionen(CollectionOfFunctions):
    def __init__(self, data=None):
        super().__init__(data, Trainingsfunktion)

    def visualize_collection_as_figure(self, label="Trainingsdatensätze", legend=True, groesse=0.8):
        super().visualize_collection_as_figure(label, legend, groesse)


class CollectionOfIdealfunktionen(CollectionOfFunctions):
    def __init__(self, data=None):
        super().__init__(data, IdealFunktion)

    def visualize_collection_as_figure(self, label="Bereitgestellte ideale Funktionen", legend=False, groesse=0.8):
        super().visualize_collection_as_figure(label, legend, groesse)

    def find_funktion_min_abweichungen(self):
        return min(self.items, key=attrgetter('summe_abweichungen'))

    def get_color_dict(self):
        colors = dict()
        possible_values = ['b', 'r', 'g', 'y']
        for item in self.items:
            colors[item.id] = possible_values.pop(0)
        return colors


class CollectionOfTestdaten(CollectionOfFunctions):
    def __init__(self, data=None):
        if isinstance(data, pd.DataFrame):
            data = [(Testdatensatz(row.x, row.y, index)) for index, row in data.iterrows()]
        super().__init__(data, Testdatensatz)

    def visualize_collection_as_figure(self, label="Bereitgestellte Testdaten", legend=False, groesse=20):
        super().visualize_collection_as_figure(label, legend, groesse)

    def to_entities(self):
        return list(map(lambda x: x.to_entity(), self.items))

    def subtract(self, collection_of_testdaten):
        set1 = set((x.x, x.y) for x in collection_of_testdaten.items)
        self.items = [x for x in self.items if (x.x, x.y) not in set1]
