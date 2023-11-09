from model import Model
import examples

import torch
from torch import nn
from torch.utils.data import DataLoader

import random

DEVICE = "cuda"

def train():
    m = Model(len(examples.dictionary)).to(DEVICE)
    #print(m.forward(torch.IntTensor([[1,2,3,4,5,6]])))
    m.train()

    ds = examples.SentenceDataset()
    ds.generate(10)
    
    dl = DataLoader(ds, batch_size=32, shuffle=True)

    criterion = nn.MSELoss()
    optimizer = torch.optim.Adam(m.parameters(), lr=0.02)
    for i in range(1):
        print("epoch:", i)
        for x, target in dl:
            x = [[examples.dictionary.index(x[i][j]) for i in range(len(x))] for j in range(len(x[0]))]
            #x = nn.functional.one_hot(torch.LongTensor(x), len(examples.dictionary)) #TODO: Is this even necessary?
            #x = x.type(torch.FloatTensor)
            x = torch.LongTensor(x).to(DEVICE)
            target = target.to(DEVICE)
            y = m(x)
            loss = criterion(y, target)
            #print(torch.sum((y> 0.5) == (target > 0.5))/target.shape[0])

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()


    ds2 = examples.SentenceDataset()
    ds2.generate(1)
    dl2 = DataLoader(ds2, batch_size=32, shuffle=False)

    m.eval()
    accuracy = torch.FloatTensor([0]).to(DEVICE)

    count = 0
    wrong = []
    for s, target in dl2:
            x = [[examples.dictionary.index(s[i][j]) for i in range(len(s))] for j in range(len(s[0]))]
            #x = nn.functional.one_hot(torch.LongTensor(x), len(examples.dictionary)) #TODO: Is this even necessary?
            #x = x.type(torch.FloatTensor)
            
            x = torch.LongTensor(x).to(DEVICE)
            target = target.to(DEVICE)
            y = m(x)
            correct = (y> 0.5) == (target > 0.5)
            accuracy += torch.sum(correct)/target.shape[0]
            
            count += 1
            for i in range(correct.shape[0]):
                if not correct[i].item():
                    l = []
                    for j in range(3):
                        l.append(s[j][i])
                    print(l, target[i])
    accuracy = accuracy / count 
    print(accuracy)
    d = {"dict_size": m.dict_size, "word_type_vector":m.word_type_vector, "model": m.state_dict()}
    torch.save(d, "grammar_ai/model.pth")

if __name__ == "__main__":
    train()