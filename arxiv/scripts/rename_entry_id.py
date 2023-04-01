"""Change existing entry IDs in the database to new ones."""

import sys, os.path as op
parent_dir = op.dirname(op.dirname(op.abspath(__file__)))
sys.path.append(parent_dir)

from sqlalchemy.orm import sessionmaker
from lib import create_db, Article, arxiv_url_to_id_and_ver, Author

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--db_url", help="database url", default="sqlite:////home/yilun.guan/.digester/arxiv/metadata.db")
args = parser.parse_args()

engine = create_db(args.db_url)
Session = sessionmaker(bind=engine)
session = Session()

for article in session.query(Article):
    try:
        if "http" in article.id:
            arxiv_id, version = arxiv_url_to_id_and_ver(article.id)
            print(f"  {article.id} -> {arxiv_id}")
            article.id = arxiv_id
            session.commit()
    except Exception as e:
        print("Error:", e)
        # delete the article
        session.rollback()
        session.query(Article).filter_by(id=article.id).delete()
        session.commit()

for author in session.query(Author):
    try:
        if "http" in author.article_id:
            arxiv_id, version = arxiv_url_to_id_and_ver(author.article_id)
            print(f"  {author.article_id} -> {arxiv_id}")
            author.article_id = arxiv_id
            session.commit()
    except Exception as e:
        print("Error:", e)
        session.rollback()