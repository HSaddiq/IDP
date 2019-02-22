class bot:
    def __init__(self):
        self.x = None
        self.y = None
        self.bearing = None

class box:
    def __init__(self, x, y, processed):
        self.x = x
        self.y = y
        self.processed = processed
