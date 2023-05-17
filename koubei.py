import os
from dotenv import load_dotenv
from langchain.document_loaders.csv_loader import CSVLoader
# from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.chains.question_answering import load_qa_chain

# from text2vec import SentenceModel
# model = SentenceModel('shibing624/text2vec-base-chinese')
# sentences = ['你好', '👋']
# sentence_embeddings = model.encode(sentences)

from langchain.embeddings import HuggingFaceEmbeddings
from chromadb.config import Settings

load_dotenv()
OPENAI_API_KEY = os.environ['OPENAI_API_KEY']
OPENAI_API_BASE = os.environ['OPENAI_API_BASE']

PERSIST_DIRECTORY = 'chroma_storage_koubei'
CHROMA_SETTINGS = Settings(
    chroma_db_impl='duckdb+parquet',
    persist_directory=PERSIST_DIRECTORY,
    anonymized_telemetry=False
)

embeddings = HuggingFaceEmbeddings(
    model_name="shibing624/text2vec-base-chinese")
# embeddings = OpenAIEmbeddings()

if os.path.exists(PERSIST_DIRECTORY) != True:
    loader = CSVLoader(file_path='koubei.csv')
    data = loader.load()
    vectorstore = Chroma.from_documents(
        data, embeddings, persist_directory=PERSIST_DIRECTORY, client_settings=CHROMA_SETTINGS)
    vectorstore.persist()

vectordb = Chroma(persist_directory=PERSIST_DIRECTORY,
                  embedding_function=embeddings, client_settings=CHROMA_SETTINGS)

query = 'CR-V缺点多么？'
search_docs = vectordb.similarity_search(query, 2)
print(len(search_docs))
print(search_docs)

llm = ChatOpenAI(temperature=0, model_name='gpt-3.5-turbo')
chain = load_qa_chain(llm, chain_type='stuff')
results = chain.run(input_documents=search_docs, question=query)
print(f'Q: {query}')
print(f'A: {results}')
