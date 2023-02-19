import os
import contextlib

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from persistence.entities import base


def silentremove(filename):
    with contextlib.suppress(FileNotFoundError):
        os.remove(filename)


class Repository:
    def __init__(self):
        silentremove('persistence/bestFit.db')

        self.engine = create_engine('sqlite:///persistence/bestFit.db', echo=False)

        base.metadata.create_all(self.engine)

        Session = sessionmaker(bind=self.engine)
        self.sessionobj = Session()

    def addAll(self, rows):
        self.sessionobj.add_all(rows)
        self.sessionobj.commit()

    def addDataframe(self, df, type):
        df.to_sql(type, self.engine, if_exists='append', index=False)
