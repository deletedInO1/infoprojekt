import torch
from torch import nn
import random
class Model(nn.Module):
    def __init__(self, dict_size, word_type_vector=3) -> None:
        super().__init__()
        
        self.dictionary = nn.Sequential(nn.Linear(dict_size, word_type_vector), nn.Sigmoid())

        self.embedding = nn.Embedding(dict_size, 90)
        self.dropout = nn.Dropout(0.5)
        self.lstm = nn.LSTM(90, 30, 30, dropout=0.1)
        
        self.flatten = nn.Flatten()
        #self.main = nn.Linear(90*3, 90)
        self.fc = nn.Linear(30*3, 1)
        self.a = nn.Sigmoid()

        self.dict_size = dict_size
        self.word_type_vector=word_type_vector

    def forward(self, x):
        x = self.embedding(x)
        x = self.dropout(x)
        x = x.view(x.shape[0], x.shape[1], -1)
        x, (hidden, cell) = self.lstm(x)
        
        
        x = self.flatten(x)
        #x = self.main(x)
        x = self.a(self.fc(x))
        return x


if __name__ == "__main__":
    m = Model(6)
    print(m.forward(torch.IntTensor([[1,2,3,4,5,6]])))
    m.train()

    criterion = nn.MSELoss()
    optimizer = torch.optim.Adam(m.parameters(), lr=0.001)

    for i in range(1000):
        y = m(torch.IntTensor([[int(random.random()*10) for _ in range(6)]]))
        loss = criterion(y, torch.Tensor([[0.2]]))
        print(y, loss)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
