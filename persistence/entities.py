from sqlalchemy import Column, Integer, Float, String, Numeric
from sqlalchemy.ext.declarative import declarative_base

base = declarative_base()


class BaseData(base):
    __tablename__ = 'Basedata'
    X = Column(Float, primary_key=True)
    Y1 = Column(Float)


class Trainingsdaten(base):
    __tablename__ = 'Trainingdata'
    x = Column(Numeric, primary_key=True)
    y1 = Column(Numeric)
    y2 = Column(Numeric)
    y3 = Column(Numeric)
    y4 = Column(Numeric)


class Testdaten(base):
    __tablename__ = 'Testdaten'
    X = Column(Float, primary_key=True)
    Y1 = Column(Float, primary_key=True)
    delta_y = Column(Float)
    ideal_funktion = Column(String, primary_key=True)


class Idealdata(base):
    __tablename__ = 'Idealdata'
    X = Column(Float, primary_key=True)
    Y1 = Column(Float)
    Y2 = Column(Float)
    Y3 = Column(Float)
    Y4 = Column(Float)
    y5 = Column(Float)
    y6 = Column(Float)
    y7 = Column(Float)
    y8 = Column(Float)
    y9 = Column(Float)
    y10 = Column(Float)
    y11 = Column(Float)
    y12 = Column(Float)
    y13 = Column(Float)
    y14 = Column(Float)
    y15 = Column(Float)
    y16 = Column(Float)
    y17 = Column(Float)
    y18 = Column(Float)
    y19 = Column(Float)
    y20 = Column(Float)
    y21 = Column(Float)
    y22 = Column(Float)
    y23 = Column(Float)
    y24 = Column(Float)
    y25 = Column(Float)
    y26 = Column(Float)
    y27 = Column(Float)
    y28 = Column(Float)
    y29 = Column(Float)
    y30 = Column(Float)
    y31 = Column(Float)
    y32 = Column(Float)
    y33 = Column(Float)
    y34 = Column(Float)
    y35 = Column(Float)
    y36 = Column(Float)
    y37 = Column(Float)
    y38 = Column(Float)
    y39 = Column(Float)
    y40 = Column(Float)
    y41 = Column(Float)
    y42 = Column(Float)
    y43 = Column(Float)
    y44 = Column(Float)
    y45 = Column(Float)
    y46 = Column(Float)
    y47 = Column(Float)
    y48 = Column(Float)
    y49 = Column(Float)
    y50 = Column(Float)
