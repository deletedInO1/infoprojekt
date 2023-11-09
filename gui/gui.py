try:
    import tkinter as tk
except ModuleNotFoundError:
    import tk
import translate
import llamacpp
import random
import vocabulary
from gui import learn_vocab
import text_to_speech
import threading
import text_to_speech

class Window:
    def __init__(self):
        self.vocabulary = vocabulary.Vocabulary()
        self.vocabulary.load()
        self.vocabulary.get_current()

        self.window = tk.Tk()
        self.vocab_window = learn_vocab.Window(self.vocabulary)

        self.txt_input = tk.Text(self.window, height=2)
        self.vc_text = tk.Label(self.window, height=2, text="vc")
        self.output_text = tk.Message(self.window, text="answer")
        self.output_text.config(aspect=300)
        self.vocab_input = tk.Text(self.window, height=1)
        self.vocab_output = tk.Label(self.window)
        self.add_vocab = tk.Button(self.window, command=self.on_add_vocab)
        self.vocabs = tk.Label()
        self.learn_vocab = tk.Button(self.window,text="Vokabeln lernen", command=self.vocab_window)

        self.txt_input.bind("<Return>", self.on_txt_input)
        self.vocab_input.bind("<Return>", self.on_vocab_input)

        self.txt_input.pack()
        self.vc_text.pack()
        self.output_text.pack()
        self.vocab_input.pack()
        self.vocab_output.pack()
        self.add_vocab.pack()
        self.vocabs.pack()
        self.learn_vocab.pack()

        self.input = "hi"
        self.vocab_in = None
        self.vocab_out = None

        self.accept_input = False
        self.activate_input()

        self.update_vocab()


    def __call__(self):
        self.window.mainloop()
    
    def on_txt_input(self, event):
        if self.accept_input:
            self.input = self.txt_input.get('1.0', "end")
            if self.input.startswith("\n"):
                self.input = str(self.input[1:])
            self.txt_input.mark_set("insert", "%d.%d" % (0, 0))
            self.txt_input.delete("1.0", "end")
            self.run_input()
        else:
            self.input = self.txt_input.get('1.0', "end")
            self.txt_input.mark_set("insert", "%d.%d" % (0, 0))
            self.txt_input.delete("1.0", "end")
            self.txt_input.insert(tk.END, self.input[:-1])

    def run_input(self):
        self.deactivate_input()

        
        def llama():
            try:
                outp = llamacpp.run(self.input)
                self.vc_text.config(text= self.input)
                self.output_text.config(text=outp)
                text_to_speech.speech(outp)
            except Exception as e:
                print(e)
            self.activate_input()
        t = threading.Thread(target=llama)
        t.daemon = True
        t.start()

    def on_vocab_input(self, event):
        vocab = self.vocab_input.get('1.0', "end")[:-1]
        if vocab.startswith("\n"):
            vocab = vocab[1:]
        self.vocab_input.mark_set("insert", "%d.%d" % (0, 0))
        self.vocab_input.delete("1.0", "end")

        vocab_out = translate.translate(vocab)
        text_to_speech.speech(vocab_out)

        self.vocab_output.config(text=vocab_out)

        self.vocab_in = vocab
        self.vocab_out = vocab_out

    def on_add_vocab(self):
        if self.vocab_in is None or self.vocab_out is None:
            return
        
        self.vocabulary.add_save(self.vocab_in, self.vocab_out)
        self.update_vocab()

    def update_vocab(self):
        s = ""
        for v in self.vocabulary.cards:
            s += str(v) + "\n"
        self.vocabs.config(text=s)

    def activate_input(self):
        self.accept_input = True
        self.txt_input.config(background="white")
    def deactivate_input(self):
        self.accept_input = False
        self.txt_input.config(background="red")