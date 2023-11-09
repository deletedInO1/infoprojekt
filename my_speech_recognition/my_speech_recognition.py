import speech_recognition as sr
from my_speech_recognition import my_vosk

r = sr.Recognizer()
r.pause_threshold = 0.2
r.non_speaking_duration = 0.1



def listen():
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        #print(source.list_working_microphones())
        audio = r.listen(source)
    
    print("-----")
    #try:
    #    text = r.recognize_google(audio)
    #except sr.UnknownValueError as e:
    #    print(e)
    #    return
    #except sr.RequestError as e:
    #    print(e)
    #    return
    #return text

    try:
        text = my_vosk.recognize(audio)
    except sr.UnknownValueError as e:
        print(e)
        return
    except sr.RequestError as e:
        print(e)
        return
    return text



if __name__ == "__main__":
    while True:
        print(listen())