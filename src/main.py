#!/usr/bin/env python3

from gensim.models import KeyedVectors
import sys
import model
import argparse

parser = argparse.ArgumentParser(description='Train SAD!.')
parser.add_argument('--article', type=str, help='article text')
parser.add_argument('--title', type=str, help='title text')
parser.add_argument('--vecs', type=str, help="location of the word vectors")

def main(f=None):
    args = parser.parse_args()
    print("Loading vectors ...")
    vecs = KeyedVectors.load_word2vec_format(args.vecs if f is None else f, binary=True)
    print("Building model ...")
    built_model = model.build_model(vecs)
    print("Training model ...")
    built_model.run(args.title, args.article)

if __name__ == "__main__":
    main()
