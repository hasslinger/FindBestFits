from abc import abstractmethod
from functools import partial
from operator import attrgetter, is_not

import pandas as pd

from configuration.logging_configuration import log
from model.funktionen import IdealFunktion, Trainingsfunktion, Testdatensatz
from util.visualisierung import plot_array_of_functions


class CollectionOfFunctions:
    def __init__(self):
        self.items = []

    def __init__(self, df, function_class):
        self.items = []

        if isinstance(df, pd.DataFrame):
            for funktionId in df.columns.drop('x').values:
                self.items.append(function_class(df['x'], df[funktionId], funktionId))
        elif isinstance(df, list):
            self.items = df


    def visualize_collection_as_figure(self, label, legend, groesse):
        plot_array_of_functions(self.items, label, legend, groesse)

    @abstractmethod
    def plot_all_items(self, colors):
        pass

    def add_item(self, item):
        log.debug('Funktion %s wird der Collection %s hinzugefuegt.', item, self)
        self.items.append(item)

    def remove_if_present(self, item):
        self.items = [x for x in self.items if not (x.x == item.x and x.y == item.y)]


class CollectionOfTrainingsfunktionen(CollectionOfFunctions):
    def __init__(self, df=None):
        super().__init__(df, Trainingsfunktion)

    def visualize_collection_as_figure(self, label="Trainingsdatensätze", legend=True, groesse=0.8):
        super().visualize_collection_as_figure(label, legend, groesse)


class CollectionOfIdealfunktionen(CollectionOfFunctions):
    def __init__(self, df=None):
        super().__init__(df, IdealFunktion)
        # self.maximale_abweichung = 0

    def visualize_collection_as_figure(self, label="Bereitgestellte ideale Funktionen", legend=False, groesse=0.8):
        super().visualize_collection_as_figure(label, legend, groesse)

    # overriding abstract method
    def plot_all_items(self, colors):
        for item in self.items:
            item.plot_with_color(colors[item.id])

    def find_funktion_min_abweichungen(self):
        return min(self.items, key=attrgetter('summe_abweichungen'))

    def get_color_dict(self):
        colors = dict()
        possible_values = ['b','r','g','y']
        for item in self.items:
            colors[item.id] = possible_values.pop(0)
        return colors

    def get_new_with_ids(self, ideal_funk_id):
        return CollectionOfIdealfunktionen(list(filter(lambda x: x.id in ideal_funk_id, self.items)))


class CollectionOfTestdaten(CollectionOfFunctions):
    def __init__(self, df=None):
        if df is None:
            self.items = []
        elif isinstance(df, list):
            self.items = df
        elif isinstance(df, pd.DataFrame):
            self.items = [(Testdatensatz(row.x, row.y, index)) for index, row in df.iterrows()]

    # overriding abstract method
    def plot_all_items(self, color='grey'):
        for item in self.items:
            if isinstance(color, dict):
                item.plot_with_color(color[item.ideal_funk])
            else:
                item.plot_with_color(color)

    def visualize_collection_as_figure(self, label="Bereitgestellte Testdaten", legend=False, groesse=20):
        super().visualize_collection_as_figure(label, legend, groesse)

    def length(self):
        return len(self.items)

    def drop_none_values(self):
        self.items = list(filter(partial(is_not, None), self.items))

    def to_entities(self):
        return list(map(lambda x: x.to_entity(), self.items))

    def subtract(self, collection_of_testdaten):
        set1 = set((x.x, x.y) for x in collection_of_testdaten.items)
        self.items = [x for x in self.items if (x.x, x.y) not in set1]

    def get_new_with_ids(self, ideal_funk_id):
        return CollectionOfTestdaten(list(filter(lambda x: x.ideal_funk in ideal_funk_id, self.items)))

    # def get_all_not_ideal_id(self, ideal_funk_id):
    #     return list(filter(lambda x: x.ideal_funk != ideal_funk_id, self.items))
