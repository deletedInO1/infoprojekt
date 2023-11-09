import gpt4all
model : gpt4all.GPT4All= None

system_prompt = "### System:\nYou are an AI assistant who gives quality response to whatever humans ask of you."
prompt_template = """### Human:
%1
### Assistant:"""

def load():
    global model
    model = gpt4all.GPT4All("llama-2-7b-chat.ggmlv3.q2_K.bin", model_path="D:\\programs\\gpt4all\\mymodels\\",
                            allow_download=False, n_threads=4)

def use(inp, **kwargs):
    return model.generate(inp, n_batch=128, **kwargs)

load()
print(use("hi, how are you?"))