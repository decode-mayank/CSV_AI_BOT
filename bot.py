from langchain.document_loaders.csv_loader import CSVLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores.pgvector import PGVector
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv
from langchain.embeddings import OpenAIEmbeddings
from config import CONNECTION_STRING
from langchain.chains import RetrievalQA
from langchain import PromptTemplate
import os

load_dotenv()
os.environ['OPENAI_API_KEY'] = os.getenv('api_key')


def generate_response(user_message):
    loader = CSVLoader(file_path='data/people-100.csv')
    documents = loader.load()
    
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    docs = text_splitter.split_documents(documents)

    embeddings = OpenAIEmbeddings()

    db = PGVector.from_documents(
        documents=docs,
        embedding=embeddings,
        collection_name="data_of_demod",
        connection_string=CONNECTION_STRING,
        openai_api_key=os.environ['OPENAI_API_KEY'],
        pre_delete_collection=False,
    )
    
    llm = ChatOpenAI(
        openai_api_key=os.environ["OPENAI_API_KEY"],
        model_name='gpt-3.5-turbo',
        temperature=0.2,
        max_tokens=50
    )

    template = """
    I want you to act as an "MS" BOT. If the user asks a greeting question then give a helpful response. I will share information with you, and you have to respond accordingly. 
    Your response should be a two-line complete sentence. If the user asks a question that is not related to the information,respond with "I am sorry I didn't understand
    your request." without any explanations or additional words. Please follow these instructions strictly and carefully.
    Context: {context}
    Question: {question}
    Answer:
    """ 

    PROMPT = PromptTemplate(template=template, input_variables=["context", "question"])
    chain_type_kwargs = {"prompt": PROMPT}
    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=db.as_retriever(),
        chain_type_kwargs=chain_type_kwargs,
    )

    # Generate AI response using prompt templates
    try:
        response = qa.run(user_message)
    except Exception as e:
        response = "I am sorry I didn't understand your request."

    return response







