

class Data:

    def test_input(self):
        pass

    def eval_input(self):
        pass

    @classmethod
    def make_data(cls, train_file, dev_file, batch_size):
        pass

class Training:
    def __init__(self, model, data, epoch_count):
        self.model = model
        self.data = data
        self.epoch_count = epoch_count
        self.cur_epoch = 0

    def has_more_epochs(self):
        return self.cur_epoch < epoch_count

    def next_epoch(self):
        self.model.run_train(self.data.test_input())
        # TODO eval
        return self.model.run_eval(self.data.eval_input())

    @classmethod
    def make_training(cls, model, the_data, epoch_count):
        return cls(model, the_data, epoch_count)
