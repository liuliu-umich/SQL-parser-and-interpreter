class Context:
    def __init__(self, key=None, value=None):
        self.map = dict()
        if key is not None and value is not None:
            self.add(key, value)

    # def __init__(self):
    #     self.map = dict()

    def add(self, key, value):
        self.map[key] = value

    def get(self, key):
        return self.map[key]
