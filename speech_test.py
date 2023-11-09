import llamacpp
import my_speech_recognition.my_speech_recognition as my_speech_recognition
import text_to_speech
print("loading model ...")
#llm_model.load()
print("answer to the system prompt:")
#print(llamacpp.run(llm_model.system_prompt, max_tokens=10))

print("----------------------------------------")
print("listening...")
while True:
    inp = my_speech_recognition.listen()
    if inp is None:
        continue
    print("input:\t", inp)
    outp = llamacpp.run(inp)
    text_to_speech.speech(outp)
    print("response:\t", outp)
    print("")