from dotenv import load_dotenv
import os

from langchain.document_loaders.csv_loader import CSVLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores.pgvector import PGVector
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQA,ConversationalRetrievalChain
from langchain import PromptTemplate

from config import CONNECTION_STRING

load_dotenv()
os.environ['OPENAI_API_KEY'] = os.getenv('api_key')


def generate_response(user_message):
    loader = CSVLoader(file_path='data/people-100.csv')
    documents = ""
    for i in loader.load():
        e = i.page_content
        documents += e

    text_splitter = CharacterTextSplitter(chunk_size = 300,chunk_overlap  = 0)
    docs = text_splitter.split_text(documents)

    embeddings = OpenAIEmbeddings()

    db = PGVector.from_texts(
        texts=docs,
        embedding=embeddings,
        collection_name="data_of_demod",
        connection_string=CONNECTION_STRING,
        openai_api_key=os.environ['OPENAI_API_KEY'],
        pre_delete_collection=False,

    )

    llm = ChatOpenAI(
        openai_api_key=os.environ["OPENAI_API_KEY"],
        model_name='gpt-3.5-turbo',
        temperature=0.0,
        max_tokens=50
    )


    template = """
    I want you to act as an Assistant.
    I will share information with you, and you have to respond accordingly. 
    Your response should be a two-line complete sentence. If the user asks a question that is not related to the information, 
    respond with "I am sorry I didn't understand"
    your request." without any explanations or additional words. Please follow these instructions strictly and carefully.
    Context: {context}
    Question: {question}
    Answer:
    """

    # template = """"You are an AI conversational assistant to answer questions based on a context.
    # You are given data from a csv file and a question, you must help the user find the information they need. 
    # Your answers should be friendly, in the same language.
    # question: {question}
    # =======
    # context: {context}
    # """

    PROMPT = PromptTemplate(template=template, input_variables=["context", "question"])
    chain_type_kwargs = {"prompt": PROMPT}

    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=db.as_retriever(),
        chain_type_kwargs= chain_type_kwargs
    )

    # Generate AI response using prompt templates
    try:
        response = qa.run(user_message)
    except Exception as e:
        response = "I am sorry I didn't understand your request."

    return response


