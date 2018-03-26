import numpy as np
import os
import pickle

n_bytes = 2**31
max_bytes = 2**31 - 1

class EmbeddingsData:
    def __init__(self, keyed_vectors=None):
        if keyed_vectors is None:
            return

        wrd2idx, mat = _load_into_matrix(keyed_vectors)
        self.word_2_idx = wrd2idx
        self.embedding_mat = mat

    def get_word_2_idx(self):
        return self.word_2_idx

    def get_embedding_mat(self):
        return self.embedding_mat

    # Credit for giant pickles: https://stackoverflow.com/a/38003910/2018455
    def save(self, fname):
        with open(str(fname)+".idx", "wb+") as f:
            self.embedding_mat.tofile(f)
        with open(str(fname)+".map", "wb+") as f:
            pickle.dump(self.word_2_idx, f)

    @staticmethod
    def load(fname):
        e = EmbeddingsData()
        with open(str(fname)+".idx", "rb") as f:
            e.embedding_mat = np.fromfile(f)
        with open(str(fname)+".map", "rb") as f:
            e.word_2_idx = pickle.load(f)
        return e

def _load_into_matrix(keyed_vecs):
    word_to_idx = {}
    embedding_matrix = np.zeros((len(keyed_vecs.wv.vocab), 300))
    for i in range(len(keyed_vecs.wv.vocab)):
        word_to_idx[keyed_vecs.wv.index2word[i]] = i
        embedding_vector = keyed_vecs.wv[keyed_vecs.wv.index2word[i]]
        if embedding_vector is not None:
            embedding_matrix[i] = embedding_vector
    return (word_to_idx, embedding_matrix)
