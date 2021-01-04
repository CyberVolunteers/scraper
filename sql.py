import uuid

import requests
import sqlalchemy as db
from sqlalchemy import Column, Integer, String, insert, delete
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


def generate_uuid():
    return str(uuid.uuid4())


# declare the structure
Base = declarative_base()

connectLocally = True

class ListingsTable(Base):
    __tablename__ = "listings"

    uuid = Column(String)
    timeForVolunteering = Column(String)
    placeForVolunteering = Column(String)
    targetAudience = Column(String)
    skills = Column(String)
    createdDate = Column(Integer)
    requirements = Column(String)
    opportunityDesc = Column(String)
    opportunityCategory = Column(String)
    opportunityTitle = Column(String)
    numOfvolunteers = Column(Integer)
    minHoursPerWeek = Column(Integer)
    maxHoursPerWeek = Column(Integer)
    id = Column(Integer, primary_key=True)
    duration = Column(String)
    charityId = Column(Integer)
    scrapedCharityName = Column(String)
    # pictureName = Column(String)


# open
with open("./sqlPassword.txt", "r") as f:
    password = f.read()

connectionString = "mysql+pymysql://serverQueryManager:%s@localhost:3306/cybervolunteers" % password

engine = db.create_engine(connectionString)
Session = sessionmaker(bind=engine)
session = Session()

requestSession = requests.Session()

# request

def recordInDb(listing, data, credentials):
    cookie, path = credentials

    statement = (
        insert(ListingsTable).
        values(**data)
    )
    statement = statement.compile(engine, compile_kwargs={"literal_binds": True})

    try:
        session.add(listing)
        session.commit()
    except:
        pass
        # print("Not able to commit to local db")

    response = requestSession.post("https://cybervolunteers.org.uk/" + path, cookies={"sessionId": cookie},
                                   data={"sql": statement})


def deleteFromSite(url, credentials):
    cookie, path = credentials

    statement = (
        delete(ListingsTable).
        where(ListingsTable.duration.like('<a class="moreDetails" href="{}%'.format(url)))
    )
    statement = statement.compile(engine, compile_kwargs={"literal_binds": True})

    try:
        engine.execute(statement)
    except:
        pass
        # print("Not able to commit to local db")

    response = requestSession.post("https://cybervolunteers.org.uk/" + path, cookies={"sessionId": cookie},
                                   data={"sql": str(statement)})
