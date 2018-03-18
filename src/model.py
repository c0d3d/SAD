import numpy as np
import tensorflow as tf
import re

class Model:
    def __init__(self, title_ph, article_ph, training_op, embeddings, emb_ph):
        self.title_ph = title_ph
        self.article_ph = article_ph
        self.training_op = training_op
        self.embeddings = embeddings
        self.emb_ph = emb_ph

    def run(self, title, article):
        init_OP = tf.global_variables_initializer()
        sess = tf.Session()
        the_idx_lookup, the_matrix = load_into_matrix(self.embeddings)
        title_ids = map(the_idx_lookup.get, title)
        article_ids = map(the_idx_lookup.get, article)
        sess.run(init_OP)
        for i in range(10):
            training_step = sess.run(model.train_op, feed_dict={
                self.title_ph: title_ids,
                self.article_ids: article_ids,
                self.emb_ph: the_matrix
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

def build_model(keyed_vecs):
    mat_ph = tf.placeholder(tf.int32, shape=[3000000, 300])
    saved_embeddings = tf.Variable([0])
    saved_embeddings = tf.assign(saved_embeddings, mat_ph, validate_shape=False)
    embedding = tf.Variable(initial_value=saved_embeddings, trainable=False)
    article_ph = tf.placeholder(tf.int32, [None])
    title_ph = tf.placeholder(tf.int32, [None])
    article_vectors = tf.expand_dims(tf.nn.embedding_lookup(embedding, article_ph), 1)
    title_vectors = tf.expand_dims(tf.nn.embedding_lookup(embedding, title_ph), 1)

    fw_cell = tf.contrib.rnn.LSTMCell(25)
    bw_cell = tf.contrib.rnn.LSTMCell(25)

    article_vectors = tf.cast(article_vectors, dtype=tf.float32)
    outputs, _ = tf.nn.bidirectional_dynamic_rnn(fw_cell,
                                                 bw_cell,
                                                 article_vectors,
                                                 dtype=tf.float32)
#                                                 initial_state_fw=fw_ts,
#                                                 initial_state_bw=bw_ts)

    outputs = tf.squeeze(outputs[0], 1), tf.squeeze(outputs[1], 1)

    output_tensor = tf.sigmoid(outputs[0])
    training_op = tf.train.GradientDescentOptimizer(0.5).minimize(output_tensor)
    return Model(title_ph, article_ph, training_op, keyed_vecs, mat_ph)
