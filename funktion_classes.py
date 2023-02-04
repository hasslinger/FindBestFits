from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Numeric

base = declarative_base()


class Testfunktion(base):
    __tablename__ = 'Testfunktion'
    x = Column(Numeric, primary_key=True)
    y1 = Column(Numeric)
    y2 = Column(Numeric)
    y3 = Column(Numeric)
    y4 = Column(Numeric)


class Testdaten(base):
    __tablename__ = 'Testdaten'
    x = Column(Numeric, primary_key=True)
    y = Column(Numeric, primary_key=True)
    deltay = Column(Numeric)
    idealfunk = Column(Numeric)


class Idealfunktion(base):
    __tablename__ = 'Idealfunktion'
    x = Column(Numeric, primary_key=True)
    y1 = Column(Numeric)
    y2 = Column(Numeric)
    y3 = Column(Numeric)
    y4 = Column(Numeric)
    y5 = Column(Numeric)
    y6 = Column(Numeric)
    y7 = Column(Numeric)
    y8 = Column(Numeric)
    y9 = Column(Numeric)
    y10 = Column(Numeric)
    y11 = Column(Numeric)
    y12 = Column(Numeric)
    y13 = Column(Numeric)
    y14 = Column(Numeric)
    y15 = Column(Numeric)
    y16 = Column(Numeric)
    y17 = Column(Numeric)
    y18 = Column(Numeric)
    y19 = Column(Numeric)
    y20 = Column(Numeric)
    y21 = Column(Numeric)
    y22 = Column(Numeric)
    y23 = Column(Numeric)
    y24 = Column(Numeric)
    y25 = Column(Numeric)
    y26 = Column(Numeric)
    y27 = Column(Numeric)
    y28 = Column(Numeric)
    y29 = Column(Numeric)
    y30 = Column(Numeric)
    y31 = Column(Numeric)
    y32 = Column(Numeric)
    y33 = Column(Numeric)
    y34 = Column(Numeric)
    y35 = Column(Numeric)
    y36 = Column(Numeric)
    y37 = Column(Numeric)
    y38 = Column(Numeric)
    y39 = Column(Numeric)
    y40 = Column(Numeric)
    y41 = Column(Numeric)
    y42 = Column(Numeric)
    y43 = Column(Numeric)
    y44 = Column(Numeric)
    y45 = Column(Numeric)
    y46 = Column(Numeric)
    y47 = Column(Numeric)
    y48 = Column(Numeric)
    y49 = Column(Numeric)
    y50 = Column(Numeric)
