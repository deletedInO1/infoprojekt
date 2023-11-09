import json
import os.path
import datetime

FILE = "cards.json"

_INP = "inp"
_OUTP = "outp"
_DATE = "date"
_FREQ = "freq"

class Vocabulary:
    def __init__(self) -> None:
        
        self.cards = []


    def load(self):
        if not os.path.exists(FILE):
            return []

        with open(FILE) as f:
            self.cards = json.load(f)
        return self.cards
    
    def add_save(self, inp, outp):
        date = datetime.datetime.now().date()
        card = {_INP: inp, _OUTP: outp, _DATE: str(date), _FREQ: 1}
        self.cards.append(card)
        with open(FILE, "w") as f:
            json.dump(self.cards, f)
    
    def get_current(self):
        l = []
        current_date = datetime.datetime.now().date()
        print("hey")
        for c in self.cards:
            date = datetime.datetime.strptime(c[_DATE], "%Y-%m-%d").date()
            difference = date - current_date
            days_difference = difference.total_seconds() / 60 / 60 / 24
            frequency = c[_FREQ]
            if days_difference+1 >= frequency:
                l.append(c)
                print(c) 

    def answered(self, card_original, answer_id):
        i = self.cards.index(card_original)
        self.cards[i][_DATE] = str(datetime.datetime.now().date())
        self.cards[i][_FREQ] *= 2

if __name__ == "__main__":
    v = Vocabulary()
    v.load()
    print(v.cards)
    c = v.cards[0]
    v.answered(c, )

            

