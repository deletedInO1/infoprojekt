import vosk
import json

model = vosk.Model(f"D:\\Schule\\Info\\projekt\\my_speech_recognition\\model")
rec = vosk.KaldiRecognizer(model, 16000)


def recognize(audio_data):
    rec.AcceptWaveform(audio_data.get_raw_data(convert_rate=16000, convert_width=2))
    finalRecognition = rec.FinalResult()
    return json.loads(finalRecognition)["text"]