"""This script instead of pulling from arxiv, populates
the database from a local json database"""

#%%
import argparse
import json
import sys, os.path as op
parent_dir = op.dirname(op.dirname(op.abspath(__file__)))
sys.path.append(parent_dir)

from sqlalchemy.orm import sessionmaker
from lib import create_db, Article, Author, arxiv_url_to_id_and_ver

parser = argparse.ArgumentParser()
parser.add_argument("--ifile", help="jsonl file to load", default="/data/arxiv-abstract-2021/arxiv-abstracts.jsonl")
parser.add_argument("--db_url", help="database url", default="sqlite:////home/yilun.guan/.digester/arxiv/metadata.db")
args = parser.parse_args()

if not op.exists(args.ifile):
    raise ValueError("File does not exist")

engine = create_db(args.db_url)

# Store articles in the database
Session = sessionmaker(bind=engine)
session = Session()

with open(args.ifile, "r") as f:
    for line in f:
        record = json.loads(line)
        # create article if it doesn't exist
        exist = session.query(Article).filter_by(id=record["id"]).first()
        if exist is not None:
            print("warning: article already exists", record["id"])
            continue
        article = Article(
            id=record["id"],
            title=record["title"],
            category=",".join(record["categories"]),
            abstract=record["abstract"],
            abstract_digested=False,
            source_file_digested=False
        )
        session.add(article)
        print("added article:", article.id)

        for author_name in record["authors"].split(","):
            author_name = author_name.strip()
            author = Author(name=author_name, article=article)
            session.add(author)

        session.commit()
