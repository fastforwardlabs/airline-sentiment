import torch
import torch.nn as nn
import spacy
import json
import pickle
nlp = spacy.load('en')

data_dir = '/home/cdsw/airline-sentiment/data/'
model_dir = '/home/cdsw/airline-sentiment/model/'

# model
class RNN(nn.Module):
    def __init__(self, input_dim, embedding_dim, hidden_dim, output_dim):
       
        super().__init__()
        self.embedding = nn.Embedding(input_dim, embedding_dim)
        self.rnn = nn.RNN(embedding_dim, hidden_dim)
        self.fc = nn.Linear(hidden_dim, output_dim)
       
    def forward(self, text):

        # text = [sent len, batch size]
        embedded = self.embedding(text)
        # embedded = [sent len, batch size, emb dim]
        output, hidden = self.rnn(embedded)
        # output = [sent len, batch size, hid dim]
        # hidden = [1, batch size, hid dim]
        assert torch.equal(output[-1, :, :], hidden.squeeze(0))

        return self.fc(hidden.squeeze(0)), hidden


INPUT_DIM = 10002
# EMBEDDING_DIM = 100
EMBEDDING_DIM = 25
HIDDEN_DIM = 256
OUTPUT_DIM = 1
vocab_index = pickle.load(open(model_dir+'/vocab_index.pkl', 'rb'))
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = RNN(INPUT_DIM, EMBEDDING_DIM, HIDDEN_DIM, OUTPUT_DIM)
model.load_state_dict(torch.load('rnn_binary_pretrain_model.pt'))


def predict_sentiment_get_embedding(model, sentence):
    model.eval()
    tokenized = [tok.text for tok in nlp.tokenizer(sentence)]
    indexed = [vocab_index[t] for t in tokenized]
    tensor = torch.LongTensor(indexed).to(device)
    tensor = tensor.unsqueeze(1)
    # print(tensor)
    sentiment, hidden = model(tensor)
    prediction = torch.sigmoid(sentiment)
    return json.dumps({'sentiment': prediction.item(),
                       'embedding': hidden.data.tolist()})
