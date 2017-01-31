from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np
import tensorflow as tf

from config import Config
import runner
import utils


class MajorityRunner(runner.Runner):
    '''Runner for the majority dummy model.'''

    def __init__(self, config, topk=8):
        super(MajorityRunner, self).__init__(config, None, train_splits=['train', 'val', 'test'],
                                             val_splits=[], test_splits=[])
        self.preds = np.zeros([config.batch_size, self.reader.label_space_size()], dtype=np.int)
        self.preds[:, :topk] = 1

    def run_session(self, batch, train=True):
        labels = batch[2]
        p, r, f = utils.f1_score(self.preds, labels)
        return ([p, r, f], [])

    def loss_str(self, losses):
        p, r, f = losses
        return "Precision: %.4f, Recall: %.4f, F-score: %.4f" % (p, r, f)

    def output(self, step, losses, extra, train=True):
        print("S:%d.  %s" % (step, self.loss_str(losses)))


def main(_):
    MajorityRunner(Config()).run()


if __name__ == '__main__':
    tf.app.run()