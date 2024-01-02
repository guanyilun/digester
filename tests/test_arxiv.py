import arxiv
max_results = 100

client = arxiv.Client()
category = "astro-ph.CO" 
articles = arxiv.Search(
    query=f"cat:{category}",
    max_results=max_results,
    sort_by=arxiv.SortCriterion.SubmittedDate
)
articles = list(client.results(articles))
