from prefect import flow, get_run_logger
from typing import Optional


@flow(name="arxiv-ingest-metadata")
def arxiv_ingest_metadata(
    db_url: str = "sqlite:////home/yilun.guan/.digester/arxiv/metadata.db",
    category: str = "astro-ph.CO",
    max_results: Optional[int] = 100
    ):
    import arxiv
    from sqlalchemy.orm import sessionmaker
    from digester.arxiv import create_db, Article, Author, arxiv_url_to_id_and_ver

    logger = get_run_logger()

    # Set up the database
    engine = create_db(db_url)

    # Fetch articles from arXiv
    search = arxiv.Search(
        query=f"cat:{category}",
        max_results=max_results,
        sort_by=arxiv.SortCriterion.SubmittedDate
    )
    articles = arxiv.Client().results(search)

    # Store articles in the database
    Session = sessionmaker(bind=engine)
    session = Session()

    new_records = 0
    for result in articles:
        # check if article already exists
        arxiv_id, _ = arxiv_url_to_id_and_ver(result.entry_id)
        if session.query(Article).filter_by(id=arxiv_id).first():
            continue
        title = result.title
        submitted_date = result.published
        abstract = result.summary
        authors = [author.name for author in result.authors]

        logger.info(f"Adding article: {arxiv_id}")

        article = Article(
            id=arxiv_id,
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