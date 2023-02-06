from sqlalchemy import create_engine, text
from entities import base
from sqlalchemy.orm import sessionmaker
import os


class Repository:
    def __init__(self):

        os.remove('bestFit.db')

        #engine = create_engine('sqlite:///college.db', echo=True)
        self.engine = create_engine('sqlite:///bestFit.db', echo=False)

        base.metadata.create_all(self.engine)

        Session = sessionmaker(bind=self.engine)
        self.sessionobj = Session()

    def add(self, row):
        self.sessionobj.add(row)
        self.sessionobj.commit()

    def addAll(self, rows):
        self.sessionobj.add_all(rows)
        self.sessionobj.commit()

    def getAll(self, type):
        qry = self.sessionobj.query(type).all()
        print(qry)
        return qry

    def addDataframe(self, df, type):
        df.to_sql(type, self.engine, if_exists='append', index=False)