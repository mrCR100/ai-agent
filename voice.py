import speech_recognition as sr

def recognize_speech_from_mic(recognizer, microphone):
    """Transcribe speech from recorded from `microphone`."""
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `speech_recognition.Recognizer` instance")
    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `speech_recognition.Microphone` instance")

    # adjust the recognizer sensitivity to ambient noise and record audio
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening...")
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
    # just recognize the speech in Chinese
        recognized_prompt = recognizer.recognize_vosk(audio, language="zh-CN")
        print("You said: " + recognized_prompt)
    except sr.UnknownValueError:
        print("Recognizer could not understand audio")
    except sr.RequestError as e:
        print(f"Could not request results from vosk model; {e}")
