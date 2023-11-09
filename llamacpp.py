import socket

def run(prompt):
    out = ""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(("localhost", 1324))
        s.sendall(prompt.encode())
        while True:
            data = s.recv(1024)
            if not data:
                break
            byte_text = bytearray()
            for b in data:
                if b == 0x03:
                    break
                byte_text.append(b)
                #print(chr(b), end="")
            else:
                out += byte_text.decode()
                continue
            out += byte_text.decode()
            break
    return out


#
# import os
# import config
# import subprocess
# import time
# #-m {config.USB_STICK}:\programs\gpt4all\mymodels\llama-2-7b-chat.ggmlv3.q2_K.bin
#
# #print("D:\\programs\\lamacpp\\llama.cpp\\build\\bin\\Release\\main.exe  -m D:\programs\gpt4all\mymodels\llama-2-7b-chat.ggmlv3.q2_K.bin")
#
#
# def command(main, model, threads = 3, context_size=2048, temp=0.7): #threads: 8 in video
#     return f"{main} -ins -t {str(threads)} -ngl 1 -m {model} -c {str(context_size)} --temp {str(temp)} \
#         --repeat_penalty 1.1 -s 42 -n -1"
#
# def run(prompt): # doesn't use prompt yet
#     with open("prompt_base.txt") as f:
#         with open("prompts.txt", "w") as f2:
#             f2.write(f.read().replace("%1", prompt))
#     command = f"{config.LLAMA_CPP_POS} -m {config.MODEL_POS} -n 2000 \
#                       -f {config.USB_STICK}:\\Schule\\Info\\projekt\\prompts.txt"
#     print(command)
#     t :str = os.popen(command
#                       ).read()[3:-1]
#     with open("f.txt", "w") as f:
#         f.write(t)
#     #return t[t.find()]a
#     return t
#
# def run_console():
#     cmd = command(f"{config.LLAMA_CPP_POS}",
#                   config.MODEL_POS)
#     print("LOL1")
#     p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
#     print("LOL2")
#     p.stdin.write("hey, how are you?".encode())
#     print("LOL3")
#     time.sleep(1)
#     while True:
#         print(p.stdout.readline())
#
#
# print(command(f"{config.LLAMA_CPP_POS}",
#                   config.MODEL_POS))
# t = run("hi")
# print(t)

#run_console()


if __name__ == "__main__":
    print(run(input()))