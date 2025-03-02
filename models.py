from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base

db_url = 'sqlite:///database.db'

engine = create_engine(db_url)
Base = declarative_base()

class Livres(Base):
    __tablename__ = "livres"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    author = Column(String, nullable=True)
    title = Column(String, nullable=False)
    langage = Column(String, nullable=True) # Langage dans lequel est écrit le document
    type = Column(String, nullable=False) # Spécifier s'il s'agit d'un langage, catégorie ou framework
    category = Column(String, nullable=False) # Spécifier si c'est web, mobile, ia ...
    description = Column(String, nullable=True)

Base.metadata.create_all(engine)
