from prefect import flow, get_run_logger


@flow(name="arxiv-metadata-ingest")
def ingest_metadata(db_url: str = "sqlite:////home/yilun.guan/.digester/arxiv/metadata.db", category: str = "astro-ph.CO"):
    import arxiv
    from sqlalchemy.orm import sessionmaker
    from lib import create_db, Article, Author  # Assuming the revised script is saved as arxiv_db.py

    logger = get_run_logger()

    # Set up the database
    engine = create_db(db_url)

    # Fetch articles from arXiv
    articles = arxiv.Search(
        query=f"cat:{category}",
        max_results=50,
        sort_by=arxiv.SortCriterion.SubmittedDate
    )

    # Store articles in the database
    Session = sessionmaker(bind=engine)
    session = Session()

    new_records = 0
    for result in articles.results():
        # check if article already exists
        if session.query(Article).filter_by(id=result.entry_id).first():
            continue
        title = result.title
        submitted_date = result.published
        category = "astro-ph.CO"
        abstract = result.summary
        authors = [author.name for author in result.authors]
        entry_id = result.entry_id

        logger.info(f"Adding article: {entry_id}")

        article = Article(
            id=entry_id,
            title=title,
            submitted_date=submitted_date,
            category=category,
            abstract=abstract,
            abstract_digested=False,
            source_file_digested=False
        )
        session.add(article)

        for author_name in authors:
            author = Author(name=author_name, article=article)
            session.add(author)
        new_records += 1

    session.commit()
    logger.info(f"Added {new_records} new records to the database.")

if __name__ == "__main__":
    ingest_metadata()