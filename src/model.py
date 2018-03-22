import numpy as np
import tensorflow as tf
import re

class Model:
    def __init__(self, title_ph, article_ph, training_op, embeddings, emb_ph, correct_ph):
        self.title_ph = title_ph
        self.article_ph = article_ph
        self.training_op = training_op
        self.embeddings = embeddings
        self.emb_ph = emb_ph
        self.correct_ph = correct_ph

    def run(self, title, article, is_fake):
        init_OP = tf.global_variables_initializer()
        sess = tf.Session()
        the_idx_lookup, the_matrix = load_into_matrix(self.embeddings)
        title_ids = [the_idx_lookup.get(x) for x in title]
        article_ids = [the_idx_lookup.get(x) for x in article]

        print("Title ", title_ids, "Article", article_ids)
        print("Initializing big ass matrix ...")
        sess.run(init_OP, feed_dict={ self.emb_ph: the_matrix })
        print("Running the training ...")
        training_step = sess.run(self.training_op, feed_dict={
            self.title_ph: title_ids,
            self.article_ph: article_ids,
            self.correct_ph: is_fake
        })

def load_into_matrix(keyed_vecs):
    word_to_idx = {}
    embedding_matrix = np.zeros((len(keyed_vecs.wv.vocab), 300))
    for i in range(len(keyed_vecs.wv.vocab)):
        word_to_idx[keyed_vecs.wv.index2word[i]] = i
        embedding_vector = keyed_vecs.wv[keyed_vecs.wv.index2word[i]]
        if embedding_vector is not None:
            embedding_matrix[i] = embedding_vector
    return (word_to_idx, embedding_matrix)

BATCH_SIZE = 1
HIDDEN_LAYERS = 5


def build_model(keyed_vecs):
    mat_ph = tf.placeholder(tf.int32, shape=[3000000, 300])
    embedding = tf.Variable(mat_ph, trainable=False)
    article_ph = tf.placeholder(tf.int32, [BATCH_SIZE, None])
    title_ph = tf.placeholder(tf.int32, [BATCH_SIZE, None])

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
    correct_ph = tf.placeholder(tf.float32, [BATCH_SIZE, 1])
    cost_fun = tf.nn.softmax_cross_entropy_with_logits_v2(
        labels=correct_ph,
        logits=output_tensor)

    training_op = tf.train.GradientDescentOptimizer(0.5).minimize(cost_fun)
    return Model(title_ph, article_ph, training_op, keyed_vecs, mat_ph, correct_ph)
