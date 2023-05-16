from langchain.document_loaders import ArxivLoader

def load_arxiv_courses(query):
  docs = ArxivLoader(query=query, load_max_docs=10).load()
  return docs[0].metadata