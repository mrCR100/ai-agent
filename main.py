from langchain_core.messages import AIMessage

import action
import re
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings import OllamaEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import ChatOllama
from langchain.vectorstores import FAISS

from flask import Flask, request, jsonify
from flask_cors import CORS


# llm deployed on local labs.
LLM_URL = "http://100.84.115.22:32123"
LLM_MODEL = "deepseek-r1:1.5b"

DATASET_DIR = "dataset"

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def extract_final_output(message: AIMessage) -> str:
    return message.content.split("\n")[-1]


user_prompt = ""

app = Flask(__name__)
CORS(app)


@app.route('/chat', methods=['POST'])
def chat():
    global user_prompt
    if request.is_json:
        user_prompt = request.get_json()
        print("Received JSON format prompt:", user_prompt)
        service_response = \
            service_chain.invoke({"question": user_prompt["message"] + "---根据分析输出合适的需要执行的动作编号"})
        print("原始输出："+service_response)
        judge_response = judge_chain.invoke(service_response)
        print(judge_response)
        ae.run(service_response)
        return jsonify({"status": "success",
                        "judge_response": judge_response,
                        "service_response": service_response}), 200
    else:
        return jsonify({"status": "error", "message": "Request must be JSON"}), 400


if __name__ == "__main__":
    loader = TextLoader(DATASET_DIR + "/action.txt", encoding="utf-8")
    loaded_docs = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(loaded_docs)
    vector_store = FAISS.from_documents(documents=splits,
                                        embedding=OllamaEmbeddings(base_url=LLM_URL,model=LLM_MODEL))

    llm = ChatOllama(
        temperature=0,
        base_url=LLM_URL,
        model=LLM_MODEL
    )

    retriever = vector_store.as_retriever()

    rag_prompt_template = """
    You are an assistant for question-answering tasks. 
    Use the following pieces of retrieved context to answer the question. 
    If you don't know the answer, just say that you don't know. 
    Use three sentences maximum and keep the answer concise.
    Question: {question} 
    Context: {context} 
    Answer:
    """
    rag_prompt = PromptTemplate.from_template(rag_prompt_template)

    ae = action.ActionExecutor()

    service_chain = (
            {"context": retriever | format_docs, "question": RunnablePassthrough()}
            | rag_prompt
            | llm
            | extract_final_output
            | StrOutputParser()
    )

    judge_prompt_template = """
    You are an assistant for question-answering tasks. 
    Use the following pieces of retrieved context to answer the question.
    Use three sentences maximum and keep the answer concise.
    Question: {service_response}---Check or judge if the response reasonable? 
    Context: {context} 
    Answer:
    """

    judge_prompt = PromptTemplate.from_template(judge_prompt_template)

    judge_chain = (
            {"context": retriever | format_docs, "service_response": RunnablePassthrough()}
            | judge_prompt
            | llm
            | StrOutputParser()
    )

    app.run(host="0.0.0.0", debug=True)
