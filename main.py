import action
from langchain import hub
# from langchain.agents import AgentType, initialize_agent
from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings import OllamaEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import ChatOllama
from langchain.vectorstores import FAISS
import speech_recognition as sr
import voice


# llm deployed on local labs.
LLM_URL = "http://100.84.115.22:32123"
LLM_MODEL = "deepseek-r1:1.5b"
# LLM_MODEL = "llama3.2:1b"


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


if __name__ == "__main__":
    loader = TextLoader("DB.txt", encoding="utf-8")
    loaded_docs = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(loaded_docs)
    vector_store = FAISS.from_documents(documents=splits, embedding=OllamaEmbeddings(base_url=LLM_URL,model=LLM_MODEL))

    llm = ChatOllama(
        temperature=0,
        base_url=LLM_URL,
        model=LLM_MODEL
    )
    # llm_with_tools = llm.bind_tools(tools)
    # agent = initialize_agent(
    #     tools,
    #     llm,
    #     agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    #     verbose=True
    # )

    retriever = vector_store.as_retriever()
    prompt = hub.pull("rlm/rag-prompt")

    ae = action.ActionExecutor()
    rag_chain = (
            {"context": retriever | format_docs, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
    )

    vr = voice.VoiceRecognizer()
    while True:
        prompt = vr.recognize_speech_from_mic(sr.Recognizer(), sr.Microphone())
        if prompt == "":
            continue
        # just for debug
        # prompt = "我有点饿了"
        print("You said: " + prompt)

        response = rag_chain.invoke({"question": prompt + "---根据分析输出合适的需要执行的动作编号"})
        # agent.run(response)
        print(response)
        ae.run(response)