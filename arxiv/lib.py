from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Article(Base):
    __tablename__ = 'articles'

    id = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    submitted_date = Column(DateTime, nullable=False)
    category = Column(String, nullable=False)
    abstract = Column(String, nullable=False)
    abstract_digested = Column(Boolean, nullable=False, default=False)
    source_file = Column(String, nullable=True)
    source_file_digested = Column(Boolean, nullable=False, default=False)
    authors = relationship('Author', back_populates='article')

class Author(Base):
    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    article_id = Column(Integer, ForeignKey('articles.id'), nullable=False)
    article = relationship('Article', back_populates='authors')

def create_db(db_url):
    engine = create_engine(db_url)
    Base.metadata.create_all(engine)
    return engine

if __name__ == "__main__":
    # Set up the database
    db_url = "sqlite:///metadata.db"
    engine = create_db(db_url)