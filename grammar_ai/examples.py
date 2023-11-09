import random
from torch.utils.data import Dataset
import torch

subjects = [
    "i, you, she, he, it, we, they, the person, the tree, the house, the cat, the dog, my family, the adult, the floor",

]
verbs = ["eat, like, use, make, hate, insult, talk to, fall in love with, loathe, read, listen to"]
objects = ["me, you, her, him, it, us, them, me, you, her, him, it, us, them,  the person, the tree, the house, the cat, the dog, my family, the adult, the floor", ]


def decode(l):
    l2 = []
    for _l in l:
        l2 += _l.split(", ")
    return l2

subjects = decode(subjects)
verbs = decode(verbs)
objects = decode(objects)

dictionary = list(set(subjects+verbs+objects))
dictionary.sort()

class SentenceDataset(Dataset):
    def __init__(self) -> None:
        super().__init__()
        self.right = []
        self.wrong = []

    def generate(self, n):
        global subjects, verbs, objects
        for _ in range(n):
            for s in subjects:
                for v in verbs:
                    for o in objects:
                        right = [s, v, o]
                        wrong = [s, v, o]
                        random.shuffle(wrong)
                        #check wether wrong:
                        if not wrong[0] in subjects and wrong[1] in verbs and wrong[2] in objects:
                            
                            self.wrong.append(wrong)
                        self.right.append(right)

    def __getitem__(self, index):
        x = None
        y = None
        if index < len(self.right):
            x = self.right[index]
            y = 1
        else:
            x = self.wrong[index - len(self.right)]
            y = 0
        #print(x)
        return x, torch.Tensor([y])
        
    def __len__(self):
        return len(self.right) + len(self.wrong)