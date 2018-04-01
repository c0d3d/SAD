import csv

# def segment(y):
#     splits = []
#     for _ in range(len(y[0])):
#         splits.append([])

#     for z in y:
#         for idx, w in enumerate(z):
#             splits[idx % len(splits)].append(w)
#     return tuple(splits)


class Data:

    def __init__(self, train_iter, dev_iter, batch_size):
        next(train_iter, None) # Skip header
        self.train = []
        x = []
        while True:
            x = []
            i = 0
            nxt = next(train_iter, None)

            while i < batch_size and nxt is not None:
                x.append(tuple(nxt[1:]))
                i += 1
                nxt = next(train_iter, None)

            if len(x) > 0:
                self.train.append(x)

            if nxt is None:
                break

    def test_input(self):
        return self.train

    def eval_input(self):
        pass

    @classmethod
    def make_data(cls, train_file, dev_file, batch_size):
        t_reader = csv.reader(train_file, delimiter="\t")
        # TODO dev
        return cls(t_reader, None, batch_size)

class Training:
    def __init__(self, model, data, epoch_count):
        self.model = model
        self.data = data
        self.epoch_count = epoch_count
        self.cur_epoch = 0

    def has_more_epochs(self):
        return self.cur_epoch < self.epoch_count

    def next_epoch(self):
        self.model.run_train(self.data.test_input())
        # TODO eval
        return self.model.run_eval(self.data.eval_input())

    @classmethod
    def make_training(cls, model, the_data, epoch_count):
        return cls(model, the_data, epoch_count)
