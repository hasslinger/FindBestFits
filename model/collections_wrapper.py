from abc import abstractmethod
from functools import partial
from operator import attrgetter, is_not

from model.funktionen import IdealFunktion, Trainingsfunktion, Testdatensatz
from util.visualisierung import plot_array_of_functions


class CollectionOfFunctions:
    def __init__(self):
        self.items = []

    def __init__(self, df, function_class):
        self.items = []

        if df is not None:
            for funktionId in df.columns.drop('x').values:
                self.items.append(function_class(df['x'], df[funktionId], funktionId))

    def visualize_collection_as_figure(self, label, legend, groesse):
        plot_array_of_functions(self.items, label, legend, groesse)

    @abstractmethod
    def plot_all_items(self, colors):
        pass

    def add_item(self, item):
        self.items.append(item)

    def remove_if_present(self, item):
        if item in self.items:
            self.items.remove(item)

class CollectionOfTrainingsfunktionen(CollectionOfFunctions):
    def __init__(self, df=None):
        super().__init__(df, Trainingsfunktion)

    def visualize_collection_as_figure(self, label="Trainingsdatensätze", legend=True, groesse=0.8):
        super().visualize_collection_as_figure(label, legend, groesse)


class CollectionOfIdealfunktionen(CollectionOfFunctions):
    def __init__(self, df=None):
        super().__init__(df, IdealFunktion)
        self.maximale_abweichung = 0

    def visualize_collection_as_figure(self, label="Bereitgestellte ideale Funktionen", legend=False, groesse=0.8):
        super().visualize_collection_as_figure(label, legend, groesse)

    # overriding abstract method
    def plot_all_items(self, colors):
        for item in self.items:
            item.plot_with_colors_and_abweichung(colors[item.id], item.get_faktor_maximale_abweichung())

    def find_funktion_min_abweichungen(self):
        return min(self.items, key=attrgetter('summe_abweichungen'))

    def get_color_dict(self):
        colors = dict()
        possible_values = ['b','r','g','y']
        for item in self.items:
            colors[item.id] = possible_values.pop(0)
        return colors


class CollectionOfTestdaten(CollectionOfFunctions):
    def __init__(self, df=None):
        if df is None:
            self.items = []
        else:
            self.items = [(Testdatensatz(row.x, row.y, index)) for index, row in df.iterrows()]

    # overriding abstract method
    def plot_all_items(self, colors='grey'):
        for item in self.items:
            if isinstance(colors, dict):
                item.plot_with_colors(colors[item.ideal_funk])
            else:
                item.plot_with_colors(colors)

    def visualize_collection_as_figure(self, label="Bereitgestellte Testdaten", legend=False, groesse=20):
        super().visualize_collection_as_figure(label, legend, groesse)

    def drop_none_values(self):
        self.items = list(filter(partial(is_not, None), self.items))

    def to_entities(self):
        return list(map(lambda x: x.to_entity(), self.items))

    def subtract(self, collection_of_testdaten):
        set1 = set((x.x, x.y) for x in collection_of_testdaten.items)
        self.items = [x for x in self.items if (x.x, x.y) not in set1]
