from langchain.document_loaders.csv_loader import CSVLoader
import os
from dotenv import load_dotenv
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.chains.question_answering import load_qa_chain

load_dotenv()
OPENAI_API_KEY = os.environ['OPENAI_API_KEY']
OPENAI_API_BASE = os.environ['OPENAI_API_BASE']

embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

loader = CSVLoader(file_path='koubei.csv')
data = loader.load()
# print(len(data[:10]))

persist_directory = 'chroma_storage_koubei'

if os.path.exists(persist_directory) != True:
    vectorstore = Chroma.from_documents(
        data[:10], embeddings, persist_directory=persist_directory)
    vectorstore.persist()

vectordb = Chroma(persist_directory=persist_directory,
                  embedding_function=embeddings)

query = '名爵MG7外观怎么样？'
search_docs = vectordb.similarity_search(query, 3)
# print(search_docs)

llm = ChatOpenAI(temperature=0, openai_api_key=OPENAI_API_KEY,
                 model_name='gpt-3.5-turbo', api_base=OPENAI_API_BASE)
chain = load_qa_chain(llm, chain_type='stuff')
results = chain.run(input_documents=search_docs, question=query)
print(f'Q: {query}')
print(f'A: {results}')
