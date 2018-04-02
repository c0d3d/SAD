import numpy as np
import tensorflow as tf
import regex as re

def remove_punctuation(text):
    return re.sub(r"\p{P}+", "", text)

class Model:
    def __init__(self, title_ph, article_ph,
                 correct_ph, training_op, eval_op,
                 embeddings, emb_ph):
        self.title_ph = title_ph
        self.article_ph = article_ph
        self.correct_ph = correct_ph
        self.training_op = training_op
        self.eval_op = eval_op
        config = tf.ConfigProto()
        config.intra_op_parallelism_threads = 8
        config.inter_op_parallelism_threads = 8

        init_op = tf.global_variables_initializer()

        self.word_2_idx = embeddings.get_word_2_idx()
        self.sess = tf.Session(config=config)
        self.sess.run(init_op, feed_dict={ emb_ph: embeddings.get_embedding_mat() })
        tf.summary.FileWriter('/tmp/a', graph=self.sess.graph)

    def _convert_to_ids(self, word_list):
        out = []
        for word in word_list:
            ans = remove_punctuation(word).lower()
            look = self.word_2_idx.get(ans)
            if look is not None:
                out.append(look)

        return out

    def _run_batch(self, batch, op):

        batch_title_ids = []
        longest_title = -1
        batch_body_ids = []
        longest_body = -1
        batch_judgment_ids = []
        for title, body, judgment in batch:
            tl = self._convert_to_ids(title.split())
            batch_title_ids.append(tl)
            longest_title = max(longest_title, len(tl))
            bl = self._convert_to_ids(body.split())
            batch_body_ids.append(bl)
            longest_body = max(longest_body, len(bl))
            batch_judgment_ids.append([int(judgment)])

        for t in batch_title_ids:
            while len(t) < longest_title:
                t.append(0)

        for b in batch_body_ids:
            while len(b) < longest_body:
                b.append(0)

        return self.sess.run(op, feed_dict={
            self.title_ph: batch_title_ids,
            self.article_ph: batch_body_ids,
            self.correct_ph: batch_judgment_ids
        })

    def run_train(self, model_input):
        print("Running train ...")
        for batch in model_input:
            self._run_batch(batch, self.training_op)

    def run_eval(self, model_input):
        print("Running eval ...")
        ans = []
        for batch in model_input:
            ans.append(zip(self._run_batch(batch, self.eval_op), map(lambda x: int(x[2]), batch)))
        return ans

HIDDEN_LAYERS = 5

def build_model(embeddings_dat, batch_size):
    mat_ph = tf.placeholder(tf.int32, shape=[3000000, 300], name="Thicc_Matrix")
    embedding = tf.Variable(mat_ph, trainable=False, name="Emb_Var")
    article_ph = tf.placeholder(tf.int32, [batch_size, None], name="Article_PH")
    title_ph = tf.placeholder(tf.int32, [batch_size, None], name="Title_PH")

    article_vectors = tf.nn.embedding_lookup(embedding, article_ph)
    title_vectors = tf.nn.embedding_lookup(embedding, title_ph)

    cell = tf.contrib.rnn.LSTMCell(HIDDEN_LAYERS)

    article_vectors = tf.cast(article_vectors, dtype=tf.float32)
    output, _ = tf.nn.dynamic_rnn(cell,
                                  article_vectors,
                                  dtype=tf.float32)

    bias_var = tf.get_variable("bias", [batch_size, HIDDEN_LAYERS, 1])

    condensed = tf.matmul(output, bias_var)
    added = tf.reduce_sum(condensed, 1)
    output_tensor = tf.sigmoid(added)
    correct_ph = tf.placeholder(tf.float32, [batch_size, 1], name="Correct_PH")
    cost_fun = tf.nn.softmax_cross_entropy_with_logits_v2(
        labels=correct_ph,
        logits=output_tensor)

    training_op = tf.train.GradientDescentOptimizer(0.05).minimize(cost_fun)
    return Model(title_ph,
                 article_ph,
                 correct_ph,
                 training_op,
                 output_tensor,
                 embeddings_dat,
                 mat_ph)
