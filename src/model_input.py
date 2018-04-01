

class ModelInput:

    def __init__(self, titles, bodies, judgments):
        self.titles = titles
        self.bodies = bodies
        self.judgments = judgments

    def __iter__(self):
        def nxt():
            for t, b, j in self.titles, self.bodies, self.judgments:
                yield (t, b, j)
        return nxt()
