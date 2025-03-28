import speech_recognition as sr
import voice
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage

# llm deployed on local labs.
LLM_URL = "http://100.84.115.22:32123"
LLM_MODEL = "deepseek-r1:1.5b"

if __name__ == "__main__":
    llm = ChatOllama(
        temperature=0,
        base_url=LLM_URL,
        model=LLM_MODEL
    )
    vr = voice.VoiceRecognizer()
    while True:
        prompt = vr.recognize_speech_from_mic(sr.Recognizer(), sr.Microphone())
        if prompt == "":
            continue
        print("You said: " + prompt)
        response = llm.invoke([HumanMessage(content=prompt)])
        print(response.content)