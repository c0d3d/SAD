import csv

def read_csv(itr, batch_size):
    ans = []
    while True:
        x = []
        i = 0
        nxt = next(itr, None)
        last_row = None
        while i < batch_size and nxt is not None:
            x.append(tuple(nxt[2:]))
            last_row = tuple(nxt[2:])
            i += 1
            nxt = next(itr, None)

        while len(x) < batch_size:
            x.append(last_row)

        ans.append(x)

        if nxt is None:
            break
    return ans

class Data:

    def __init__(self, train_iter, dev_iter, batch_size):
        self.train = read_csv(train_iter, batch_size)
        self.dev = read_csv(dev_iter, batch_size)

    def test_input(self):
        return self.train

    def eval_input(self):
        return self.dev

    @classmethod
    def make_data(cls, train_file, dev_file, batch_size):
        t_reader = csv.reader(train_file, delimiter="\t")
        next(t_reader, None) # Skip header
        d_reader = csv.reader(dev_file, delimiter="\t")
        next(d_reader, None) # Skip header
        return cls(t_reader, d_reader, batch_size)

class Training:
    def __init__(self, model, data, epoch_count):
        self.model = model
        self.data = data
        self.epoch_count = epoch_count
        self.cur_epoch = 0

    def has_more_epochs(self):
        return self.cur_epoch < self.epoch_count

    def next_epoch(self):
        self.cur_epoch += 1
        self.model.run_train(self.data.test_input())
        if self.data.eval_input() is not None:
            ans = self.model.run_eval(self.data.eval_input())
        else:
            print("Skipping eval ...")
            return

        correct_count = 0
        total = 0

        tp = 0
        tn = 0
        fp = 0
        fn = 0

        for batch_ans in ans:
            for actual, expected in batch_ans:
                print(actual[0], "vs.", expected)
                total += 1
                v = int(round(actual[0]))
                correct = v == expected
                if correct:
                    correct_count += 1
                    if v == 0:
                        tn += 1
                    else:
                        tp += 1
                else:
                    if v == 0:
                        fn += 1
                    else:
                        fp += 1

        print("[{0:<4}|{1:<4}]".format(tn, fn))
        print("[---------]")
        print("[{0:<4}|{1:<4}]".format(fp, tn))

        print("Correct: ", correct_count)
        print("Total: ", total)
        print("Percentage: ", correct_count / total)


    @classmethod
    def make_training(cls, model, the_data, epoch_count):
        return cls(model, the_data, epoch_count)
# 0.5559105431309904
