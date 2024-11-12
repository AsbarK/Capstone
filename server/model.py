import os
import pandas as pd
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_groq import  ChatGroq
from dotenv import load_dotenv
load_dotenv()


GROK_API_KEY = os.getenv('GROKAPI')

persistent_directory = os.path.join('.', "db", "chroma_db_with_metadata")
# Use SentenceTransformer to create local embeddings

embed = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")



# Initialize Chroma vector store with the embedding function
db = Chroma(
    collection_name="csv_data",
    persist_directory=persistent_directory,
    embedding_function=embed
)
df1 = pd.read_csv("../chocolately_code_pred.csv")
df1 = df1.drop('Predicted Code', axis=1)
df2 = pd.read_csv("../Final_Updated_Email_Management_Tasks_new.csv")
df2 = df2.drop(["Unnamed: 2","Unnamed: 3","Unnamed: 4"], axis=1)
df2 = df2.rename(columns={
    'Task Description': 'Software',
    'Google Apps Script Code':'Target Code'
})

df = pd.concat([df1, df2], ignore_index=True)

retriever = db.as_retriever(
    search_type="mmr",
    search_kwargs={"k": 2},
)
# Create a ChatOpenAI model
llm = ChatGroq(api_key=GROK_API_KEY,model="llama3-8b-8192")

# Contextualize question prompt
# This system prompt helps the AI understand that it should reformulate the question
# based on the chat history to make it a standalone question
contextualize_q_system_prompt = (
    "Given a chat history and the latest user question "
    "which might reference context in the chat history, "
    "formulate a standalone question which can be understood "
    "without the chat history. Do NOT answer the question, just "
    "reformulate it if needed and otherwise return it as is."
)

# Create a prompt template for contextualizing questions
contextualize_q_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", contextualize_q_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)

# Create a history-aware retriever
# This uses the LLM to help reformulate the question based on chat history
history_aware_retriever = create_history_aware_retriever(
    llm, retriever, contextualize_q_prompt
)

# Answer question prompt
# This system prompt helps the AI understand that it should provide concise answers
# based on the retrieved context and indicates what to do if the answer is unknown
# qa_system_prompt = (
#     "You are an assistant for question-answering tasks. You are an expert in writing Downloading Scripts for windows"
#     "and Email management Scripts. Use "
#     "the following pieces of retrieved context to answer the "
#     "question. Just give the script and be consise."
#     "\n\n"
#     "{context}"
# )
qa_system_prompt = (
    "You are an assistant for question-answering tasks. You are an expert in writing Downloading Scripts(use Chocolately)"
    "and Email management Scripts(use the Google Apps Script). Use "
    "the following context of scripts as base to answer the "
    "question. Just give the script."
    "\n\n"
    "{context}"
)

# Create a prompt template for answering questions
qa_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", qa_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)

# Create a chain to combine documents for question answering
# `create_stuff_documents_chain` feeds all retrieved context into the LLM
question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)

# Create a retrieval chain that combines the history-aware retriever and the question answering chain
rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)


def createVectorDB():
    texts = []
    metadatas = []
    ids = []
    for _, row in df.iterrows():
        texts.append(row['Software'])
        texts.append(row['Target Code'])
        metadatas.append({'Software': row['Software'], 'Target Code': row['Target Code']})
        metadatas.append({'Software': row['Software'], 'Target Code': row['Target Code']})
        ids.append(f"{row.name}_0")
        ids.append(f"{row.name}_1")

    db.add_texts(
        texts=texts,
        metadatas=metadatas,
        ids=ids
    )
def continual_chat(query,chat_history):
    # Process the user's query through the retrieval chain
    result = rag_chain.invoke({"input": query, "chat_history": chat_history})
    # Display the AI's response
    #print(f"AI: {result}")
    print(f"AI: {result['answer']}")
    # Update the chat history

    return result

