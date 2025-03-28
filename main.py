import speech_recognition as sr
import voice

if __name__ == "__main__":
    vr = voice.VoiceRecognizer()
    while True:
        prompt = vr.recognize_speech_from_mic(sr.Recognizer(), sr.Microphone())
        print("You said: " + prompt)