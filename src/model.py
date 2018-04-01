import numpy as np
import tensorflow as tf
import re

class Model:
    def __init__(self, title_ph, article_ph,
                 correct_ph, training_op, eval_op,
                 embeddings, emb_ph):
        self.title_ph = title_ph
        self.article_ph = article_ph
        self.correct_ph = correct_ph
        self.training_op = training_op
        self.eval_op = eval_op

        init_op = tf.global_variables_initializer()

        self.word_2_idx = embeddings.get_word_2_idx()
        self.sess = tf.Session()
        self.sess.run(init_op, feed_dict={ emb_ph: embeddings.get_embedding_mat() })

    def _convert_to_ids(self, word_list):
        return [self.word_2_idx.get(x) for x in word_list]

    def _run_batch(self, batch, op):
        batch_title_ids = []
        batch_body_ids = []
        batch_judgment_ids = []
        for title, body, judgment in batch:
            print(judgment)
            batch_title_ids.append(self._convert_to_ids(title))
            batch_body_ids.append(self._convert_to_ids(body))
            batch_judgment_ids.append(judgment)

        return self.sess.run(op, feed_dict={
            self.title_ph: batch_title_ids,
            self.article_ph: batch_body_ids,
            self.correct_ph: batch_judgment_ids
        })

    def run_train(self, model_input):
        for batch in model_input:
            self._run_batch(batch, self.training_op)

    def run_eval(self, model_input):
        ans = []
        for tbatch, bbatch, _ in model_input:
            ans.append(self._run_batch(tbatch, bbatch, [], self.eval_op))
        return ans

BATCH_SIZE = 1
HIDDEN_LAYERS = 5

def build_model(embeddings_dat):
    mat_ph = tf.placeholder(tf.int32, shape=[3000000, 300], name="Thicc_Matrix")
    embedding = tf.Variable(mat_ph, trainable=False, name="Emb_Var")
    article_ph = tf.placeholder(tf.int32, [BATCH_SIZE, None], name="Article_PH")
    title_ph = tf.placeholder(tf.int32, [BATCH_SIZE, None], name="Title_PH")

    article_vectors = tf.nn.embedding_lookup(embedding, article_ph)
    title_vectors = tf.nn.embedding_lookup(embedding, title_ph)

    cell = tf.contrib.rnn.LSTMCell(HIDDEN_LAYERS)

    article_vectors = tf.cast(article_vectors, dtype=tf.float32)
    output, _ = tf.nn.dynamic_rnn(cell,
                                  article_vectors,
                                  dtype=tf.float32)

    bias_var = tf.get_variable("bias", [BATCH_SIZE, HIDDEN_LAYERS, 1])

    condensed = tf.matmul(output, bias_var)
    added = tf.reduce_sum(condensed, 1)
    output_tensor = tf.sigmoid(added)
    correct_ph = tf.placeholder(tf.float32, [BATCH_SIZE, 1], name="Correct_PH")
    cost_fun = tf.nn.softmax_cross_entropy_with_logits_v2(
        labels=correct_ph,
        logits=output_tensor)

    training_op = tf.train.GradientDescentOptimizer(0.5).minimize(cost_fun)
    return Model(title_ph,
                 article_ph,
                 correct_ph,
                 training_op,
                 output_tensor,
                 embeddings_dat,
                 mat_ph)
