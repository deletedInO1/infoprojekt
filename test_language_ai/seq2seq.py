print("import modules...")
import torch
from torch import nn
from torch import optim
from torchtext.datasets import Multi30k
from torchtext.data import Field, BucketIterator
#from torch.utils.tensorboard import SummaryWriter
import numpy as np
import spacy
import random
import utils


device = "cuda"

l1 = "de"
l2 = "en"

spacy_l1 = spacy.blank(l1)
spacy_l2 = spacy.blank(l2)

def tokenizer_l2(text):
    return [tok.text for tok in spacy_l2.tokenizer(text)]
def tokenizer_l1(text):
    return [tok.text for tok in spacy_l1.tokenizer(text)]

lang2 = Field(tokenize=tokenizer_l2, lower=True, init_token="<sos>",
    eos_token="<eos>")
lang1 = Field(tokenize=tokenizer_l1, lower=True, init_token="<sos>",
    eos_token="<eos>") 

train_data, validation_data, test_data = Multi30k.splits(exts=("."+l1, "."+l2), fields=(lang1, lang2),root="data")


print("building vocab...")
lang1.build_vocab(train_data, max_size=1000, min_freq=2)
lang2.build_vocab(train_data, max_size=1000, min_freq=2)
print("vocab built")
class Encoder(nn.Module):
    def __init__(self, input_size, embedding_size, hidden_size, num_layers, dropout):
        #input size: vocab size
        super(Encoder, self).__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        
        self.dropout = nn.Dropout(dropout)
        self.embedding = nn.Embedding(input_size, embedding_size)
        self.lstm = nn.LSTM(embedding_size, hidden_size, num_layers, dropout=dropout)
    
    def forward(self, x):
        embedding = self.dropout(self.embedding(x))
        #(seq_length, N, embedding_size)
        outputs, (hidden, cell) = self.lstm(embedding)

        return hidden, cell

class Decoder(nn.Module):
    def __init__(self, input_size, embedding_size, hidden_size, output_size, num_layers, dropout):
        super(Decoder, self).__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.dropout = nn.Dropout(dropout)
        self.embedding = nn.Embedding(input_size, embedding_size)
        self.lstm = nn.LSTM(embedding_size, hidden_size, num_layers, dropout=dropout)
        self.fc = nn.Linear(hidden_size, output_size)
    
    def forward(self, x, hidden, cell):
        #shape of x: (N), we want (1, N), cause we want 1 word at a time
        x = x.unsqueeze(0)
        embedding = self.dropout(self.embedding(x))
        outputs, (hidden, cell) = self.lstm(embedding, (hidden, cell))
        pedictions = self.fc(outputs)
        #shape: (1, N, length_of_vocab)
        predictions = predictions.squeeze(0)

        return predictions, hidden, cell
    

class Seq2Seq(nn.Module):
    def __init__(self, encoder, decoder) -> None:
        super().__init__()
        self.encoder = encoder
        self.decoder = decoder
    
    def forward(self, source, target, teacher_force_ratio=0.5):
        batch_size = source.shape[1]
        target_len = source.shape[0]
        target_vocab_size = len(lang2.vocab)

        outputs = torch.zeros(target_len, batch_size, target_vocab_size).to(device)

        hidden, cell = self.encoder(source)

        x = target[0]
        for t in range(1, target_len):
            output, hidden, cell = self.decoder(x, hidden, cell)

            outputs[t] = output
            best_guess = output.argmax(1)
            if random.random() < teacher_force_ratio:
                x = target[t]
            else:
                x = buest_guess
        return outputs

# Training Hyperparameters:

num_epochs = 20
learning_rate = 0.001
batch_size = 64

# Model Hyperparameters
load_model = False
save_model = False

input_size_encoder = len(lang1.vocab)
input_size_decoder = len(lang2.vocab)
output_size = len(lang2.vocab)
encoder_embedding_size=300
decoder_embedding_size=300
hidden_size=1024
num_layers = 2

enc_dropout = 0.5
dec_dropout = 0.5

# Tensorboard 
#writer = SummaryWriter("logs")

print("setting up training...")
step = 0
train_iterator, valid_iterator, test_iterator = BucketIterator.splits((train_data, validation_data, test_data),
                                                                      batch_size=batch_size,
                                                                      sort_within_batch=True,
                                                                      sort_key = lambda x: len(x.src),
                                                                      device = device)

encoder = Encoder(input_size_encoder, encoder_embedding_size, hidden_size, num_layers, enc_dropout)
decoder = Decoder(input_size_decoder, decoder_embedding_size, hidden_size, num_layers, dec_dropout)

model = Seq2Seq(encoder, decoder)

optimizer = optim.Adam(model.parameters(), lr=learning_rate)

pad_idx = lang2.vocab.stoi["<pad>"]
criterion = nn.CrossEntropyLoss(ignore_index=pad_idx)

print("loading model...")
if load_model:
    utils.load_checkpoint(torch.load("checkpoint.pth"), model, optimizer)

for epoch in range(num_epochs):
    print(f"Epoch {epoch} / {num_epochs}")

    for batch_idx, batch in enumerate(train_iterator):
        inp_data = batch.src.to(device)
        target = batch.trg.to(device)
        output = model(inp_data, target)
        output = output[1:].reshape(-1, output.shape[2])
        target = target[1:].reshape(-1)
        optimizer.zero_grad()
        loss = criterion(output, target)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1)
        optimizer.step()

        #writer.add_scalar("Training loss", loss, global_step=step)
        step += 1

    if save_model:
        checkpoint = {"state_dict": model.state_dict(), "optimizer": optimizer.state_dict()}
        utils.save_checkpoint(checkpoint, "checkpoint.pth")
