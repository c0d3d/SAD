#!/usr/bin/env python3

from embeddings import EmbeddingsData
from gensim.models import KeyedVectors
from model import build_model
from training import Data, Training
import argparse
import sys

DEFAULT_EMBEDDINGS_PICKLE="embeddings.dat"

parser = argparse.ArgumentParser(description='SAD!')
subparsers = parser.add_subparsers(help="Commands", dest="cmd_type")

# Build the embeddings
parse_emb = subparsers.add_parser("embeddings", help="Construct the pickled embeddings")
parse_emb.add_argument("data", type=str, help="Binary blob for the word2vec pretrained vectors")
parse_emb.add_argument("output", default=DEFAULT_EMBEDDINGS_PICKLE, nargs="?", type=str, help="Basename for the data files that will be output")

# Run a training session
parse_train = subparsers.add_parser("train", help="Run model training")
parse_train.add_argument("train_file", type=argparse.FileType('r'), help="File containing the training data (format: TBD)")
parse_train.add_argument("dev_file", type=argparse.FileType('r'), help="File containing the dev data (format: TBD)")
parse_train.add_argument("--batch-size", type=int, default=1, help="Training batch size")
parse_train.add_argument("--epoch-count", type=int, default=5, help="Number of epochs for training")
parse_train.add_argument("--embeddings-data-file", type=str, default=DEFAULT_EMBEDDINGS_PICKLE, help="Base name for the embeddings data", )

# Run the model on some text
parse_run = subparsers.add_parser("run", help="Run model on some text") # TODO

def main(f=None):
    args = parser.parse_args()
    if args.cmd_type == "embeddings":
        build_embeddings(args.data, args.output)
    elif args.cmd_type:
        embeddings = EmbeddingsData.load(args.embeddings_data_file)
        the_data = Data.make_data(args.train_file, args.dev_file, args.batch_size)
        model = build_model(embeddings)
        train_sess = Training.make_training(model, the_data, args.epoch_count)
        while train_sess.has_more_epochs():
            eval_results = train_sess.next_epoch()
            # TODO check evaluation results
    return 0

def build_embeddings(input_file, output_file):
    print("Loading keyed vectors ...")
    vecs = KeyedVectors.load_word2vec_format(input_file, binary=True)
    print("Constructing pickled embeddings ...")
    EmbeddingsData(vecs).save(output_file)
    print("Done ...")

if __name__ == "__main__":
    exit(main())
