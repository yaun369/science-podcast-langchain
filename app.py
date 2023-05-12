from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.chains.question_answering import load_qa_chain
import os
from dotenv import load_dotenv
import xml.etree.ElementTree as ET

load_dotenv()
OPENAI_API_KEY = os.environ['OPENAI_API_KEY']
OPENAI_API_BASE = os.environ['OPENAI_API_BASE']

embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY, openai_api_version='2020-11-07')


def load_pdf_courses(pdf_name):
    directory = 'chroma_storage_' + pdf_name
    # 如果本地不存在当前内容
    if os.path.exists(directory) != True:
        # 解析 pdf
        loader = PyPDFLoader('pdf_data/' + pdf_name + '.pdf')
        pages = loader.load_and_split()
        # 把解析好的内容分块
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=0)
        split_docs = text_splitter.split_documents(pages)
        print(f'{len(split_docs)} split_docs')
        # 把分块内容处理成 embeddings
        vectorstore = Chroma.from_documents(
            split_docs, embeddings, persist_directory=directory)
        # 结果持久化
        vectorstore.persist()
    return directory


persist_directory = load_pdf_courses('893')

vectordb = Chroma(persist_directory=persist_directory,
                  embedding_function=embeddings)
query = 'ChatGPT 和 OpenAI 什么关系？'
search_docs = vectordb.similarity_search(query, 2)
# print(search_docs)

llm = ChatOpenAI(temperature=0, model_name='gpt-3.5-turbo')
chain = load_qa_chain(llm, chain_type='stuff')
results = chain.run(input_documents=search_docs, question=query)
print(f'Q: {query}')
print(f'A: {results}')

speak = ET.Element('speak')
speak.set('xmlns', 'http://www.w3.org/2001/10/synthesis')
speak.set('xmlns:mstts', 'http://www.w3.org/2001/mstts')
speak.set('xmlns:emo', 'http://www.w3.org/2009/10/emotionml')
speak.set('version', '1.0')
speak.set('xml:lang', 'en-US')

voice = ET.SubElement(speak, 'voice')
voice.set('name', 'zh-TW-YunJheNeural')

prosody = ET.SubElement(voice, 'prosody')
prosody.set('rate', '20%')
prosody.set('pitch', '20%')
prosody.text = query + results

# ET.dump(speak)
tree = ET.ElementTree(speak)
tree.write(persist_directory + '/SSML.xml', encoding='utf-8')