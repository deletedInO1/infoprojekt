from model import Model
import examples

import torch
from torch import nn
from torch.utils.data import DataLoader


DEVICE = "cuda"



def eval():
    
    d = torch.load("grammar_ai/model.pth")
    m = Model(d["dict_size"], d["word_type_vector"])
    m.load_state_dict(d["model"])
    m = m.to(DEVICE)
    #print(m.state_dict())
    m.eval()

    ds2 = examples.SentenceDataset()
    ds2.generate(10)
    dl2 = DataLoader(ds2, batch_size=32)

    accuracy = torch.FloatTensor([0]).to(DEVICE)
    count = 0
    for x, target in dl2:
            x = [[examples.dictionary.index(x[i][j]) for i in range(len(x))] for j in range(len(x[0]))]
            #x = nn.functional.one_hot(torch.LongTensor(x), len(examples.dictionary)) #TODO: Is this even necessary?
            #x = x.type(torch.FloatTensor)
            
            x = torch.LongTensor(x).to(DEVICE)
            target = target.to(DEVICE)
            y = m(x)
            accuracy += torch.sum((y> 0.5) == (target > 0.5))/target.shape[0]
            count += 1
    accuracy = accuracy / count 
    print(accuracy)
    d = {"dict_size": m.dict_size, "word_type_vector":m.word_type_vector, "model": m.state_dict()}
    torch.save(d, "grammar_ai/model.pth")
           
eval()