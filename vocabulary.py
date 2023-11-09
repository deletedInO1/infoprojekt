import json
import os.path
import datetime

FILE = "cards.json"

_INP = "inp"
_OUTP = "outp"
_DATE = "date"
_FREQ = "freq"

_AGAIN = 0
_HARD = 1
_GOOD = 2
_EASY = 3

class Vocabulary:
    def __init__(self) -> None:
        
        self.cards = []


    def load(self):
        if not os.path.exists(FILE):
            return []

        with open(FILE) as f:
            self.cards = json.load(f)
        return self.cards
    
    def _add(self, inp, outp):
        date = datetime.datetime.now().date()
        card = {_INP: inp, _OUTP: outp, _DATE: str(date), _FREQ: 1}
        self.cards.append(card)
    
    def add_save(self, inp, outp):
        self._add(inp, outp)
        self.save()

    def save(self):
        with open(FILE, "w") as f:
            json.dump(self.cards, f)

    def get_current(self):
        l = []
        current_date = datetime.datetime.now().date()
        for c in self.cards:
            date = datetime.datetime.strptime(c[_DATE], "%Y-%m-%d").date()
            difference = date - current_date
            days_difference = difference.total_seconds() / 60 / 60 / 24
            if days_difference <= 0:
                l.append(c)
        return l
    
    def card_date(self, card):
        return datetime.datetime.strptime(card[_DATE], "%Y-%m-%d").date()

    def answered(self, card_original, answer_id):
        i = self.cards.index(card_original)
        date = self.card_date(cards[i])
        freq = self.cards[i][_FREQ] 
        #self.cards[i][_DATE] = str(datetime.datetime.now().date())
        if answer_id == _AGAIN:
            freq = 1
        elif answer_id == _HARD:
            date += datetime.timedelta(days=freq//2)
        elif answer_id == _GOOD:
            date += datetime.timedelta(days=freq)
            freq *= 2
        elif answer_id == _EASY:
            date += datetime.timedelta(days=freq*4)
            freq *= 3
        
        cards[i][_DATE] = str(date)
        cards[i][_FREQ] = freq

        self.save()


if __name__ == "__main__":
    for t in range(4):
        v = Vocabulary()
        v._add("", "")
        cards = v.get_current()
        assert len(cards) == 1
        card = cards[0]
        #v.answered(card, _GOOD)
        print(card)
        v.answered(card, t)
        print(cards)
        print(v.get_current())
        print("----------")