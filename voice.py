import os
import speech_recognition as sr
from vosk import KaldiRecognizer, Model


def recognize_by_vosk(vosk_model, audio_data):
    assert isinstance(audio_data, sr.AudioData), "Data must be audio data"
    if not os.path.exists("model"):
        return "Please download the model from https://github.com/alphacep/vosk-api and unpack as 'model' in the current folder."

    rec = KaldiRecognizer(vosk_model, 16000)
    rec.AcceptWaveform(audio_data.get_raw_data(convert_rate=16000, convert_width=2))
    final_recognition = rec.FinalResult()
    return final_recognition


class VoiceRecognizer(object):
    def __init__(self):
        self.vosk_model = Model("model")

    def recognize_speech_from_mic(self, recognizer, mic):
        """Transcribe speech from recorded from `microphone`."""
        if not isinstance(recognizer, sr.Recognizer):
            raise TypeError("`recognizer` must be `speech_recognition.Recognizer` instance")
        if not isinstance(mic, sr.Microphone):
            raise TypeError("`microphone` must be `speech_recognition.Microphone` instance")

        # adjust the recognizer sensitivity to ambient noise and record audio
        with mic as source:
            recognizer.adjust_for_ambient_noise(source)
            print("Listening...")
            audio = recognizer.listen(source)

        try:
            # print("Recognizing...")
        # just recognize the speech in Chinese
            recognized_prompt = recognize_by_vosk(self.vosk_model, audio)
            return  recognized_prompt
        except sr.UnknownValueError:
            print("Recognizer could not understand audio")
        except sr.RequestError as e:
            print(f"Could not request results from vosk model; {e}")
