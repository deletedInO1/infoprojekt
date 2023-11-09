import llm_model

    

print("hi")
llm_model.load()

x = llm_model.use(llm_model.system_prompt)
print(x)

while True:
    i = input("say something: ")
    if i == "/stop":
        break
    else:
        print(llm_model.use(llm_model.prompt_template.replace("%1", i)))
    
print("Bye")