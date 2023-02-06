from matplotlib import pyplot as plt

from entities import Testdaten


class Funktion:
    def __init__(self, x, y, id):
        self.x = x
        self.y = y
        self.id = id

    # + describe methode?
    def plot(self, legend, groesse):
        if legend:
            plt.scatter(x=self.x, y=self.y, cmap=self.id, label=self.id, s=groesse)
        else:
            plt.scatter(x=self.x, y=self.y, c='tab:blue', s=groesse)


class Trainingsfunktion(Funktion):
    def __init__(self, x, y, label):
        super().__init__(x, y, label)


class IdealFunktion(Funktion):
    def __init__(self, x, y, label):
        super().__init__(x, y, label)
        self.summe_abweichungen = None
        self.maximale_abweichung = None

    def plot(self, legend, groesse):
        plt.plot(self.x, self.y, label=self.id, lw=groesse)

    def get_y_from_x(self, x):
        return self.y.iloc[self.x[self.x == x].index[0]]


class Testdatensatz(Funktion):
    def __init__(self, x, y, id):
        super().__init__(x, y, id)
        self.delta_y = None
        self.ideal_funk = None

    def to_entity(self):
        return Testdaten(X=self.x, Y1=self.y, delta_y=self.delta_y, ideal_funktion=self.ideal_funk)
