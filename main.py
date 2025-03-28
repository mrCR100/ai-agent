import speech_recognition as sr
import voice

if __name__ == "__main__":
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    voice.recognize_speech_from_mic(recognizer, microphone)