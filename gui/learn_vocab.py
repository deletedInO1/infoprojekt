try:
    import tkinter as tk
except ModuleNotFoundError:
    import tk
import vocabulary
import random

window_exists = False

class Window:
    def __init__(self, vocabs:vocabulary.Vocabulary):
        
        self.vocabs = vocabs
        self.current_card = None
        

    def __call__(self):
        global window_exists
        if window_exists:
            return
        window_exists = True
        self.window = tk.Tk()
        self.vocab_question = tk.Label(self.window)
        self.vocab_solution = tk.Label(self.window)
        self.reveal_button = tk.Button(self.window, text="reveal", command=self.on_reveal)
        self.buttons = [
            tk.Button(self.window, text="nochmal", command=lambda : self.on_vote(0)),
            tk.Button(self.window, text="schwer", command=lambda : self.on_vote(1)),
            tk.Button(self.window, text="gut", command=lambda : self.on_vote(2)),
            tk.Button(self.window, text="einfach", command=lambda : self.on_vote(3))
        ]

        self.reveal_button.pack()
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_reveal(self):
        self.reveal_button.pack_forget()
        self.vocab_solution.pack()
        for b in self.buttons:
            b.pack()

    def on_vote(self, score):
        print(score)
        for b in self.buttons:
            b.pack_forget()
        self.vocab_solution.pack_forget()
        self.reveal_button.pack()
    
    def setup(self):
        self.current_card = random.choice(self.vocabs.cards)
        self.vocab_question.config(text=self.current_card[0])
        self.vocab_solution.config(text=self.current_card[1])
    
    def on_closing(self):
        global window_exists
        window_exists = False
        self.window.destroy()

if __name__ == "__main__":
    Window()()