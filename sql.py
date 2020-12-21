import sqlalchemy as db

engine = db.create_engine('mysql+mysqldb://<user>:<password>@<host>[:<port>]/<dbname>')
