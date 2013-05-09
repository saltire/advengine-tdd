from dictionary import Dictionary


class Adventure:
    def __init__(self, data):
        self.dict = Dictionary(data['words'])
        